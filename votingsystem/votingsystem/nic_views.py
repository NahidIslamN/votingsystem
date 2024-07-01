from django.shortcuts import render,redirect
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.decorators import login_required


from django.contrib import messages
from accounts.models import(
    Commissioners,
    ElectionCategories,
    CustomUser,
    Observer,
    Election,
    Voter
)



def send_message_email(email, message):
    subject = 'E-voting Elections'
    html_message = render_to_string('email_template2.html', {'message': message})
    plain_message = strip_tags(html_message)
    send_mail(subject, plain_message, 'from@example.com', [email], html_message=html_message)


@login_required(login_url="login_page")
def save_election_category_data(request):
    if request.method == "POST":
        data = request.POST
        usrs = request.user
        if usrs.user_type != "2":
            messages.info(request,"You are not Able to add Category data")
            return redirect("/save_election_category_data/")
        else:
            com_id = Commissioners.objects.get(users = usrs)
            election_type = data.get("election_type")
            designation = data.get("designation")
            election_categories = ElectionCategories.objects.create(
                comission_id = com_id,
                election_type = election_type,
                designation = designation
            )
            election_categories.save()
            messages.info(request,"Categories Save Successfully !")
            return redirect("/save_election_category_data/")
    return render(request,"NIC/create_and_Election_category.html")



@login_required(login_url="login_page")
def add_nic_officers(request):
    usr = request.user
    commiss = Commissioners.objects.get(users = usr )
    if request.method == "POST":
        data = request.POST
        image = request.FILES.get("image")        
        if data.get("password1") != data.get("password2"):
            messages.info(request, "Password is not Metched !")
            return redirect("/add_nics_officers/")
 
        elif CustomUser.objects.filter(username = data.get("username")).exists():
            messages.info(request,"UserName already Taken !")
            return redirect("/add_nics_officers/")
        elif CustomUser.objects.filter(email = data.get("emai")).exists():
            messages.info(request, "This eamil already taken !")
            return redirect("/add_nics_officers/")
        elif Observer.objects.filter(Identifier = data.get("Identifier")).exists():
            messages.info(request,"NID Number Already Exiest !")
            return redirect("/add_nics_officers/")
        
        else:
           commiss_id = Commissioners.objects.get(comitionar_ID= data.get("comm_id"))
           urss =  CustomUser.objects.create(
               first_name = data.get("first_name"),
               last_name = data.get("last_name"),
               username = data.get("username"),
               email = data.get("emai"),
               user_type = 4,
               mobile = data.get("mobile"),
               profile_pic = image,   

            )
           urss.set_password(data.get("password1"))

           Officers = Observer.objects.create(
                    users = urss,
                    comission_id = commiss_id,
                    Identifier = data.get("Identifier"),               
           )
           urss.save()
           Officers.save()
           messages.info(request,"Officer created Successfully")
           return redirect("/add_nics_officers/")    

    cp = {
        "commiss":commiss
    }

    return render(request,"NIC/add_nic_officers.html", context=cp)


@login_required(login_url="login_page")
def arrenge_an_election(request):
    users = request.user
    commission_id = None
    election_type = None
    if users.user_type != "2":
        messages.info("You are not able to arrange Election !")
        return redirect("/arrenge_an_election/")
    else:
        commission_id = Commissioners.objects.get(users = users)
        election_type = ElectionCategories.objects.filter(comission_id = commission_id )    
    if request.method =="POST":
        data = request.POST
        election_c_id = ElectionCategories.objects.get(id = data.get("election_type"))
        election = Election.objects.create(
            comission_id = commission_id,
            election_type = election_c_id,
            Election_Date = data.get("electiondate")
        )
        election.save()
        
        voters = Voter.objects.filter(comission_id = commission_id)
        for voter in voters:
            if voter.users.is_email_verified:
                email = voter.users.email
                message = f"{election.election_type.election_type} arrange in {election.Election_Date}, You Can be a Candidate of Next election!"
                send_message_email(email, message)
            else:
                continue

        messages.info(request,"Successfully Added election data !")
        return redirect("/arrenge_an_election/")
    

    cp = {
        "election_type":election_type
    }

    return render(request,"NIC/arrange_electons.html", context=cp)




