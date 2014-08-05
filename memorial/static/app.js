$(document).ready(function(){
    var messages = io.connect("/message");
    var queue = Array() 
    var container = Array()
    $("#expand").click(function(){ $("#controls").toggle()});
    messages.on('message', function(data){
        data.forEach(function(message){
            queue.push(message);
        });
    });
    
    var pullFromQueue = function(){
        $(".text").on('mouseenter', function(e){
            $el = $(e.target);
            $el.css("max-height", "none");
            console.log('in');
            $el.on('mouseleave',function(e){
                $el.css("max-height", "120px");
            })
        });

        if (queue.length > 0){
            var message = queue.shift()
            $message = $("<div class='message'></div>");
            $message.append("<div class='datetime'>" + message['time'] + "<span class='date'> "  + message['date'] + "</span></div>");
            $message.append("<div class='text'>" + message['text'] + "</div>");
            $message.css({opacity: '0'})
            $message.hide().prependTo("#messages").slideDown(100).animate({ opacity: '1'},200);
        }
        
        if(($("#messages").height() - 1000 +  $("#header").height()) >= $(window).height()){
            $(".message:last").fadeOut(300, function(){ $(this).off();  $(this).remove();  })
        }
    }

    setInterval(pullFromQueue, 330);

})
