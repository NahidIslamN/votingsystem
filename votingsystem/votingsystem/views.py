from typing import Any
from django.shortcuts import render,redirect
from django.views import generic
from django.contrib.auth import logout,login,authenticate
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
import random
from django.contrib.auth.hashers import check_password

from django.contrib.auth.decorators import login_required


from django.contrib import messages
from accounts.models import(
    CustomUser,
    Commissioners,
    Voter,
    Vote,
    Election,
    Observer,
)

def Homepage(request):
    user = request.user
    total_member = CustomUser.objects.all().count()
    total_representive = CustomUser.objects.filter(user_type = "0", status = "1").count()

    total_voters = None
    total_election = None
    if user.user_type == "1":
        total_voters = Voter.objects.all().count() 
        total_election = Election.objects.all().count()

    elif user.user_type == "2":
        cm_id = Commissioners.objects.get(users = user)
        total_voters = Voter.objects.filter(comission_id = cm_id).count()
        total_election = Election.objects.filter(comission_id = cm_id).count()
    elif user.user_type == "4":
        ob_id = Observer.objects.get(users = user)
        cm_id = ob_id.comission_id
        total_voters = Voter.objects.filter(comission_id = cm_id).count()
        total_election = Election.objects.filter(comission_id = cm_id).count()
    
        
    

    cp = {
        "total_member":total_member,
        "total_voters":total_voters,
        "total_representive":total_representive,
        "total_election":total_election,

    }
    return render(request,"homepage.html", context=cp)

class BasePage(generic.TemplateView):    
    template_name = 'base.html'


class loginpage(generic.TemplateView):
    template_name = "loginpage.html"


        


def logoutfun(request):
    logout(request)
    return redirect("/")



@login_required(login_url="login_page")
def view_my_profile(request):

    return render(request,"authenticate/profile.html")


@login_required(login_url="login_page")
def edite_my_profile(request):
    users = request.user
    if request.method == "POST":
        data = request.POST
        image = request.FILES.get("image")
        if data.get("first_name"):
            users.first_name = data.get("first_name")        
        if data.get("last_name"):
            users.last_name = data.get("last_name")        
        if data.get("username"):
            users.username = data.get("username")        
        if data.get("mobile"):
            users.mobile = data.get("mobile")
        if image:
            users.profile_pic = image        
        messages.info(request, "Profile Update Successfully!")
        users.save() 

    return render(request,"authenticate/edite_my_profile.html")




class base2(generic.TemplateView):
    template_name = "base2.html"



class home_page2(generic.TemplateView):
    template_name = "homepage2.html"


def generate_otp():
    return str(random.randint(100000, 999999))



def send_otp_email(email, otp):
    subject = 'Your E-Voting OTP'
    html_message = render_to_string('email_template.html', {'otp': otp})
    plain_message = strip_tags(html_message)
    send_mail(subject, plain_message, 'nahidislam740405@gmail.com', [email], html_message=html_message)


def generate_and_send_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if CustomUser.objects.filter(email = email).exists():
            otp = generate_otp()
            send_otp_email(email, otp)
            otp_instance, created = CustomUser.objects.get_or_create(email=email)
            otp_instance.otp = otp
            otp_instance.save()
            return redirect(f'/verify_otp/{email}/')
        else:
            messages.info(request,"Invailed Email Address !")
            return redirect("/generate_otp/")
    return render(request, 'generate_otp.html')


def generate_and_send_forgot_pass_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if CustomUser.objects.filter(email = email).exists():
            otp = generate_otp()
            send_otp_email(email, otp)
            otp_instance, created = CustomUser.objects.get_or_create(email=email)
            otp_instance.otp = otp
            otp_instance.save()
            return redirect(f"/verify_otp_forgot_password/{email}")
           
        else:
            messages.info(request,"Invailed Email Address !")
            return redirect("/generate_otp/")
    return render(request, 'generate_otp.html')



def verify_otp_forgot_password(request , email):
    if request.method == 'POST':
        email_adress = email 
        otp_entered = request.POST.get('otp')
        try:
            otp_instance = CustomUser.objects.get(email=email_adress)
            if otp_instance.otp == otp_entered:
                otp_instance.forget_pass_status = True
                otp_instance.save()

                return redirect(f"/forget_my_pass/{email_adress}/")
                
            else:
                # OTP matched, do something here
                messages.info(request,"Failed Veryfied !")
                return redirect("/generate_otp/")
        except CustomUser.DoesNotExist:
            messages.info(request,"invalid email address!")
            return redirect("/generate_otp/")
        
    return render(request,'verify_otp.html')




def forget_my_pass(request,email):
    if request.method == "POST":
        data = request.POST
        password1 = data.get("password1")
        password2 = data.get("password1")

        if password1 == password2:
            try:
                users = CustomUser.objects.get(email = email) 
                if users.forget_pass_status:               
                    users.set_password(password1)
                    users.forget_pass_status = False                    
                    users.save()
                    return redirect("/login_page/")
                else:
                    messages.info(request,"Veryfi your OTP first!")
                    return redirect("/generate_and_send_forgot_pass_otp/")

            except:
                messages.info(request,"invaild email address!")
                return redirect("/generate_and_send_forgot_pass_otp/")
        else:
            messages.info(request,"Password Is not Meched!")
            return redirect("/forget_my_pass/{email}")           
        
        
        
    return render(request,"forget_my_pass.html")








