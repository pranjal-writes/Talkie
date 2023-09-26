from django.shortcuts import render, HttpResponse
from django.core import serializers
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .models import Profile
from .models import Message
from .models import FriendRequest
from datetime import datetime
from django.db.models import Q


import json

from django.core.files.base import ContentFile
from PIL import Image
import base64
import os




# Create your views here.
@login_required(login_url='login')
def home(request):
    contact_query = request.user.profile.friends.all()
    contact_list = []
    for i in contact_query:
        if i != request.user:
            contact_list.append(i)
        else:
            pass
    

    

        
    all_messages = Message.objects.filter(recipient=request.user)
        
    params = {'names': contact_list}
    
        
    return render(request, 'chat/chat.html', params)




@require_GET
def get_chat_history(request):
    recipient = request.GET.get('contact_name')
    messages = Message.objects.filter(
        (Q(sender__username=request.user.username) & Q(recipient__username=recipient))|
        (Q(sender__username=recipient) & Q(recipient__username=request.user.username))
    
    ).order_by('timestamp')
    chat_history = [
            {
                'id': message.id,
                'sender': message.sender.username,
                'recipient': message.recipient.username,
                'content': message.content,
                'sent': message.sender.username == request.user.username,
                'timestamp': message.timestamp.isoformat(),
            }
            for message in messages
        ]
    
    
    return JsonResponse({'chat_history': chat_history})


@require_POST
def send_message(request):
    sender = request.user
    rec = request.POST.get('recipient')
    recipient = User.objects.get(username=rec)
    content = request.POST.get('message')
    message = Message(sender=sender,recipient=recipient, content=content)
    message.save()
    return JsonResponse({})








@require_GET
def get_new_messages(request):
    recipient = request.GET.get('contact_name')
    last_message_id = request.GET.get('last_message_id')
    sender_username = request.user.username

    try:
        last_message_id = int(last_message_id)
    except:
        last_message_id = 0 


    messages = Message.objects.filter(
        (Q(sender__username=sender_username) & Q(recipient__username=recipient))|
        (Q(sender__username=recipient) & Q(recipient__username=sender_username)),
        id__gt = last_message_id
    
    ).order_by('timestamp')

    new_messages = [
            {
                'id': message.id,
                'sender': message.sender.username,
                'recipient': message.recipient.username,
                'content': message.content,
                'sent': message.sender.username == request.user.username,
                'timestamp': message.timestamp.isoformat(),
            }
            for message in messages
        ]
    
    
    return JsonResponse({'new_messages': new_messages})







def get_unread_message_counts(request):
    sender_username = request.user.username
    contacts = request.user.profile.friends.all()
    unread_message_counts = {}

    for contact in contacts:
        unread_count = Message.objects.filter(
            sender = contact,
            recipient = request.user,
            is_read = False 
        ).count()
        unread_message_counts[contact.username] = unread_count
    
    return JsonResponse({'unread_message_counts': unread_message_counts})


def mark_as_read(request):
    rec = request.GET.get('contactName')
   
    sender = User.objects.get(username=rec)
    messages = Message.objects.filter(sender=sender,recipient=request.user, is_read=False)
    
    messages.update(is_read=True)
    return JsonResponse({})






def send_friend_request(request):
    recipient_user = request.POST.get('recipient_user')
    
    recipient = User.objects.get(username=recipient_user)
    existing_request = FriendRequest.objects.filter(sender=request.user, recipient=recipient,status='pending').exists()
    existing_request2 = FriendRequest.objects.filter(sender=recipient, recipient=request.user ,status='pending').exists()
    already_friends= Profile.objects.filter(user=request.user, friends=recipient).exists()
    already_friends2= Profile.objects.filter(user=recipient, friends=request.user).exists()
    
    if request.method == 'POST' and not existing_request and not already_friends:
        friend_request = FriendRequest(sender=request.user, recipient=recipient)
        friend_request.save()

        return JsonResponse({'status': 'success'})
    elif existing_request or existing_request2:
        return JsonResponse({'status': 'existing_request'})
    elif already_friends or already_friends2:
        return JsonResponse({'status': 'already_friends'})
    else:
        return JsonResponse({'status': 'error'})




def get_pending_requests(request):
    pending_requests = FriendRequest.objects.filter(status='pending', recipient=request.user)
    friend_requests_data = [{'id':req.id, 'sender':req.sender.username, 'recipient':req.recipient.username}for req in pending_requests]

    return JsonResponse({'friend_requests': friend_requests_data})



def accept_friend_request(request):
    request_id = request.POST.get('request_id')
    friend_request = FriendRequest.objects.filter(id=request_id, recipient=request.user)

    if request.method == 'POST':
        friend_request.update(status='accepted')
        acceptor_profile = Profile.objects.get(user=request.user)


        
        name = request.POST.get('sender_name')
        sender_name = User.objects.get(username=name)
        sender_profile= Profile.objects.get(user=sender_name)
        
        

        acceptor_name = acceptor_profile.user
        sender_name = sender_profile.user
        acceptor_profile.friends.add(sender_name)
        acceptor_profile.save()
        sender_profile.friends.add(acceptor_name)
        sender_profile.save()
        
        return JsonResponse({'status':'success'})

    return JsonResponse({'status':'error'})


def delete_friend_request(request):
    request_id = request.POST.get('request_id')
    friend_request = FriendRequest.objects.filter(id=request_id, recipient=request.user)
    

    if request.method == 'POST' and friend_request.exists():
        friend_request.delete()
        
        return JsonResponse({'status': 'deleted'})
    return JsonResponse({'status': 'error'})

@login_required(login_url='login')
def notifications(request):
    return render(request, 'chat/notifications.html')



@login_required(login_url='login')
def search_user(request):

    
        
    params = {}
    return render(request, 'chat/search_user.html', params)
def available_users(request):
    username = request.POST.get('username')
    avail_users = []
    temp = {}
    
    if username != None and username!="":
        if get_user_model().objects.filter(username__startswith=username)!= None:
            temp =get_user_model().objects.filter(username__startswith=username)
        
        else:
            print("no user")

    

    for i in temp:
        if i != request.user:
            avail_users.append(i.username)
        else:
            pass

    data = json.dumps(avail_users)
    return JsonResponse(data, safe=False)




@login_required(login_url='login')
def group_chat(request):
    return render(request, 'chat/group-chat.html')


@login_required(login_url='login')
def user_profile(request):
    params = {'user': request.user, 'dp':request.user.profile.dp.url}
    return render(request, 'chat/user-profile.html',params)

@require_POST
def upload_profile_picture(request):
    # Handle POST request for profile picture upload
    if request.method == 'POST':
        profile_picture = request.POST.get('profile_picture')  # Get the base64-encoded profile picture

        

        user_profile = request.user.profile

        # Decode the base64-encoded profile picture to bytes
        image_data = base64.b64decode(profile_picture.split(',')[1])

        # Create a ContentFile from the decoded image data
        image_file = ContentFile(image_data, name='profile_picture.png')

        # Resize the image if needed (optional)
        img = Image.open(image_file)
        max_size = (300, 300)
        img.thumbnail(max_size)

        # Save the image to the user's profile
        user_profile.dp.save('profile_picture.png', image_file, save=True)

        # Replace the following line with your logic to get the URL of the saved profile picture
        # For this example, we are just returning the URL of the ImageField
        profile_picture_url = user_profile.dp.url

        return JsonResponse({'status': 'success', 'profile_picture_url': profile_picture_url})





@login_required(login_url='login')
def logout(request):
    
    return redirect('login/')