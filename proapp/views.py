from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.hashers import make_password
from .models import *
from django.contrib import messages
from django.db import connection
cursor = connection.cursor()
from django.contrib.auth import logout
from django.core.files.storage import FileSystemStorage

from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.db.models import Q
import datetime


def home(request):
    if 'user' in request.session:
        user = request.session['user']
        data = Login.objects.get(username=user)
        if data.role == 'admin':
            return render(request,'master/home.html')
        elif data.role == 'contractor':
            return redirect('/contractor_home')
        elif data.role == 'employee':
            return render(request, 'employee/home.html')
        else:
            return redirect('/home')
    else:
        return render(request,'home.html')
    


def login(request):
    if request.method == 'POST':
        use = request.POST['use']
        pas = request.POST['pas']
        try:
            data = Login.objects.get(username=use,password= pas)
            if data.status == 1:
                request.session['user'] = use
                request.session['log_id'] = data.log_id
                return redirect('/home')
            else:
                messages.success(request, 'Admin Approval required...')
                return redirect(login)
        except Exception:
            messages.success(request, 'Invalid Username Or Password...')
            return redirect(login)
    else:
        return render(request,'login.html')
    
def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')


#-----------------Master-------------------
def category(request):
    if 'user' in request.session:
        if request.method == 'POST':
            cat = request.POST['n1']
            
            if Category.objects.filter(category=cat).exists():
                messages.error(request, 'Category already taken.')
                return redirect('/category')
            else:
                Category.objects.create(category=cat).save()
                messages.success(request,'Category added successfully.....')
                return redirect('/category')
        else:
            d = Category.objects.all()
            return render(request,'master/product_category.html',{'data':d})
    else:
        return redirect('/home')

    
def up_category(request,ct_id):
    if 'user' in request.session:
        data=Category.objects.filter(ct_id=ct_id)
        return render(request,'master/up_category.html',{'data':data})
    else:
        return redirect('/home')
    
def update_category(request):
    if 'user' in request.session:
        if request.method == 'POST':
            id = request.POST['n1']
            cat = request.POST['n2']
            Category.objects.filter(ct_id=id).update(category=cat)
            messages.success(request, 'Updated successfully.....')
            return redirect('/category')
        else: 
            return redirect('/category')
    else:
        return redirect('/home')
    
def del_category(request,ct_id):
    if 'user' in request.session:
        data  = Category.objects.get(ct_id=ct_id)
        data.delete()
        messages.success(request, 'Category deleted successfully.....')
        return redirect ('/category')
    else:
        return redirect('/home')
    

   

def product_type(request):
    if 'user' in request.session:
        if request.method == 'POST':
            ct_id = request.POST['n1']
            p_type =  request.POST['n2']
            n4 = request.FILES['n4']

            obj = FileSystemStorage()
            fl = obj.save(n4.name,n4)
            img = obj.url(fl)

            Product_type.objects.create(ct_id=ct_id,product_type=p_type,stock=0,image=img)
            messages.success(request,'Product type added successfully.....')
            return redirect('/product_type')
        else:
            d = Category.objects.all()
            d2 = Product_type.objects.all().select_related('ct')
            return render(request,'master/product_type.html', {'data':d,'data2':d2})
    else:
        return redirect('/home')
    
def up_type(request,tp_id):
    if 'user' in request.session:
        data = Product_type.objects.filter(tp_id=tp_id).select_related('ct')
        data2 = Category.objects.all()
        return render(request,'master/up_type.html', {'data':data,'data2':data2})
    else:
        return redirect('/home')
    
def update_type(request):
    if 'user' in request.session:
        if request.method == 'POST':
            ct_id = request.POST['n1']
            p_type = request.POST['n2']
            tp_id = request.POST['tp_id']
            if len(request.FILES) == 0:

                Product_type.objects.filter(tp_id=tp_id).update(ct_id=ct_id,product_type=p_type)
                messages.success(request, 'Updated successfully.....')
                return redirect('/product_type')
            else:
                n4 = request.FILES['n4']
                obj = FileSystemStorage()
                fl = obj.save(n4.name,n4)
                img = obj.url(fl)

                Product_type.objects.filter(tp_id=tp_id).update(ct_id=ct_id,product_type=p_type,image=img)
                messages.success(request,'Updated successfully.....')
                return redirect('/product_type')
        else:
            return redirect('/product_type')
    else:
        return redirect('/home')
    
