$(document).ready(function() {
    setTimeout(requestLogs, 10);
});

function requestLogs() {
    var host = 'wss://' + location.host + '/logs'

    ws = new WebSocket(host);

    var websocket = new WebSocket(host);

    websocket.onopen = function (evt) { };
    websocket.onmessage = function(evt) {
        $('#count').html($.parseJSON(evt.data)['count']);
    };
    websocket.onerror = function (evt) { };
}