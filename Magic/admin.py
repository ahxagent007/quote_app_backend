from django.contrib import admin
from .models import *

admin.site.register(chat)
admin.site.register(verification)
admin.site.register(last_seen)