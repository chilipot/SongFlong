// Client Side Javascript to receive numbers.
$(document).ready(function(){
    // start up the SocketIO connection to the server - the namespace 'test' is also included here if necessary
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    var temp = "";
    console.log(socket);
    // this is a callback that triggers when the "my response" event is emitted by the server.
    socket.on('connection made', function(msg) {

      console.log('receive');
      console.log(msg);
    });

    socket.on('data created', function(msg) {

      console.log(msg);
      socket.emit('get data')
    });

    socket.on('send data', function(msg) {
      data = msg.content
      console.log(msg);

      for (i = 0, len = data.length; i < len; i++) {
        console.log(i);
        $('#video' + i + ' source').attr("src", data[i]['file']);
        $('#art' + i).attr("src", data[i]['art']);
        console.log($('#video' + i)[0]);
        $('#video' + i).get(0).load();
        console.log(data[i]['file']);
        console.log($('#video' + i));

        // $('#title' + i).attr("src", data.art);
      }
      console.log("Updated");

    });

    $('form').submit(function(event) {
      console.log("submitted");
        socket.emit('send search', {data: $('#url').val()});
        return false;
    });
});
