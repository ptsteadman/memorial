var memorial = {

    init: function(){
        memorial.messages = io.connect("/message");
        memorial.queue = Array();
        memorial.startQueue();
        memorial.initControls();
        memorial.fast = false;
        
        // display help info and set up an event listener
        // to detect when we're not holding onto a message
        $(document).mouseup(function(){
                $("#clicked-on").html("") 
                $("#clicked-on").css("display", "none");
        });

        setTimeout(function(){ $("#welcome").fadeOut(300); }, 3000);
    },

    startQueue: function(){
        // stick messages into a queue as they're sent from the server
        memorial.messages.on('message', function(data){
            data.forEach(function(message){
                memorial.queue.push(message);
            });
        });
        // periodically render the messages one by one (avoids large dumps)
        memorial.interval = setInterval(function(){ memorial.pullFromQueue(250, 150); }, 200);
    },

    pullFromQueue: function(fadeSpeed, slideSpeed){

        // get a message from the queue and prepend it
        if (memorial.queue.length > 0){
            var message = memorial.queue.shift()
            $message = $("<div class='message'></div>");
            var datetime = message['time'] + " " + message['date']
            $message.append("<div class='datetime'>" + datetime + "</div>");
            $message.append("<div class='text'>" + message['text'] + "</div>"); $message.css({opacity: '0'});
            // add event listeners to new divs
            memorial.messageDivListeners($message);
            $message.hide().prependTo("#messages").slideDown(slideSpeed).animate({ opacity: '1'}, fadeSpeed);
        }

        // speed the rate we pull if the queue is getting large
        if (memorial.queue.length >= 5 && memorial.fast == false){
            clearInterval(memorial.interval);
            memorial.interval = setInterval(function(){ memorial.pullFromQueue(150, 100); }, 100);
            memorial.fast = true;
        } 

        // calm it down if the queue is small
        if (memorial.queue.length <  5 && memorial.fast == true){
            clearInterval(memorial.interval);
            memorial.interval = setInterval(function(){ memorial.pullFromQueue(250, 150); }, 200);
            memorial.fast = false;
        } 
        
        // delete messages that are outside the viewport
        if(($("#messages").height() + 40 +  $("#header").height()) >= $(window).height()){
            $(".message:last").fadeOut(200, function(){ $(this).off();  $(this).remove();  })
        }

    },

    initControls: function(){
        function htmlEncode(value){ return $('<div/>').text(value).html(); }
        function htmlDecode(value){ return $('<div/>').html(value).text(); } 

        $("#expand").click(function(){
            $("#controls-container").toggle();
            var plusminus = $("#plus-minus").text() == " + " ? " - " : " + ";
            $("#plus-minus").text(plusminus);
        });
        // read time value from text input, send to server
        $("#settime").click(function(){
            var hours = $("#hours").val();
            var minutes = $("#minutes").val();
            var seconds = $("#seconds").val();
            memorial.messages.emit('settime', hours + ":" + minutes + ":" + seconds);
        });

        $("#setstate").click(function(){
            var state_to_set = $("#setstate").attr("value") == '◼' ? 'paused' : 'running';
            memorial.messages.emit('setstate', state_to_set);
            var btn_value = state_to_set == 'running' ? '◼' : '►';
            $("#setstate").attr("value", btn_value);
        });

        // server responds with failure message or the time value
        memorial.messages.on('settime-status', function(data){
            if (data == 'failure'){
                $("#settime-msg").html("Invalid time.");
            } else {
                $("#settime-msg").html("Time set to " + data + ".");
                $("#messages").empty();
                memorial.queue = Array()
            }
        });
    },

    messageDivListeners: function($message){
        // listener to show full text on hover
        $message.on('mouseenter', function(e){
            $el = $(e.target);
            $el.css("max-height", "none");
            $el.on('mouseleave',function(e){
                $el.css("max-height", "120px");
            })
        });
        
        // listener to "hold" on click
        $message.on('mousedown', function(e){
            $("#clicked-on").html($(this).html())
            $("#clicked-on").css("display", "block" );
            $("#clicked-on").css("left", $(this).position().left - 2);
            $("#clicked-on").css("top", $(this).position().top + 10);                
            $("#clicked-on").css("width", $(this).width());
        });
    },

};

$(document).ready(memorial.init);


