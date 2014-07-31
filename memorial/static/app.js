$(document).ready(function(){
    var messages = io.connect("/message");
    var container = Array()
    var MAX_MESSAGES = 20
    messages.on('message', function(data){
        data.forEach(function(message){
            if (container.length == MAX_MESSAGES){
                container.shift();
            }
            container.push(message);
        });
        $("#messages").html("");
        container.forEach(function(message){
            $("#messages").append("<p><b>" +  message['service'] + " " +  message['date'] + " "  + message['time'] + "</b>: "  + message['text'] + "</p>");
            console.log(message);
        });
    });
});
