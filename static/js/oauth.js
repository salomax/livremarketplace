/**
 * Most of this code is taken from the offical Google+ Sign In Documentation
 * https://developers.google.com/+/web/people/#retrieve_an_authenticated_users_email_address
 * Make sure to refer to the link if something isn't clear.
 *
 * Credits for mkhatib
 * https://github.com/mkhatib/googleplus-signin-appengine-endpoints-python
 */

var API_ROOT = '//' + document.location.host + '/_ah/api';


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
}


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

        // Importar HTML do main     
        $('#wrapper').html(response);  

        // Attach dropdowns
        $('.dropdown-toggle').dropdown();

        // Definir imagem do usuário
        $('img.user-image').attr('src', obj.image.url);
        $('img.user-image-lg').attr('src', obj.image.url + '&sz=160');

        // Definir nome do usuário
        $('span.user-display-name').html(obj.displayName);


      }); // Fim do ajax()

    }); // Fim do request.execute()

  }); // Fim do gapi.client.load

  // TODO Logout
  // https://mail.google.com/mail/u/0/?logout&hl=en

  // Make an authenticated call to our own Greeting API Backend.
  // gapi.client.load('greetings', 'v1', function() {
  //   var request = gapi.client.greetings.get();
  //   request.execute(function(response) {
  //     $('#greeting').text(response.msg).show();
  //   });
  // }, API_ROOT);
}