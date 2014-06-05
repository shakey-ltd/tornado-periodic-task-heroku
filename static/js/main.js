$(document).ready(function() {
    setTimeout(requestLogs, 10);
});

function requestLogs() {
    var host = 'ws://' + location.host + '/logs'

    ws = new WebSocket(host);

    var websocket = new WebSocket(host);

    websocket.onopen = function (evt) { };
    websocket.onmessage = function(evt) {
        var timestap = $.parseJSON(evt.data)['timestamp'];
        var text = $.parseJSON(evt.data)['text'];
        $("#log-list").prepend('<dt>'+timestap+'</dt><dd>'+text+'</dd>');
    };
    websocket.onerror = function (evt) { };
}