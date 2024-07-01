from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required


from django.contrib import messages
from accounts.models import(
    CustomUser,
    Observer,
    Election,
    Voter,
    Canditats
)
from votingsystem.nic_views import send_message_email

@login_required(login_url="login_page")
def none_aproval_candidate(request):
    user = request.user
    if user.user_type != "4":
        return redirect("/")
    
    users = request.user
    comission_id = None
    if users.user_type != "4":
        messages.info(request, "You can't Access this Data !")
    else:
        observer_id = Observer.objects.get(users = users)
        comission_id =observer_id.comission_id
    elections = Election.objects.filter(status = True, comission_id = comission_id).order_by("-created_at")
    cp = {
        "elections":elections,
    }
    return render(request, "NO/none_aproval_candidate.html", context=cp)





@login_required(login_url="login_page")
def view_none_aproval_and_aproval_candidates_no(request,id,choice):
    user = request.user
    if user.user_type != "4":
        return redirect("/")
    
    candidates_id = None
    try:
        election_id = Election.objects.get(id = id)
    except:
        return redirect("/homepage/")

    if choice == "1":
        candidates_id = Canditats.objects.filter(election_id=election_id, status=True)
    elif choice == "0":
        candidates_id = Canditats.objects.filter(election_id=election_id, status=False)
    else:
        return redirect("/homepage/")
    cp = {
        "choice":choice,
        "candidates_id":candidates_id
    }
    return render(request,"NO/view_none_aproval_candidates.html", context=cp)



@login_required(login_url="login_page")
def aprove_or_denied_candidate(request, id, choice):
    user = request.user
    if user.user_type != "4":
        return redirect("/")
    
    candidates_id = None
    try:
        candidates_id = Canditats.objects.get(id = id)
    except:
        return redirect("/")

    if choice == "0":
        candidates_id.delete()
        candidates_id.save()
        return redirect("/none_aproval_candidate/")
    
    elif choice == "1":
        candidates_id.status = True
        candidates_id.save()
        email = candidates_id.voter_id.users.email
        send_message_email(email, "E-Voting Aproved your Appication for Candidates")
        return redirect("/none_aproval_candidate/")
    

    return redirect("/none_aproval_candidate/")




@login_required(login_url="login_page")
def none_aproval_voters(request):
    user = request.user
    if user.user_type != "4":
        return redirect("/")
    
    users = request.user
    observer_d = Observer.objects.get(users = user)
    commisson_id = observer_d.comission_id


    voters = Voter.objects.filter(comission_id = commisson_id )

    none_aproval_voter = []

    for x in voters:
        if x.users.status == False:
            none_aproval_voter.append(x) 
        
    cp = {
        "voters":none_aproval_voter,
        
    }
    return render(request, "NO/none_aproval_voter.html", context=cp)






@login_required(login_url="login_page")
def aprove_or_denied_voter(request,id,choice):
    user = CustomUser.objects.get(id = id)

    uss = request.user
    if uss.user_type !="4":
        return redirect("/")

    if choice == "0":
        user.delete()
        
    elif choice == "1":
        user.status = True
        user.save()
    elif choice == "3":
        user.status = False
        user.save()
        return redirect("/all_activate_voters/")

    return redirect("/none_aproval_voters/")




@login_required(login_url="login_page")
def all_activate_voters(request):
    user = request.user
    if user.user_type != "4":
        return redirect("/")
    
    users = request.user
    observer_d = Observer.objects.get(users = user)
    commisson_id = observer_d.comission_id


    voters = Voter.objects.filter(comission_id = commisson_id )

    all_activate_voter = []

    for x in voters:
        if x.users.status == True:
            all_activate_voter.append(x) 
        
    cp = {
        "voters":all_activate_voter,
        
    }
    return render(request, "NO/all_activate_voters.html", context=cp)
