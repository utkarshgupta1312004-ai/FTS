from django.shortcuts import render,redirect
from django.contrib import messages
from adminapp.models import Employee
from .models import LoginInfo

# Create your views here.
def Index(request):
    return render(request,'index.html')

def Adminlogin(request):
    try:
        if request.method == "POST":
            email = request.POST.get('username')
            password = request.POST.get('password')
            try:
                user = LoginInfo.objects.get(email=email, password=password)

                if user.usertype == 'admin':
                    messages.success(request, 'Login Success')
                    request.session['adminid'] = user.email
                    return redirect('admindash')
                else:
                    messages.error(request, 'Invalid user credentials for admin login')
                    return redirect('adminlogin')
            except LoginInfo.DoesNotExist:
                messages.error(request, 'Please Enter Correct Details')
                return redirect('adminlogin')

    except Exception:
        messages.error(request, 'Please Enter Correct Details')
        return redirect('adminlogin')
    
    return render(request, 'adminlogin.html')

def UserLogin(request):
    try:
        if request.method == "POST":
            email = request.POST.get('username')
            password = request.POST.get('password')
            try:
                user = LoginInfo.objects.get(email=email, password=password)

                if user.usertype == 'employee':
                    messages.success(request, 'Login Success')
                    request.session['empemail'] = user.email
                    try:
                        emp = Employee.objects.get(empemail=user.email)
                        request.session['empname'] = emp.empname
                    except Employee.DoesNotExist:
                        request.session['empname'] = user.email
                    return redirect('userdash')
                else:
                    messages.error(request, 'Invalid user credentials for user login')
                    return redirect('userlogin')
            except LoginInfo.DoesNotExist:
                messages.error(request, 'Please Enter Correct Details')
                return redirect('userlogin')

    except Exception:
        messages.error(request, 'Please Enter Correct Details')
        return redirect('userlogin')
    
    return render(request, 'userlogin.html')