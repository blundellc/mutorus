var root='';
var want_new = false;

function log(msg) {
    setTimeout(function() {
        throw new Error(msg);
    }, 0);
}

$(document).ready(function () {
    //$("#qs").click(function () {$("#qf").submit(); return false;});
    $("#qn").click(function () { log('button next');want_new = true; next(); return false;});
    $("#qf").submit(function () { want_new = true; lk(); return false;});
});
function onYouTubePlayerReady(playerId) {
    var ytplay = document.getElementById("ytplay");
    ytplay.addEventListener("onStateChange", "sc");
    ytplay.addEventListener("onError", "next");
}

function sc(state) { log('state is ' + state); if (state == 0) { next(); } }
var queue = [];
function next() {
    log('next?');
    if (queue.length > 0) {
        var ytplay = document.getElementById("ytplay");
        var vid = queue.pop();
        log('now playing ' + vid.url);
        ytplay.loadVideoByUrl(vid.url,0);
        want_new = false;
    }
    if (queue.length < 3) {
        log('want more');
        lk();
    }
} 
function lk() {
    var qq = $('input[name="q"]').val();
    $.getJSON(root+'/z', {q: qq},up);
    return false;
}
function up(data) {
    log('data: ' +data.vs.length);
    for (var ii = 0; ii < data.vs.length; ii++) {
        queue.push(data.vs[ii]);
    }
    if (queue.length > 0 && want_new) {
        next();
    }
}

(function(){
var params = { allowScriptAccess: "always" };
var atts = { id: "ytplay" };
swfobject.embedSWF("http://www.youtube.com/v/NBDAunPkSAY?enablejsapi=1&playerapiid=ytplayer", "ytframe", "425", "356", "8", null, null, params, atts);
})();

