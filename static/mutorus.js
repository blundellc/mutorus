var root='';
var want_new = false;
var queue = [];
var offset = 1;

function log(msg) {
    setTimeout(function() {
        throw new Error(msg);
    }, 0);
}

$(document).ready(function () {
    $("#qn").click(function () { want(); next(); return false;});
    $("#qf").submit(function () { want(); queue=[]; offset=1; lk(); return false;});
});

function onYouTubePlayerReady(playerId) {
    var ytplay = document.getElementById("ytplay");
    ytplay.addEventListener("onStateChange", "sc");
    ytplay.addEventListener("onError", "err");
}

function want() {
    $('#q').css('background-color','yellow');
    want_new = true;
}

function err() {
    log('yt error');
    next();
}

function got() {
    $('#q').css('background-color','');
    want_new = false;
}

function sc(state) { if (state == 0) { next(); } }

function next() {
    if (queue.length > 0) {
        var ytplay = document.getElementById("ytplay");
        var vid = queue.pop();
        ytplay.loadVideoByUrl(vid.url,0);
        got();
    }
    if (queue.length < 3) {
        lk();
    }
}

function lk() {
    var qq = $('#q').val();
    $.getJSON(root+'/z', {q: qq, o: offset},up);
}

function up(data) {
    for (var ii = 0; ii < data.vs.length; ii++) {
        queue.push(data.vs[ii]);
    }
    offset += data.last;
    if (queue.length > 0 && want_new) {
        next();
    }
}

(function(){
var params = { allowScriptAccess: "always" };
var atts = { id: "ytplay" };
swfobject.embedSWF("http://www.youtube.com/v/NBDAunPkSAY?enablejsapi=1&playerapiid=ytplayer", "ytframe", "425", "356", "8", null, null, params, atts);
})();

