from django.db import models
from accounts.models import CustomUser, Commissioners
from django.utils import timezone

asia_dhaka = timezone.get_fixed_timezone(360)
current_time_dhaka = timezone.localtime(timezone.now(), asia_dhaka)




class Notifications(models.Model):
    users = models.ForeignKey(Commissioners, on_delete= models.CASCADE)
    Notifications_text = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    expird_date = models.DateField(null=True, blank=True)
    update = models.DateTimeField(auto_now=True)


class Messanger(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete= models.CASCADE)
    reciver = models.ForeignKey(CustomUser, related_name='reciver', on_delete=models.CASCADE)
    message_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)



class Feedback(models.Model):
    users = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    feetback_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    
