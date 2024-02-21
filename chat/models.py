from django.db import models
from Repair_App.models import *
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User as AppUser
# import TIME_ZONE
# Create your models here.
# class GroupMessage(models.Model):
#     sender = models.ForeignKey(AppUser, on_delete=models.DO_NOTHING, related_name = 'groupsender_instance')
#     group_name = models.ForeignKey(Standard, on_delete=models.DO_NOTHING)
#     message = models.TextField()
#     datetime = models.DateTimeField(auto_now_add=True)
#     message_file = models.FileField(upload_to='message_files', blank=True, null=True)
#     message_image = models.FileField(upload_to='message_images', blank=True, null=True)
    
#     class meta:
#         ordering=('datetime')
        
#     def __str__(self):
#         return 'Message at'+' '+ str(self.datetime)

class Message(models.Model):
    sender = models.ForeignKey(AppUser, on_delete=models.DO_NOTHING, related_name = 'sender_instance')
    receiver = models.ForeignKey(AppUser, on_delete=models.DO_NOTHING, related_name = 'receiver_instance')
    datetime = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=10000, blank=True, null=True)
    message_file = models.FileField(upload_to='message_files', blank=True, null=True)
    message_image = models.FileField(upload_to='message_images', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_read = models.BooleanField(default=False)
    
    class meta:
        ordering=('datetime')
        
    def __str__(self):
        return 'Message at'+' '+ str(self.datetime)