from django.db import models


class quote(models.Model):
    id = models.AutoField(primary_key=True)
    quote = models.TextField(null=False)
    by = models.CharField(max_length=255, null=False)
    created_date = models.DateTimeField(auto_now_add=True)
