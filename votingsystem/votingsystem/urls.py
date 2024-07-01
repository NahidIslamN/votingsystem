"""
URL configuration for votingsystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from votingsystem.views import *
from votingsystem.no_views import *
from votingsystem.all_user_views import *

from votingsystem.enic_views import *
from votingsystem.nic_views import *

from accounts.views import *

urlpatterns = [
    path("", home_page2.as_view(), name="home_page2"),
    path("base2/",base2.as_view(),name="base2"),
    path('homepage/',Homepage,name="homepage"),
    path('logoutrout/',logoutfun, name="logoutrout"),
    path('login_page/',loginpage.as_view(),name="login_page"),
    path('logindata/',Loginrout.as_view(),name="logindata"),
    path('basepage/', BasePage.as_view(), name="basepage"),
    path('admin/', admin.site.urls),
    path("view_my_profile/", view_my_profile, name="view_my_profile"),
    path("edite_my_profile/", edite_my_profile, name ="edite_my_profile"),
    path("regester_as_a_voter/",regester_as_a_voter, name = "regester_as_a_voter"),
    path("change_my_password/", change_my_password, name="change_my_password"),
    path("generate_and_send_forgot_pass_otp/", generate_and_send_forgot_pass_otp, name="generate_and_send_forgot_pass_otp"),
    path("verify_otp_forgot_password/<email>/", verify_otp_forgot_password, name="verify_otp_forgot_password"),
    path("forget_my_pass/<email>/", forget_my_pass, name = "forget_my_pass"),
    path("verify_emails_representative/", verify_emails_representative, name = "verify_emails_representative"),
    path("varify_success/", varify_success, name="varify_success"),

    #all user Urls
    path("view_all_valid_elections/",view_all_valid_elections, name = "view_all_valid_elections"),
    path("go_to_my_voting_place/<id>/", go_to_my_voting_place, name="go_to_my_voting_place"),
    path("apply_for_a_canditates/<id>/", apply_for_a_canditates, name= "apply_for_a_canditates"),
    path("view_election_result/<id>/", view_election_result, name="view_election_result"),
    

    #NIC Urls Data
    path("add_nics_officers/",add_nic_officers, name = "add_nic_officers"),
    path("save_election_category_data/",save_election_category_data, name = "save_election_category_data"),
    path("arrenge_an_election/", arrenge_an_election, name="arrenge_an_election"),



    #ENIC Urls
    path("save_commissioner_data/",Save_Commissioner_Data, name ="save_commissioner_data"),
    path("add_a_representative/", add_a_representative, name = "add_a_representative"),


    #NO Urls
    path("none_aproval_candidate/", none_aproval_candidate, name="none_aproval_candidate"),
    path("view_none_aproval_and_aproval_candidates_no/<id>/<choice>/", view_none_aproval_and_aproval_candidates_no, name="view_none_aproval_and_aproval_candidates_no"),
    path("aprove_or_denied_candidate/<id>/<choice>/", aprove_or_denied_candidate, name="aprove_or_denied_candidate"),
    path("none_aproval_voters/", none_aproval_voters, name="none_aproval_voters"),
    path("aprove_or_denied_voter/<id>/<choice>/", aprove_or_denied_voter, name ="aprove_or_denied_voter"),
    path("all_activate_voters/", all_activate_voters, name = "all_activate_voters"),
    



    # Give Voting urls
    path("save_voting_data/<e_id>/<can_id>/",save_voting_data, name= "save_voting_data"),
    path("verify_otp_vot/<id>/", verify_otp_vot, name="verify_otp_vot"),
    path("alarts_shows/<str:text>/",alarts_shows, name = "alarts_shows"),






    #User Email Varifications
    path ("generate_otp/", generate_and_send_otp, name = "generate_otp"),
    path("verify_otp/<email>/",verify_otp, name ="verify_otp")
    
]

if settings.DEBUG:
       
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
