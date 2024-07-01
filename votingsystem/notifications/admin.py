from django.contrib import admin

from notifications.models import *

# Register your models here.
admin.site.register(Notifications)
admin.site.register(Messanger)
admin.site.register(Feedback)