def del_type(request,tp_id):
    if 'user' in request.session:
        data  = Product_type.objects.get(tp_id=tp_id)
        data.delete()
        messages.success(request, 'Deleted successfully.....')
        return redirect ('/product_type')
    else:
        return redirect('/home')
    
def types(request):
    d = Product_type.objects.all()

    return render(request,'master/products.html',{'data':d})
    

def type_spec(request):
    if 'user' in request.session:
        if request.method == 'POST':
            tp_id = request.POST['n1']
            siz =  request.POST['n2']
            pri = request.POST['n3']

            Type_spec.objects.create(tp_id=tp_id,size=siz,price=pri)
            messages.success(request,'Added successfully.....')
            return redirect('/type_spec')
        else:
            d = Product_type.objects.all()
            d2 = Type_spec.objects.all().select_related('tp')
            return render(request,'master/product_price.html',{'data':d,'data2':d2})
    else:
        return redirect('/home')
    
def up_spec(request,ts_id):
    if 'user' in request.session:
        data = Type_spec.objects.filter(ts_id=ts_id).select_related('tp')
        data2 = Product_type.objects.all()
        return render(request,'master/update_price.html',{'data':data,'data2':data2})
    else:
        return redirect('/home')
    
def update_spec(request):
    if 'user' in request.session:
        if request.method == 'POST':
            ts_id = request.POST['n1']
            tp_id = request.POST['n2']
            siz = request.POST['n3']
            pri = request.POST['n4']

            Type_spec.objects.filter(ts_id=ts_id).update(tp_id=tp_id,size=siz,price=pri)
            messages.success(request, 'Updated successfully.....')
            return redirect('/type_spec')
        else:
            return redirect('/type_spec')
    else:
        return redirect('/home')
    
def del_spec(request,ts_id):
    if 'user' in request.session:
        data  = Type_spec.objects.get(ts_id=ts_id)
        data.delete()
        messages.success(request, 'Deleted successfully.....')
        return redirect ('/type_spec')
    else:
        return redirect('/home')
    


def emp_register(request):
    if request.method == 'POST':
        nam = request.POST['n1']
        n2 = request.FILES['n2']

        obj = FileSystemStorage()
        fl = obj.save(n2.name,n2)
        img = obj.url(fl)

     

        add = request.POST['n3']
        n10 = request.FILES['n10']

        obj = FileSystemStorage()
        fl = obj.save(n10.name,n10)
        imgs = obj.url(fl)
        
        con = request.POST['n4']
        ema = request.POST['n5']
        use = request.POST['n6']
        desi = request.POST['n9']

        pas =  request.POST['n7']

        Login.objects.create(username=use,password=pas,role='employee',status=0)
        d = Login.objects.get(username=use)

        Employee_register.objects.create(name=nam,image=img,address=add,images=imgs,contact_no=con,designation=desi,email=ema,log_id=d.log_id)
        messages.success(request, 'Registered successfully.....')
        return redirect('/emp_register')
    else:
        return render(request,'emp_register.html')

def view_employee(request):
    if 'user' in request.session:
        data  = Employee_register.objects.all().select_related('log')
        return render (request,'master/view_employee.html',{'data':data})
    else:
        return redirect('/home')
    
def approve_employee(request,log_id):
    if 'user' in request.session:
        Login.objects.filter(log_id=log_id).update(status=1)
        return redirect('/view_employee')
    else:
        return redirect('/home')

def del_emp(request,log_id):
    if 'user' in request.session:
        data  = Login.objects.get(log_id=log_id)
        data.delete()
        messages.success(request, 'Employee deleted successfully.....')
        return redirect ('/view_employee')
    else:
        return redirect('/home')
    
