$(document).ready(function(){
    var messages = io.connect("/message");
    var container = Array()
    var MAX_MESSAGES = 20
    messages.on('message', function(data){
        data.forEach(function(message){
            if (container.length == MAX_MESSAGES){
                container.pop();
            }
            container.unshift(message);
        });
        $("#messages").html("");
        var first = true;
        container.forEach(function(message){
            $message = $("<div class='message'></div>");
            $message.append("<div class='datetime'>" + message['time'] + "<span class='date'> "  + message['date'] + "</span>:</div>");
            $message.append("<div class='text'>" + message['text'] + "</div>");
            $("#messages").append($message);
        });
    });
});
