var client_id = 'ea818cb4d2c943bf9e70dbbee6ca0608';
var redirect_uri = 'http://127.0.0.1:5500/index.html';
var client_secret = '4b1b7a9333494eeb974dccaa3780f341'
const AUTHORIZE ='https://accounts.spotify.com/authorize';

function Login(){
 let url = AUTHORIZE;
 url+="?client_id="+client_id;
 url+="&response_type=code";
 url += "&redirect_uri=" + encodeURI(redirect_uri);
 url+="&show_dialog=true"
 url+="&scope=user-read-private user-read-email user-read-playback-state user-top-read"
      
 window.location.href = url;
}