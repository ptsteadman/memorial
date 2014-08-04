$(document).ready(function(){
    var messages = io.connect("/message");
    var queue = Array() 
    var container = Array()
    var MAX_MESSAGES = 20
    messages.on('message', function(data){
        data.forEach(function(message){
            queue.push(message);
        });
    });
    
    var pullFromQueue = function(){
        if (queue.length > 0){
            message = queue.shift()
            $message = $("<div class='message'></div>");
            $message.append("<div class='datetime'>" + message['time'] + "<span class='date'> "  + message['date'] + "</span>:</div>");
            $message.append("<div class='text'>" + message['text'] + "</div>");
            $message.hide().prependTo("#messages").slideDown(250);
        }
        
        if(($("#messages").height() + 25 +  $("#header").height()) > $(window).height()){
            console.log('remove')
            $(".message:last").fadeOut(300, function(){ $(this).remove(); })
        }
    }

    setInterval(pullFromQueue, 250);
})
