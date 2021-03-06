from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import json
from channels import Group

from django.conf import settings
# Create your models here.

class Sticker(models.Model):
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    created_date = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='media')
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class TradeRequest(models.Model):
    users = models.ManyToManyField(User)
    requested_sticker = models.ForeignKey(Sticker, on_delete=models.CASCADE, related_name='requested')
    requested_quantity = models.IntegerField(default = 1)
    given_sticker = models.ForeignKey(Sticker, on_delete=models.CASCADE, related_name='given')
    given_quantity = models.IntegerField(default = 1)
    message = models.TextField(default="Hey, I want to make a trade.")
    accepted = models.BooleanField(default=False)
    given_completed = models.BooleanField(default=False)
    requested_completed = models.BooleanField(default=False)

    def is_valid(self):
        valid = True
        if self.requested_sticker.quantity < self.requested_quantity or self.given_sticker.quantity < self.given_quantity:
            valid = False
        return valid
    


class Room(models.Model):
    """
    A room for people to chat in.
    """
    users = models.ManyToManyField(User)
    active = models.BooleanField(default=False)


    @property
    def websocket_group(self):
        """
        Returns the Channels Group that sockets should subscribe to to get sent
        messages as they are generated.
        """
        return Group("room-%s" % self.id)

    def send_message(self, message):
        """
        Called to send a message to the room on behalf of a user.
        """
        final_msg = {'room': str(self.id), 'message': message.message, 'sender__username': message.sender.username, 'msg_type': message.msg_type}

        # Send out the message to everyone in the room
        self.websocket_group.send(
            {"text": json.dumps(final_msg)}
        )

class Message(models.Model):
    created_date = models.DateTimeField(default=timezone.now)
    message = models.TextField(max_length=500)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    msg_type = models.IntegerField(default = 1)
    def __str__(self):
        return self.message