def verify_otp(request , email):
    if request.method == 'POST':
        email_adress = email 
        otp_entered = request.POST.get('otp')
        try:
            otp_instance = CustomUser.objects.get(email=email_adress)
            if otp_instance.otp == otp_entered:
                otp_instance.is_email_verified = True
                otp_instance.save()
                return redirect("/login_page/")
            else:
                # OTP matched, do something here
                messages.info(request,"Failed Veryfied !")
                return redirect("/generate_otp/")
        except CustomUser.DoesNotExist:
            messages.info(request,"Failed Veryfied !")
            return redirect("/generate_otp/")
    return render(request,'verify_otp.html')




def verify_otp_vot(request , id):
    Vote_id = Vote.objects.get(id = id)

    if request.method == "POST":
        otp = request.POST.get("otp")
        if Vote_id.otp == otp:
            Vote_id.is_varified = True
            Vote_id.save()
            return redirect("/alarts_shows/Congratulations Successfully Submit Your Vot !")
        else:
            Vote_id.delete()
            messages.info(request, "Your Varification is failed! Vote again to your favorite canditate!")
            return redirect("/alarts_shows/Worng Varification Code !")
   

   
    

    
    return render(request,'authenticate/veryfi_otp.html')





def regester_as_a_voter(request):
    commiss = Commissioners.objects.all()
    if request.method == "POST":        
        data = request.POST
        image = request.FILES.get("image")        
        if data.get("password1") != data.get("password2"):
            messages.info(request, "Password is not Metched !")
            return redirect("/regester_as_a_voter/")
        if data.get("emai") != data.get("username"):
            messages.info(request, "Emai is not Metched !")
            return redirect("/regester_as_a_voter/")

        elif CustomUser.objects.filter(username = data.get("username")).exists():
            messages.info(request,"UserName already Taken !")
            return redirect("/regester_as_a_voter/")
        elif CustomUser.objects.filter(email = data.get("emai")).exists():
            messages.info(request, "This eamil already taken !")
            return redirect("/regester_as_a_voter/")
        elif Voter.objects.filter(Identifier = data.get("Identifier")).exists():
            messages.info(request,"NID Number Already Exiest !")
            return redirect("/regester_as_a_voter/")
        
        else:
           commiss_id = Commissioners.objects.get(id = data.get("commission_id"))
           urss =  CustomUser.objects.create(
               first_name = data.get("first_name"),
               last_name = data.get("last_name"),
               username = data.get("username"),
               email = data.get("username"),
               user_type = 5,
               mobile = data.get("mobile"),
               profile_pic = image,           

            )
           urss.set_password(data.get("password1"))
           Voter_obj = Voter.objects.create(
                users = urss,
                comission_id = commiss_id,
                Identifier = data.get("Identifier"),
                father_name = data.get("father_name"),
                mother_name = data.get("mother_name"),
           )
           Voter_obj.save()
           urss.save()
           messages.info(request,"Regestraton Successfully Done!")
           return redirect("/generate_otp/")
        
        


    cp = {
        "commiss":commiss
    }
    return render(request, "regester_as_a_voter.html", context=cp)





def alarts_shows(request,text):
    texts = text

    return render(request,"votealarts/already_voted.html", context={"text":texts})


@login_required(login_url="login_page")
def change_my_password(request):
    users = request.user

    if request.method == "POST":
        data = request.POST
        Old_pass = data.get("Old_pass")
        New_pass = data.get("New_pass")
        New_pass2 = data.get("New_pass2")
        if check_password(Old_pass, users.password):
            if New_pass == New_pass2:
                users.set_password(New_pass)
                users.save()
                return redirect("/logoutrout/")
            else:
                return redirect("/logoutrout/")
        else:
            return redirect("/logoutrout/")

    return redirect("/view_my_profile/")


def varify_success(request):
    user = CustomUser.objects.get(id = "1")
    represntives = CustomUser.objects.filter(user_type= "0", is_email_verified = True)
    total_rep = represntives.count()
    if request.method == "POST":
        data = request.POST
        sum = 0
        for x in represntives:
            if sum == total_rep-1 and x.otp == data.get(f"{x.id}") :
                login(request, user)
                return redirect("/homepage/")           
            else:
      
                if x.otp == data.get(f"{x.id}"):
                    sum = sum+1
               
                else:
                    messages.info(request,"verify is not complete!")
                    return redirect("/")

    cp = {
        "represntives" : represntives,
    }
    return render(request,"varifi_otp_admin_when.html", context = cp)



def verify_emails_representative(request):       
    represntives = CustomUser.objects.filter(user_type= "0", is_email_verified = True)
    if represntives is not None:
        for x in represntives:
            email = x.email
            otp = generate_otp()
            x.otp = otp
            x.save()
            send_otp_email(email, otp)
    else:
        return redirect("/logindata/")
    cp = {
        "represntives" : represntives,
    }
    return render(request,"varifi_otp_admin_when.html", context = cp)

class Loginrout(generic.View):
    def post(self,request, *args, **kwrgs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        if CustomUser.objects.filter(username = username).exists():
            user = CustomUser.objects.get(username = username)
            if user.is_email_verified and user.status:
                if authenticate(username = username, password = password):
                    if user.is_superuser and user.user_type == "1":
                        if Election.objects.filter(status=True).exists():
                            # return redirect("/verify_emails_representative/")
                            login(request,user)
                            return redirect('/homepage/')                                                     
                            
                        else:
                            login(request,user)
                            return redirect('/homepage/')
                    else:
                        login(request,user)
                    if user.user_type != "5":
                        return redirect('/homepage/')
                    else:
                        return redirect("/")
                else:
                    messages.info(request,"Worng Password")
                    return redirect("/login_page/")
            else:
                if not user.is_email_verified:
                    return redirect("/generate_otp/")
                else:
                    messages.info(request,"Wait for officer aproval!")
                    return redirect("/login_page/")                
        else:
            messages.info(request,"Worng Candidate")
            return redirect("/login_page/")  






    