def view_contractor(request):
    if 'user' in request.session:
        data  = Contractor_register.objects.all().select_related('log')
        return render (request,'master/view_contractor.html',{'data':data})
    else:
        return redirect('/home')
    
def approve_contractor(request,log_id):
    if 'user' in request.session:
        Login.objects.filter(log_id=log_id).update(status=1)
        return redirect('/view_contractor')
    else:
        return redirect('/home')
    
def del_contractor(request,log_id):
    if 'user' in request.session:
        data  = Login.objects.get(log_id=log_id)
        data.delete()
        messages.success(request, 'Deleted successfully.....')
        return redirect ('/view_contractor')
    else:
        return redirect('/home')


def buy_view(request):
    if 'log_id' in request.session:
        data = Order_product.objects.all()
   
        return render(request,'master/buy_view.html',{'data':data})
    else:
        return redirect('/home')
    
def delivered1(request):
    if 'log_id' in request.session:
        data = Order_product.objects.filter(status=1)
   
        return render(request, 'master/deliverd1.html', {'data': data})
    else:
        return redirect('/home')
    
def notdelivered1(request):
    if 'log_id' in request.session:
        dat = Order_product.objects.filter(status=0)
        data=[]
        for i in dat:

            
            d1 = i.re_date
          
            d2 = datetime.datetime.now()
            d2=d2.date()
            diff=d1-d2
          
            data.append({'or_id': i.or_id,'log':i.log, 'tp_id':i.tp_id,'date':i.date,'re_date':i.re_date,'size':i.size,'price':i.price,'load':i.load,'amount':i.amount,'status':i.status,'diff':diff.days})
   
        return render(request, 'master/notdeliverd1.html', {'data': data})
    else:
        return redirect('/home')



def ad_profile(request):
    if 'log_id' in request.session:
        log_id = request.session['log_id']
        if request.method == 'POST':
            logid = request.POST['n1']
            opas = request.POST['n2']
            npas = request.POST['n3']
            try:
                data = Login.objects.get(log_id=logid)
                if data.password == opas:
                    Login.objects.filter(log_id=logid).update(password=npas)
                    messages.success(request, 'Your Password has been Reset successfully.....')
                    return redirect('/ad_profile')
                else:
                    messages.success(request, 'Enter valid current password....!')
                    return redirect('/ad_profile')
            except Exception:
                messages.success(request, 'Invalid User.....')
                return redirect('/ad_profile')
        else:
            data = Login.objects.filter(log_id=log_id)
            return render(request,'master/profile.html',{'data':data})
    else:
        return redirect('/login')



    

#------------------Employee-------------------
def stock1(request):
    d = Product_type.objects.all()

    
    return render(request,'employee/stock1.html',{'data':d})

def add_stock(request):
    if 'user' in request.session:
        data = Product_type.objects.all().select_related('ct')
        return render(request,'employee/add_stock.html',{'data':data})
    else:
        return redirect('/home')

def up_stock(request,tp_id):
    if 'user' in request.session:
        data=Product_type.objects.filter(tp_id=tp_id)
        return render(request,'employee/update_stock.html',{'data':data})
    else:
        return redirect('/home')
    
def update_stock(request):
    if 'user' in request.session:
        if request.method == 'POST':
            tp_id = request.POST['tp_id']
            sto = request.POST['sto']
            Product_type.objects.filter(tp_id=tp_id).update(stock=sto)
            # messages.success(request, 'Stock Updated successfully.....')
            return redirect('/add_stock')
        else: 
            return redirect('/add_stock')
    else:
        return redirect('/home')
    

   
def buy_details(request):
    if 'log_id' in request.session:
        dat = Order_product.objects.all()
        
        data=[]
        for i in dat:

            
            d1 = i.re_date
          
            d2 = datetime.datetime.now()
            d2=d2.date()
            diff=d1-d2
          
            data.append({'or_id': i.or_id,'log':i.log, 'tp_id':i.tp_id,'date':i.date,'re_date':i.re_date,'size':i.size,'price':i.price,'load':i.load,'amount':i.amount,'status':i.status,'diff':diff.days})
       
        return render(request, 'employee/buy_details.html', {'data': data})
    else:
        return redirect('/home')
    
