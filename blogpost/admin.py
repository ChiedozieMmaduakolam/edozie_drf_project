from django.contrib import admin
from .models import CustomUser
from bankapp.models import BankDetails
# Register your models here.


admin.site.register(CustomUser)
admin.site.register(BankDetails)