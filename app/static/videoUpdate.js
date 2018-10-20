// Client Side Javascript to receive numbers.
$(document).ready(function(){
    // start up the SocketIO connection to the server - the namespace 'test' is also included here if necessary
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    console.log(socket);

    $('form').submit(function(event) {
        socket.emit('my event', {data: $('#url').val()});
        return false;
    });
    // this is a callback that triggers when the "my response" event is emitted by the server.
    socket.on('my response', function(msg) {

      console.log('receive');;
      console.log(msg);;
    });
});
