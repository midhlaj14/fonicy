from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register([Login,Contractor_register,Category,Product_type,Type_spec,Employee_register,Order_product,Feedback,PasswordReset])
