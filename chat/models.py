# chat/models.py

from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipient')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id} -> sender:{self.sender}"



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dp = models.ImageField(default = "blank-picture.png", upload_to="profile_pics")
    friends = models.ManyToManyField(User, related_name="+", blank=True)

    def save(self, *args, **kwargs):
        if not self.pk and not self.user_id:
            self.user = User.objects.get(username=self.user)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username
    


class FriendRequest(models.Model):
    
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_friend_requests')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_friend_requests')
    status = models.CharField(max_length=10, choices=[('accepted','Accepted'),('declined','Declined'),('pending','Pending')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('sender', 'recipient') #unique friend reques between sender and recipient