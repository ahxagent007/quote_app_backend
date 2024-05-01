from django.db import models

class image(models.Model):
    id = models.AutoField(primary_key=True)
    image_path = models.CharField(max_length=255, null=False)
    sender_id = models.IntegerField(null=False)
    created_date = models.DateTimeField(auto_now_add=True)


class chat(models.Model):
    id = models.AutoField(primary_key=True)
    message = models.TextField()
    sender = models.IntegerField(null=False)
    receiver = models.IntegerField(null=False)
    created_time = models.DateTimeField(auto_now_add=True)
    chat_room_id = models.CharField(null=False, max_length=255)
    images = models.ManyToManyField(image, null=True)


class verification(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.IntegerField(null=False, unique=True)
    passcode = models.CharField(max_length=255)

class last_seen(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.IntegerField(null=False, unique=True)
    last_time = models.DateTimeField(auto_now=True, null=True)

class report(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.IntegerField(null=False, unique=True)
    report_message = models.CharField(max_length=1000)
    created_date = models.DateTimeField(auto_now=True, null=True)