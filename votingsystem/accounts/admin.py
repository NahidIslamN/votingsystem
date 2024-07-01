from django.contrib import admin
from accounts.models import (
    CustomUser,
    Commissioners,
    Voter,
    Observer,
    ElectionCategories,
    Election,
    Canditats,
    Vote,
)

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Commissioners)
admin.site.register(Voter)
admin.site.register(Observer)
admin.site.register(ElectionCategories)
admin.site.register(Election)
admin.site.register(Canditats)
admin.site.register(Vote)

