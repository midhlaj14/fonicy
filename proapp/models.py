from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Login(models.Model):
    log_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20)
    password = models.TextField()
    role = models.CharField(max_length=20)
    status = models.IntegerField()
    
    def __str__(s):
        return f'{s.username}'
    
    
    
class Contractor_register(models.Model):
    con_id = models.AutoField(primary_key=True)
    log = models.ForeignKey(Login,on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    company = models.CharField(max_length=50)
    owner_name = models.CharField(max_length=30)
    licence = models.CharField(max_length=40)
    company_address = models.CharField(max_length=150)
    contact_no = models.IntegerField()
    email =  models.CharField(max_length=50)  

    class Meta:
        db_table = 'tb_Contractor_register'



class Category(models.Model):
    ct_id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=80,unique=True)
    def __str__(s):
        return f'{s.ct_id}'  

class Product_type(models.Model):
    tp_id = models.AutoField(primary_key=True)
    ct = models.ForeignKey(Category,on_delete=models.CASCADE)
    product_type = models.CharField(max_length=80)
    stock = models.IntegerField()
    image = models.CharField(max_length=50)
    class Meta:
        db_table = 'tb_Product_type'  

class Type_spec(models.Model):
    ts_id = models.AutoField(primary_key=True)
    tp = models.ForeignKey(Product_type,on_delete=models.CASCADE)
    size = models.IntegerField()
    price = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    def __str__(s):
        return f'{s.ts_id}'  

class Employee_register(models.Model):
    emp_id = models.AutoField(primary_key=True)
    log = models.ForeignKey(Login,on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    image = models.CharField(max_length=50)
    address = models.CharField(max_length=150)
    images = models.CharField(max_length=50)
    designation = models.CharField(max_length=50,blank=True,null=True)
    contact_no = models.BigIntegerField()
    email = models.CharField(max_length=50)    
    def __str__(s):
        return f'{s.name}'  


class Order_product(models.Model):
    or_id = models.AutoField(primary_key=True)
    log = models.ForeignKey(Login,on_delete=models.CASCADE)
 
    tp_id = models.IntegerField()
    date = models.DateField()
    re_date = models.DateField()
    size = models.IntegerField()
    load = models.IntegerField()
    price = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True) 
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    o_type = models.CharField(max_length=20)
    status = models.IntegerField()
    status1 = models.IntegerField()
    class Meta:
        db_table = 'tb_Order_product'  

class Feedback(models.Model):
    fd_id = models.AutoField(primary_key=True)
    log_id = models.IntegerField()
    rec_id = models.IntegerField()
    feedback = models.TextField()
    reply = models.TextField()
    feedback_date = models.DateField()
    def __str__(s):
        return f'{s.fd_id}'  

# Create your models here.


class PasswordReset(models.Model):
    user = models.ForeignKey(Contractor_register,on_delete=models.CASCADE)
    token = models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_now_add=True)

   
    