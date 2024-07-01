from django.shortcuts import render,redirect
from datetime import timedelta
from django.utils import timezone
from datetime import timedelta

from django.contrib.auth.decorators import login_required





from django.contrib import messages
from accounts.models import(
    Commissioners,
    Observer,
    Election,
    Voter,
    Canditats,
    Vote,    

)

from votingsystem.views import(
    generate_otp,
    send_otp_email
)


@login_required(login_url="login_page")
def view_all_valid_elections(request):
    uss = request.user 

    if uss.user_type == "2":
        comm_id = Commissioners.objects.get(users = uss) 
    elif uss.user_type == "4":
        officer = Observer.objects.get(users = uss)
        comm_id = officer.comission_id
    elif uss.user_type == "5":
        voter = Voter.objects.get(users = uss)
        comm_id = voter.comission_id
    

    Elections_status = Election.objects.filter(comission_id= comm_id,status=True)

    for x in Elections_status:
        asia_dhaka = timezone.get_fixed_timezone(360)
        current_time_dhaka = timezone.localtime(timezone.now(), asia_dhaka)
        

        
        if x.Election_Date == current_time_dhaka.date() and  x.elections_start_at <= current_time_dhaka.time() <= x.election_end:              
            x.able_to_vote = True
            x.save()
            
        else:            
            x.able_to_vote = False
            x.save() 
            if x.Election_Date + timedelta(days=1) < current_time_dhaka.date():                
                x.status = False
                x.able_to_vote = False
                x.save()
        
        if x.Election_Date < current_time_dhaka.date() and current_time_dhaka.time() > x.election_end:
            x.se_result_status = True
            x.save()
        

            
    
    if uss.user_type != "1":     
        Elections = Election.objects.filter(comission_id = comm_id, status = True)
    else :
        Elections = Election.objects.filter(status = True)
    
    cp = {
        "Elections":Elections,

    }
        

    return render(request,"authenticate/view_election.html", context=cp)




@login_required(login_url="login_page")
def go_to_my_voting_place(request,id):
    electons = Election.objects.get(id = id)
    canditate = Canditats.objects.filter(election_id = electons, status = True)
    Commissioners = electons.comission_id

    cp = {
        "canditate":canditate,
        "electons":electons,
        "Commissioners":Commissioners,
    }    
    return render(request,"authenticate/view_candidate&voter.html", context=cp)


@login_required(login_url="login_page")
def save_voting_data (request,e_id,can_id):
    users = request.user 
    voter_id = None
    election_id = Election.objects.get(id =e_id)
    Canditate_id = Canditats.objects.get(id = can_id)
    try:
        voter_id = Voter.objects.get(users = users)
    except:
        return redirect("/alarts_shows/You are not a Voter !")


    if Vote.objects.filter(voter_id = voter_id, election_id = election_id).exists():        
        return redirect("/alarts_shows/Already Submit Your Vote !")
    
        
    elif election_id.able_to_vote:
        vote_data = Vote.objects.create(
            voter_id = voter_id,
            election_id = election_id,
            Canditate_id = Canditate_id,
        )
        otp = generate_otp()
        vote_data.otp = otp
        vote_data.save()
        email = voter_id.users.email         
        send_otp_email(email, otp)

        return redirect(f"/verify_otp_vot/{vote_data.id}/")
    
    else:
        return redirect("/alarts_shows/Voting time expird or voteing process not start yet !")
    



@login_required(login_url="login_page")
def apply_for_a_canditates(request, id):
    asia_dhaka = timezone.get_fixed_timezone(360)
    current_time_dhaka = timezone.localtime(timezone.now(), asia_dhaka)
    election_id = None
    try:
        election_id = Election.objects.get(id = id)
    except:
        return redirect("/view_all_valid_elections/") 

    users = request.user
    voter_id = None
    try:
        voter_id = Voter.objects.get(users = users)
    except:
        return redirect("/view_all_valid_elections/")
    
    if users.user_type != "5":
        return redirect("/view_all_valid_elections/")
    elif (current_time_dhaka.date() >= election_id.Election_Date - timedelta(days=1)):
        return redirect("/view_all_valid_elections/")
    elif(not election_id):
        return redirect("/view_all_valid_elections/")
    elif (Canditats.objects.filter(voter_id = voter_id, election_id = election_id)).exists():
        return redirect("/view_all_valid_elections/")



    if request.method == "POST":
        data = request.POST
        mul_niti = data.get("mul_niti")
        if Canditats.objects.filter(election_id = election_id, voter_id = voter_id ).exists():
            messages.info(request, "You already aplyed for this election !")
            return redirect(f"/apply_for_a_canditates/{id}/")
        candidates = Canditats.objects.create(
            voter_id = voter_id,
            election_id = election_id,
            mul_niti = mul_niti,
            
            
        )
        candidates.save()
        messages.info(request, "Successfully Apply for Nomimation! Wait for Athurity Aproval")
        return redirect(f"/apply_for_a_canditates/{id}/")

    return render(request,"authenticate/apply_for_a_canditates.html")


@login_required(login_url="login_page")
def view_election_result(request,id):
    election_id = None
    Candidates_ids = None
    try:
        election_id = Election.objects.get(id = id)
    except:
        return redirect("/alarts_shows/Election id is not Valid!/") 
    
    if (not election_id.se_result_status):
        return redirect("/alarts_shows/Election is not end yet!/")
    try:    
        Candidates_ids = Canditats.objects.filter(election_id = election_id, status = True)
    except:
        return redirect("/alarts_shows/Candidate not Applied yet!/")


    commission_id = election_id.comission_id

    total_vote = Vote.objects.filter(election_id = election_id, is_varified=True).count() 
    if total_vote == 0:
       return redirect("/alarts_shows/People is not voted in the election/")
    rows = Candidates_ids.count()
    bland_array = [[] for _ in range(rows)]  
     

    i = 0
    for entity in Candidates_ids:
        vote_candidates = Vote.objects.filter(election_id = election_id, Canditate_id = entity, is_varified=True ).count()
        persentice = (vote_candidates * 100)/ total_vote
        bland_array[i].append(entity)
        bland_array[i].append(vote_candidates)
        bland_array[i].append(persentice)
        i = i + 1        
        

    cp = {
        "bland_array":bland_array,
        "election_id":election_id,
        "commission_id":commission_id,
    }
    return render(request,"authenticate/view_result.html", context=cp)



