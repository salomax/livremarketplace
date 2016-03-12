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
function onSignIn(googleUser) {

    var profile = googleUser.getBasicProfile();

    $.ajax({
        url: "/main",
        context: document.body
    }).done(function(response) {

        // Importar main html    
        $('.wrapper').html(response);

        // Carregar a página principal.
        $.main.load();

        // Attach dropdowns
        $('.dropdown-toggle').dropdown();

        // Definir imagem do usuário
        var image = (profile.getImageUrl() ? profile.getImageUrl() : '/img/profile.png');
        $('img.user-image').attr('src', image);
        $('img.user-image-sidebar').attr('src', image + '?sz=160');

        // Definir nome do usuário
        $('span.user-display-name').html(profile.getName());

        // Sign out button
        $('a.sign-out').click(function() {
              signOut();
            });

    }); // Fim done()

} // Fim onSignIn

/**
 * Sign out.
 */
function signOut() {
    var auth2 = gapi.auth2.getAuthInstance();
    auth2.signOut().then(function () {
      console.log('User signed out.');
      window.location = '/'
    });
  }