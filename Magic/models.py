from django.db import models

class chat(models.Model):
    id = models.AutoField(primary_key=True)
    message = models.TextField()
    sender = models.IntegerField(null=False)
    receiver = models.IntegerField(null=False)
    created_time = models.DateTimeField(auto_now_add=True)
    chat_room_id = models.CharField(null=False, max_length=255)

class verification(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.IntegerField(null=False, unique=True)
    passcode = models.CharField(max_length=255)
