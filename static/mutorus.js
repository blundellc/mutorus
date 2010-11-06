//(function() {

var want_new = false;
var queue = [];
var offset = 1;
var hash = '';
var scrobbed = true;

function log(msg) {
    setTimeout(function() {
        throw new Error(msg);
    }, 0);
}

$(document).ready(function () {
    $("#qn").click(function () { next(); return false;});
    $("#qf").submit(function () { want(); queue=[]; offset=1; lk(); return false;});
    restore();
});

function want() {
    $('#q').css('background-color','yellow');
    want_new = true;
}

function watch(vid) {
    play(vid.hash);
    want_new = false;
    scrobbed = false;
    hash = vid.hash;
    document.title = vid.title+' (mutorus)';
    $('#q').css('background-color','');
    $('#msg').text(vid.title);
    $('#msg').attr('href',vid.watch);
    save();
}


function play(hash) {
    var ytplay = document.getElementById("ytplay");
    if (!ytplay) {
        loadswf(hash);
    } else {
        ytplay.loadVideoById(hash,0);
        ytplay.playVideo();
    }
}

function loadswf(hh) {
    var params = { allowScriptAccess: "always" };
    var atts = { id: "ytplay" };
    swfobject.embedSWF("http://www.youtube.com/v/"+hh+"?enablejsapi=1&playerapiid=ytplayer&autoplay=1", "ytframe", "425", "356", "8", null, null, params, atts);
}

function onYouTubePlayerReady(playerId) {
    var ytplay = document.getElementById("ytplay");
    ytplay.addEventListener("onStateChange", "sc");
    ytplay.addEventListener("onError", "err");
}


function err() { log('yt error ' + JSON.stringify(arguments)); next(); }
function sc(state) { if (state == 0) { next(); } }

function save() {
    var q = $('#q').val();
    location.hash = hash+'/'+offset+'/'+(q?q:'');
}

function restore() {
    if (location.hash && location.hash != '/') {
        var h = location.hash.slice(1).split('/');
        hash = h.shift()||'';
        offset = parseInt(h.shift())||1;
        var q = h.shift()||'';
        for (var i = 0; i < h.length; i++) {
            q = q + '/' + h[i];
        }
        $('#q').val(q);
        lk();
        if (hash) {
            watch({'hash':hash,'watch':'','title':q});
        }
    }
}

function next() {
    scrob();
    want();
    if (queue.length > 0) {
        watch(queue.pop());
    }
    if (queue.length < 3) {
        lk();
    }
}

function lk() { $.getJSON('/z', {q: $('#q').val()||'', o: offset||1},up); }

function up(data) {
    for (var ii = 0; ii < data.vs.length; ii++) {
        queue.push(data.vs[ii]);
    }
    offset += data.last;
    if (queue.length > 0 && want_new) {
        next();
    }
}

function scrob() {
    if (scrobbed) {
        return;
    }
    var ytplay = document.getElementById("ytplay");
    var remaining = -1;
    if (ytplay) {
        var duration = ytplay.getDuration();
        if (duration) {
            var pos = ytplay.getCurrentTime();
            if (pos) {
                remaining = duration - pos;
            }
        }
    }
    $.getJSON('/scrob', {h: hash||'', r: remaining},function(){});
    scrobbed = true;
}

//})();