# def buy_details(request):
#     if 'log_id' in request.session:
        
#         cursor.execute("select c.name,c.company,tp.product_type,o.date,o.re_date,o.size,o.price,o.load,o.amount,o.status,o.or_id from tb_product_type as tp inner join tb_order_product as o on o.tp_id=tp.tp_id inner join tb_contractor_register as c on c.log_id=o.log_id where o.o_type='buy'")
#         data = cursor.fetchall()
        
#         return render(request,'employee/buy_details.html',{'data':data})
#     else:
#         return redirect('/home')
    
def delivered(request):
    if 'log_id' in request.session:
        data = Order_product.objects.filter(status=1)
   
        return render(request, 'employee/delivered.html', {'data': data})
    else:
        return redirect('/home')
    
def notdelivered(request):
    if 'log_id' in request.session:
        dat = Order_product.objects.filter(status=0)
        data=[]
        for i in dat:

            
            d1 = i.re_date
          
            d2 = datetime.datetime.now()
            d2=d2.date()
            diff=d1-d2
          
            data.append({'or_id': i.or_id,'log':i.log, 'tp_id':i.tp_id,'date':i.date,'re_date':i.re_date,'size':i.size,'price':i.price,'load':i.load,'amount':i.amount,'status':i.status,'status1':i.status1,'diff':diff.days})
   
        return render(request, 'employee/notdelivered.html', {'data': data})
    else:
        return redirect('/home')


   


def deliver(request,or_id):
    if 'user' in request.session:
        Order_product.objects.filter(or_id=or_id).update(status=1)
        # messages.success(request)
        return redirect('/home')
    else:
        return redirect('/home')
    
def order_picked(request,or_id):
    if 'user' in request.session:
        Order_product.objects.filter(or_id=or_id).update(status=1)
        # messages.success(request)
        return redirect('/home')
    else:
        return redirect('/home')

    
def emp_profile(request):
    if 'log_id' in request.session:
        log_id = request.session['log_id']
        if request.method == 'POST':
            logid = request.POST['logid']
            nam = request.POST['n1']
            add = request.POST['n3']
            cno = request.POST['n4']
            ema = request.POST['n5']

            if len(request.FILES) == 0:
                Employee_register.objects.filter(log_id=logid).update(name=nam,address=add,contact_no=cno,email=ema)
                messages.success(request, 'Updated successfully.....')
                return redirect('/emp_profile')
            else:
                n2 = request.FILES['n2']
                obj = FileSystemStorage()
                fl = obj.save(n2.name,n2)
                img = obj.url(fl)

                Employee_register.objects.filter(log_id=logid).update(name=nam,address=add,contact_no=cno,email=ema,image=img)
                messages.success(request, 'Updated successfully.....')
                return redirect('/emp_profile')
        else:
            data = Employee_register.objects.filter(log_id=log_id)
            return render(request,'employee/profile.html',{'data':data})
    else:
        return redirect('/home')

def reset_emp(request):
    if 'log_id' in request.session:
        log_id = request.session['log_id']
        if request.method == 'POST':
            logid = request.POST['logid']
            opas = request.POST['opas']
            npas = request.POST['npas']
            try:
                data = Login.objects.get(log_id=logid)
                if data.password == opas:
                    Login.objects.filter(log_id=logid).update(password=npas)
                    messages.success(request, 'Your Password has been Reset successfully.....')
                    return redirect('/emp_profile')
                else:
                    messages.success(request, 'Enter valid current password....!')
                    return redirect('/reset_emp')
            except Exception:
                messages.success(request, 'Invalid User.....')
                return redirect('/reset_emp')
        else:
            data = Login.objects.filter(log_id=log_id)
            return render(request,'employee/reset_emp.html',{'data':data})
    else:
        return redirect('/home')  


#------------------contractor------------------


