function Login(){
  var client_id = '';
  var redirect_uri = 'http://127.0.0.1:5500/index.html';
  
  var app = express();
  
  app.get('/login', function(req, res) {
  
    var state = generateRandomString(16);
    var scope = 'user-read-private user-read-email';
  
    res.redirect('https://accounts.spotify.com/authorize?' +
      querystring.stringify({
        response_type: 'code',
        client_id: client_id,
        scope: scope,
        redirect_uri: redirect_uri,
        state: state
      }));
  });
}