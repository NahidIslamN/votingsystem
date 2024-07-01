from django.shortcuts import render,redirect
from django.views import generic
from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from accounts.models import(
    CustomUser,
    Commissioners,

)


@login_required(login_url="login_page")
def Save_Commissioner_Data(request):
    if request.method == "POST":
        user = request.user
        data = request.POST
        image = request.FILES.get("image")

        if user.user_type != "1":
            messages.info(request, "You are not able to add Data !")
            return redirect("/save_commissioner_data/")
        
        elif data.get("password1") != data.get("password2"):
            messages.info(request, "Password is not Metched !")
            return redirect("/save_commissioner_data/")
        
        elif CustomUser.objects.filter(username = data.get("username")).exists():
            messages.info(request,"username already taken!")
            return redirect("/save_commissioner_data/")
        
        elif Commissioners.objects.filter(comitionar_ID = data.get("com_id")).exists():
            messages.info(request,"Commissioner ID already Taken")
            return redirect("/save_commissioner_data/")
        elif CustomUser.objects.filter(username = data.get("username")).exists():
            messages.info(request,"UserName already Taken !")
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
               user_type = 2,
               mobile = data.get("mobile"),
               profile_pic = image,           

            )
           urss.set_password(data.get("password1"))

           comm = Commissioners.objects.create(
               users = urss,
               comitionar_ID = data.get("com_id"),
               Zone_Name=  data.get("com_area"),

           )

           urss.save()
           comm.save()
           messages.info(request, "Commmissioner Created Successfully")
           return redirect("/save_commissioner_data/")
            


    

    return render(request,"ENIC/add_commissioner.html")