def contractor_reg(request):
    if request.method == 'POST':
        nam = request.POST['n1']
        cnam = request.POST['n2']
        onam = request.POST['n3']

        n4 = request.FILES['n4']

        obj = FileSystemStorage()
        fl = obj.save(n4.name,n4)
        lic = obj.url(fl)

        cadd = request.POST['n5']
        con = request.POST['n6']
        ema = request.POST['n7']
        use = request.POST['n8']
        pas =  request.POST['n9']

        # Check if username already exists
        if Login.objects.filter(username=use).exists():
            messages.error(request, 'Username already taken.')
            return redirect('/contractor_reg')

    

        # Create a new Login object
        login_obj = Login(username=use, password=pas, role='contractor', status=0)
        login_obj.save()

        # Create a new Contractor_register object
        contractor_obj = Contractor_register(name=nam,company=cnam,owner_name=onam,licence=lic,company_address=cadd,contact_no=con,email=ema,log_id=login_obj.log_id)
        contractor_obj.save()

        messages.success(request, 'Registered successfully.....')
        return redirect('/contractor_reg')
    else:
        return render(request, 'contractor_reg.html')
    
def contractor_home(request):
    if 'user' in request.session:
        data = Product_type.objects.all().select_related('ct')
        return render(request,'contractor/home.html',{'data':data})
    else:
        return redirect('/home')


def buy(request,tp_id):
    if 'user' in request.session:
        data  = Product_type.objects.filter(tp_id=tp_id)
        data2  = Type_spec.objects.filter(tp_id=tp_id)
        return render(request,'contractor/buy_product.html',{'data':data,'data2':data2})
    else:
        return redirect('/home')

def payment_done(request):
    return render(request,'contractor/payment_done.html')

def buy_product(request):
    if 'user' in request.session:
        if request.method == 'POST':
            tp_id = request.POST['tp_id']
            size = request.POST['size']
            data  = Product_type.objects.filter(tp_id=tp_id)
            data2 = Type_spec.objects.filter(tp_id=tp_id,size=size)
            return render(request,'contractor/buy_now.html',{'data':data,'data2':data2})
        else:
            return redirect('/home')
    else:
        return redirect('/home')
    
def buy_now(request):
    if 'log_id' in request.session:
        log_id = request.session['log_id']
        if request.method == 'POST':
            tp_id = request.POST['tp_id']
            from datetime import date
            dt = date.today()
            rdt = request.POST['rdt']
            size = request.POST['size']
            load = request.POST['lod']
            pri = request.POST['price']
            amt = request.POST['amnt']

            s = int(load)*int(size)
            d=Product_type.objects.get(tp_id=tp_id)
            sub = d.stock-s
            
            Product_type.objects.filter(tp_id=tp_id).update(stock=sub)
            Order_product.objects.create(log_id=log_id,tp_id=tp_id,date=dt,re_date=rdt,size=size,load=load,price=pri,amount=amt,o_type='buy',status=0)
            # messages.success(request, 'Ordered successfully.....')

            return redirect('/payment_done')
        else:
            return redirect('/home')
    else:
        return redirect('/home')  

# def view_buy(request):
#     if 'log_id' in request.session:
#         v=request.session['log_id']   
#         print(v,type(v))
#         login=Login.objects.get(log_id=v)
#         print(login.username)
#         con=Contractor_register.objects.get(log=login)
#         print(con)

#         data = Order_product.objects.filter(company=con.con_id)
#         print(data)
#         # data='  '
       
#         return render(request,'contractor/view_buy.html',{'data':data})
#     else:
#         return redirect('/home')



def view_buy(request):
    if 'log_id' in request.session:
        log_id = request.session['log_id']
        cursor.execute("select c.name,c.company,tp.product_type,o.date,o.re_date,o.size,o.price,o.load,o.amount,o.status from tb_product_type as tp inner join tb_order_product as o on o.tp_id=tp.tp_id inner join tb_contractor_register as c on c.log_id=o.log_id where o.o_type='buy' and c.log_id="+str(log_id))
        data = cursor.fetchall()
        return render(request,'contractor/view_buy.html',{'data':data})
    else:
        return redirect('/home')



