        // // themes menu display
        // $('#theme').click(function () {
        //     $('.style-switcher').toggle(function () {
        //         $('.style-switcher').addClass('open'), function () {
        //             $('.style-switcher').css('display', 'block')
        //         }
        
        //     });
        
        // })
        
        // // themes selection
        
        // $('.color-1').click(function () {
        //     $('.color-1-link').removeAttr('disabled');
        //     $('.color-2-link').prop('disabled', true);
        //     $('.color-3-link').prop('disabled', true);
        //     $('#theme').click();
        // })
        // $('.color-2').click(function () {
        //     $('.color-2-link').removeAttr('disabled');
        //     $('.color-1-link').prop('disabled', true);
        //     $('.color-3-link').prop('disabled', true);
        //     $('#theme').click();
        // })
        // $('.color-3').click(function () {
        //     $('.color-3-link').removeAttr('disabled');
        //     $('.color-2-link').prop('disabled', true);
        //     $('.color-1-link').prop('disabled', true);
        //     $('#theme').click();
        // })
        // $('.light-dark-switch').click(function () {
        //     if ($('.light-theme').prop('disabled')) {
        //         $('.light-theme').removeAttr('disabled')
        //         $('.dark-theme').prop('disabled', true);
        //         $('.sun-moon').removeClass('ion-ios-sunny').addClass('ion-ios-moon')
        //     } else {
        //         $('.dark-theme').removeAttr('disabled')
        //         $('.light-theme').prop('disabled', true);
        //         $('.sun-moon').removeClass('ion-ios-moon').addClass('ion-ios-sunny')
        //     }
        
        // })
        
        
        // nav-menu selection
        function select(element) {
            $('.select').removeClass('active').filter(element).toggleClass('active');
        }
        
        // selecting chats
        function selectChat(element) {
            updatechats();
            $('.chatname').removeClass('active-chat').filter(element).toggleClass('active-chat');
            var name = $(this).find('.name').text().trim()
            var img_src = $(this).find('img').attr('src');
            
            $('#chats .name').text(name)
            $('#chats .dp img').attr('src', img_src)
            $('.active-contact').removeClass('hidden')
            $('#messagebox').removeClass('hidden')
        
            
        }
        
        $('.chatname').on('click', function(){
            var name = $(this).find('.name').text().trim()
            var img_src = $(this).find('img').attr('src');
            
            $('#chats .name').text(name)
            $('#chats .dp img').attr('src', img_src)
        })
        
        var allItems = $('.chatnames')
        function isAnyItemSelected(){
            return allItems.hasClass('active-chat')
        }
        function updatechats(){
            $('.box').toggleClass("hidden", isAnyItemSelected())
        }
        
        
        // responsive actions
        if ($(window).width() < 820) {
        
            $('.chatname').click(function () {
                $('#chats').css('display', 'block'),
                    $('#chat-contacts').css('display', 'none')
            })
        
            $('.backbtn').toggle(function () {
                $('#chats').css('display', 'none'),
                    $('#chat-contacts').css('display', 'block')
            })
        
        }



var lastMessageId = null;
function loadChatHistory(contactName){
    $.ajax({
        type:'GET',
        url: 'get_chat_history',
        data:{
            'contact_name':contactName
        },
        dataType: 'json',
        success: function (data){
           
            var chatBox = $('.chat-messages');
            var sentMessages = $('.sent')
            var receivedMessages = $('.received')
            var messageContent = '';
            chatBox.empty();
            $.each(data.chat_history, function(index, message){
                
                var messageClass = message.sent ? 'sent':'received';
                
                
                
                if (message.sent){
                    // sentMessages.append(messageContent)
                    messageContent += '<div class="texts"><div class=" '+ messageClass+'">'+  message.content+ '</div></div>'
                }else{
                    messageContent += '<div class=" '+ messageClass+'">'+  message.content+ '</div>'
                }
                lastMessageId = message.id
            })
            $('.chat-messages').html(messageContent)
            
            var activeContact = $('.active-contact .name')
            activeContact.data('last-message-id', lastMessageId)
            
        }
    })
    
}

$('.chatnames .chatname').click(function(){
    var contactName = $(this).find('.name').text().trim()
    loadChatHistory(contactName)


    $.ajax({
        type:'GET',
        url: 'mark_as_read',
        data:{
            'contactName':contactName,
        },
        dataType: 'json',
        success: function (data){
            
            
        }
    })


} )


function sendMessage(message, recipient){
    $.ajax({
        type:'POST',
        async: true,
        url: 'send_message',
        data:{
            csrfmiddlewaretoken: $('[name="csrfmiddlewaretoken"]').val(),
            // csrfmiddlewaretoken: "{{ csrf_token }}",
            'message': message,
            'recipient': recipient,
            
        },
        success: function(){

            $('#messagebox .message-box input').val("")
            loadChatHistory(recipient)
        }
    })
}

$('.message-box').submit(function(event){
    event.preventDefault();
    var message = $('#messagebox .message-box input').val();
    var recipient = $('#chats .name').text().trim()
    sendMessage(message, recipient)
})

function checkForNewMessages(){
    var activeContact = $('.active-contact .name');
    var contactUsername = activeContact.text().trim()
    var lastMessageId = activeContact.data('last-message-id')


    $.ajax({
        type:'GET',
        url: 'get_new_messages',
        data:{
            'contact_name':contactUsername,
            'last_message_id': lastMessageId
        },
        dataType: 'json',
        success: function (data){
            
            var messageContent = '';
            if(data.new_messages){

                $.each(data.new_messages, function(index, message){

                    var messageClass = message.sent ? 'sent':'received';
                
                
                
                if (message.sent){
                    
                    messageContent += '<div class="texts"><div class=" '+ messageClass+'">'+  message.content+ '</div></div>'
                }else{
                    messageContent += '<div class=" '+ messageClass+'">'+  message.content+ '</div>'
                }

                lastMessageId = message.id

                })
                if(messageContent != ''){
                $('.chat-messages').html(function(){
                    $(this).append(messageContent)
                    var chatBox = $('.chat-messages');
                    chatBox.scrollTop(chatBox[0].scrollHeight)
                })}
                else{

                }
            
                var activeContact = $('.active-contact .name')
                activeContact.data('last-message-id', lastMessageId)

                

                var notificationBadge = $('#chats .name').find('.notification-badge')
                notificationBadge.text('')

            }
            
        }
    })


}



function startCheckingForNewMessages(){
    setInterval(checkForNewMessages, 3000)
}

startCheckingForNewMessages()

function updateNotificationBadge(){
    $.ajax({
        type: 'GET',
        url: 'get_unread_message_counts',
        dataType: 'json',
        success: function (data){
            var unreadMessageCounts = data.unread_message_counts;
            var contacts = $('.chatnames .chatname')
            
            contacts.each(function(){
                var contactUsername = $(this).find('.name').text().trim();
                
                var notificationBadge= $(this).find('.notification-badge')
                var unreadCount = unreadMessageCounts[contactUsername] || 0
                
                if(unreadCount>0){
                    notificationBadge.text(unreadCount).show()
                }else{
                    notificationBadge.text('').hide()
                }
            })
        }
    })
}
updateNotificationBadge()
setInterval(updateNotificationBadge, 3000)


