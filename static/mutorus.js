var root='';
var want_new = false;
var queue = [];
var offset = 1;
var hash = 'NBDAunPkSAY';

function log(msg) {
    setTimeout(function() {
        throw new Error(msg);
    }, 0);
}

$(document).ready(function () {
    $("#qn").click(function () { want(); next(); return false;});
    $("#qf").submit(function () { want(); queue=[]; offset=1; lk(); return false;});
    var params = { allowScriptAccess: "always" };
    var atts = { id: "ytplay" };
    restore();
    swfobject.embedSWF("http://www.youtube.com/v/"+hash+"?enablejsapi=1&playerapiid=ytplayer", "ytframe", "425", "356", "8", null, null, params, atts);
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

function got(vid) {
    want_new = false;
    var ytplay = document.getElementById("ytplay");
    ytplay.loadVideoByUrl(vid.url,0);
    ytplay.playVideo();
    document.title = vid.title+' (mutorus)';
    $('#q').css('background-color','');
    $('#msg').text(vid.title);
    $('#msg').attr('href',vid.url);
    hash = vid.url.replace(/^http:..www.youtube.com(.watch)?.v.([^&?]+)([?&].*)?$/, "$2");
    save();
}

function save() {
    var q = $('#q').val();
    if (q) {
        location.hash = hash+'/'+q;
    } else {
        location.hash = hash+'/';
    }
}

function restore() {
    log('restore ' + location.hash);
    if (location.hash && location.hash != '/') {
        var h = location.hash.slice(1).split('/',2);
        hash = h.shift();
        var q = h.shift();
        for (var i = 0; i < h.length; i++) {
            q = q + '/' + h[i];
        }
        $('#q').val(q);
        lk();
    }
}

function sc(state) { log('state ' + state); if (state == 0) { next(); } }

function next() {
    log('next');
    if (queue.length > 0) {
        got(queue.pop());
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


