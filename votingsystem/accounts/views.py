from django.shortcuts import render, redirect
from accounts.models import*
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from votingsystem.decorators import *

# Create your views here.

@login_required(login_url="login_page")
@specific_user_required(user_id=1)
def add_a_representative(request):
    user = request.user
    if (not user.is_superuser) and (user.user_type != "1"):
        return redirect("/alarts_shows/You are not a representative or admin!/")
    elif request.method == "POST":
        if request.method == "POST":
            user = request.user
            data = request.POST
            # print(data)
            image = request.FILES.get("image")

            if data.get("password1") != data.get("password2"):
                messages.info(request, "Password is not Metched !")
                return redirect("/save_commissioner_data/")
            
            elif CustomUser.objects.filter(username = data.get("username")).exists():
                messages.info(request,"username already taken!")
                return redirect("/save_commissioner_data/")

            elif CustomUser.objects.filter(email = data.get("emai")).exists():
                messages.info(request, "This eamil already taken !")
                return redirect("/save_commissioner_data/")
            
            else:
                urss =  CustomUser.objects.create(
                    first_name = data.get("first_name"),
                    last_name = data.get("last_name"),
                    username = data.get("username"),
                    email = data.get("emai"),
                    user_type = 0,
                    is_superuser = True,
                    mobile = data.get("mobile"),
                    profile_pic = image,
                    status = True,           

                    )
                urss.set_password(data.get("password1"))
                urss.save()
                messages.info(request,"Representatives Added Successfully!")
                

    else:
        pass

        
    
    return render(request, "ENIC/add_representative.html")
        



