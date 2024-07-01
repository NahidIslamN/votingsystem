from django.db import models
from datetime import time
import datetime

# Create your models here.

from django.contrib.auth.models import AbstractUser



class CustomUser(AbstractUser):
    USER = (
        (1,"ENIC"),
        (2,"NIC"),
        (3,"Canditats"),
        (4,"Observer"),
        (5,"Voter")
    )
    
    status = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    voter_id = models.PositiveBigIntegerField(null=True, blank=True)
    user_type = models.CharField(choices = USER,max_length=50)
    mobile = models.CharField(max_length=15, null= True, blank=True)
    otp = models.CharField(max_length=10, null= True, blank=True)
    profile_pic = models.ImageField(upload_to="profile_picture")
    forget_pass_status = models.BooleanField(default=False)
    



class Commissioners(models.Model):
    users = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    comitionar_ID = models.CharField(max_length=10,unique=True)
    Zone_Name = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)
    update_ad = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.Zone_Name





class Voter(models.Model):
    users = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    comission_id = models.ForeignKey(Commissioners, on_delete=models.CASCADE)
    Identifier = models.CharField(max_length=50, unique=True)
    father_name = models.CharField(max_length=50)
    mother_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    update_ad = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f" {self.comission_id.Zone_Name} {self.Identifier}"





class Observer(models.Model):
    users = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    comission_id = models.ForeignKey(Commissioners, on_delete=models.CASCADE)
    Identifier = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_ad = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f" {self.comission_id.Zone_Name} {self.Identifier} "





class ElectionCategories(models.Model):
    comission_id = models.ForeignKey(Commissioners, on_delete=models.CASCADE)
    election_type = models.CharField(max_length=50)
    designation = models.CharField(max_length=25)
    if_universe = models.BooleanField(default=False)



class Election(models.Model):
    comission_id = models.ForeignKey(Commissioners, on_delete=models.CASCADE)
    election_type = models.ForeignKey(ElectionCategories, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_ad = models.DateTimeField(auto_now=True)
    Election_Date= models.DateField()
    elections_start_at = models.TimeField(default=datetime.time(8, 0)) 
    election_end = models.TimeField(default=datetime.time(17, 0)) 
    able_to_vote = models.BooleanField(default=False)
    se_result_status = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.comission_id.Zone_Name} {self.election_type.election_type}"






class Canditats(models.Model):
    voter_id = models.ForeignKey(Voter,on_delete=models.CASCADE)
    election_id = models.ForeignKey(Election, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    discription = models.TextField(null=True, blank=True)
    mul_niti = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.election_id.comission_id.Zone_Name} {self.election_id.election_type.election_type}"





class Vote (models.Model):
    voter_id = models.ForeignKey(Voter, on_delete= models.CASCADE)
    election_id = models.ForeignKey(Election, on_delete=models.CASCADE)
    Canditate_id = models.ForeignKey(Canditats, on_delete=models.CASCADE)
    is_varified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, null=True, blank=True)
    def __str__(self):
        return f"{self.election_id.election_type.designation} {self.election_id.comission_id.Zone_Name}"
    

    





    




