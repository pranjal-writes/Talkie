from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),
    # path('receive_message', views.receive_message, name='receive_message'),
    path('send_message', views.send_message, name='send_message'),
    path('get_chat_history', views.get_chat_history, name='get_chat_history'),
    path('get_new_messages', views.get_new_messages, name='get_new_messages'),
    path('mark_as_read', views.mark_as_read, name='mark_as_read'),
    path('get_unread_message_counts', views.get_unread_message_counts, name='get_unread_message_counts'),
    # path('group_chat', views.group_chat, name='group_chat'),
    path('search_user', views.search_user, name='search_user'),
    path('notifications', views.notifications, name='notifications'),
    path('send_friend_request', views.send_friend_request, name='send_friend_request'),
    path('get_pending_requests', views.get_pending_requests, name='get_pending_requests'),
    path('accept_friend_request', views.accept_friend_request, name='accept_friend_request'),
    path('delete_friend_request', views.delete_friend_request, name='delete_friend_request'),
    path('available_users', views.available_users, name='available_users'),
    path('user_profile', views.user_profile, name='user_profile'),
    path('upload_profile_picture', views.upload_profile_picture, name='upload_profile_picture'),
    path('logout', views.logout, name='logout'),
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)