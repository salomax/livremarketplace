
/******************************************************************************
 * oauth.js
 *
 * Copyright 2016 Marcos Salomão
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * 
 *     http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 * @version     1.0
 * @author      Marcos Salomão (salomao.marcos@gmail.com)
 *****************************************************************************/

/**
 * Most of this code is taken from the offical Google+ Sign In Documentation
 * https://developers.google.com/+/web/people/#retrieve_an_authenticated_users_email_address
 * Make sure to refer to the link if something isn't clear.
 *
 * Credits for mkhatib
 * https://github.com/mkhatib/googleplus-signin-appengine-endpoints-python
 */

/*
 * Triggered when the user accepts the the sign in, cancels, or closes the
 * authorization dialog.
 */
function loginFinishedCallback(authResult) {
  
  if (authResult) {

    if (authResult['error'] == undefined){

      // This is important for any subsequent authenticated gapi.client requests to work.
      // Including CoinRun API backend. This stores the returned token.
      gapi.auth.setToken(authResult);
      $('#signin-button').hide();
      getInfo();

    } else {

      console.log('An error occurred');

    }

  } else {

    console.log('Empty authResult. Something went wrong.');

  }

};

/*
 * Initiates the request to the userinfo endpoint to get the user's email
 * address. This function relies on the gapi.auth.setToken containing a valid
 * OAuth access token.
 *
 * When the request completes, the getEmailCallback is triggered and passed
 * the result of the request.
 */
function getInfo() {

  // Load the oauth2 libraries to enable the userinfo methods.
  gapi.client.load('oauth2', 'v2', function() {

    var request = gapi.client.oauth2.userinfo.get();

    request.execute(function(obj){

      $('#email').text(obj.email);

    });

  });

  // Get user profile.
  gapi.client.load('plus','v1', function(){
    var request = gapi.client.plus.people.get({
      'userId': 'me'
    });

    request.execute(function(obj) {
      $.ajax({
        url: "/main",
        context: document.body
      }).done(function(response) {

        // Importar main html    
        $('#wrapper').html(response);

        // Carregar a página principal.
        $.main.load();

        // Importar script do bootstratp template vendor (AdminLTE)
        // E atachar os componentes necessários após carregado
        $.getScript('/js/vendor.min.js', function() {

          // Attach dropdowns
          $('.dropdown-toggle').dropdown();

          // Definir imagem do usuário
          $('img.user-image').attr('src', obj.image.url);
          $('img.user-image-lg').attr('src', obj.image.url + '&sz=160');

          // Definir nome do usuário
          $('span.user-display-name').html(obj.displayName);

        });

      }); // Fim do ajax()

    }); // Fim do request.execute()

  }); // Fim do gapi.client.load

};
