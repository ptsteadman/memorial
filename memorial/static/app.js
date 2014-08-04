$(document).ready(function(){
    var messages = io.connect("/message");
    var queue = Array() 
    var container = Array()
    messages.on('message', function(data){
        data.forEach(function(message){
            queue.push(message);
        });
    });
    
    var pullFromQueue = function(){
        if (queue.length > 0){
            var message = queue.shift()
            $message = $("<div class='message'></div>");
            $message.append("<div class='datetime'>" + message['time'] + "<span class='date'> "  + message['date'] + "</span>:</div>");
            $message.append("<div class='text'>" + message['text'] + "</div>");
            $message.hide().prependTo("#messages").slideDown(150);
        }
        
        if(($("#messages").height() + 36 +  $("#header").height()) >= $(window).height()){
            console.log('remove')
            $(".message:last").fadeOut(300, function(){ $(this).remove(); })
        }
    }

    setInterval(pullFromQueue, 330);
})
