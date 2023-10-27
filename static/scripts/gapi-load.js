function init() {
    gapi.load('auth2', function() {
      var auth2 = gapi.auth2.init({
        client_id: "1031925357556-g9tr3am18n1vg8ce88svenjgj82onrvt.apps.googleusercontent.com",
        hosted_domain: 'uncc.edu',
        scope: 'email',
        fetch_basic_profile: false,
        redirect_uri: '/home'
      });

    auth2.attachClickHandler('google-signon-div', {});

    auth2.currentUser.listen(function (user) {
        if (user && user.isSignedIn()) {
            validateTokenOnYourServer(user.getAuthResponse().id_token)
                .then(function () {
                    console.log('User logged in');
                })
                .catch(function (err) {
                    auth2.then(function() { auth2.signOut(); });
                });
        }
    });
    });
  }