def contractor_profile(request):
    if 'log_id' in request.session:
        log_id = request.session['log_id']
        if request.method == 'POST':
            logid = request.POST['n7']
            nam = request.POST['n1']
            cnam = request.POST['n2']
            onam = request.POST['n3']
            add = request.POST['n4']
            cno = request.POST['n5']
            ema = request.POST['n6']

            Contractor_register.objects.filter(log_id=logid).update(name=nam,company=cnam,owner_name=onam,company_address=add,contact_no=cno,email=ema)
            return redirect('/contractor_profile')
        else:
            data = Contractor_register.objects.filter(log_id=log_id)
            return render(request,'contractor/profile.html',{'data':data})
    else:
        return redirect('/home')

def reset_con(request):
    if 'log_id' in request.session:
        log_id = request.session['log_id']
        if request.method == 'POST':
            logid = request.POST['logid']
            opas = request.POST['opas']
            npas = request.POST['npas']
            try:
                data = Login.objects.get(log_id=logid)
                if data.password == opas:
                    Login.objects.filter(log_id=logid).update(password=npas)
                    messages.success(request, 'Your Password has been Reset successfully.....')
                    return redirect('/contractor_profile')
                else:
                    messages.success(request, 'Enter valid current password....!')
                    return redirect('/contractor_profile')
            except Exception:
                messages.success(request, 'Invalid User.....')
                return redirect('/contractor_profile')
        else:
            data = Login.objects.filter(log_id=log_id)
            return render(request,'contractor/reset_con.html',{'data':data})
    else:
        return redirect('/home')  


def master_reg(request):
    if request.method == 'POST':
        use = request.POST['use']
        pas =  request.POST['pas']
        Login.objects.create(username=use,password=pas,role='admin',status=1)
        return redirect('/master_reg')
    else:
        return render(request,'master_reg.html')
    
def sign_out(request):
    logout(request)
    request.session.delete()
    return redirect('/home')

# Create your views here.

def forgot_password(request):
    if request.method == 'POST':
        email1 = request.POST.get('email')
        try:
            user1 = Contractor_register.objects.get(email=email1)
            print(user1)
        except:
            messages.info(request,"Email id not registered")
            return redirect(forgot_password)
        # Generate and save a unique token
        token = get_random_string(length=4)
        PasswordReset.objects.create(user=user1, token=token)
        print("hello")
        # Send email with reset link
        reset_link = f'http://127.0.0.1:8000/reset/{token}'
        try:
            send_mail('Reset Your Password', f'Click the link to reset your password: {reset_link}','settings.EMAIL_HOST_USER', [email1],fail_silently=False)
            # return render(request, 'emailsent.html')
            print("sended")
        except:
            print("network error")
            messages.info(request,"Network connection failed")
            return redirect(forgot_password)

    return render(request, 'forgot_password.html')

def reset_password(request, token):
       # Verify token and reset the password
      print(token)
      password_reset = PasswordReset.objects.get(token=token)
    #   usr = Contractor_register.objects.get(id=password_reset.user)
      if request.method == 'POST':
            new_password = request.POST.get('newpassword')
            repeat_password = request.POST.get('cpassword')
            if repeat_password == new_password:
                  password_reset.user.set_password(new_password)
                  password_reset.user.save()
                  # password_reset.delete()
                  return redirect('/login')
      return render(request, 'reset_password.html',{'token':token})

# def search(r):
#      if r.method=='POST':
#           s=r.POST.get('srch')
#           print(s)
#           re=Category.objects.get(category=s)
#           print(re)
#           data=Product_type.objects.filter(ct=re).values
#           print(data)
     
#           return render(r,'contractor/home.html',{'data':data})





def search(request):
    if request.method == 'POST':
        search_term = request.POST.get('srch')
        
        if not search_term:
            return redirect('/home')
        
        try:
            category = Category.objects.get(category=search_term)
        except Category.DoesNotExist:
            messages.info(request,"no such category")
            return redirect('/home')
        
        product_types = Product_type.objects.filter(ct=category).values()
        
        return render(request, 'contractor/home.html', {'data': product_types})

    return HttpResponse("Invalid request method", status=405)
          






