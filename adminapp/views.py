from userapp.models import Files, FileMovement
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_control
from django.db import transaction
from django.db.models import Count, Q
from adminapp.models import Department, Employee
from mainapp.models import LoginInfo
import datetime

# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def Admindash(request):
    adminid = request.session.get('adminid')
    if not adminid:
        messages.error(request, 'Please Login First')
        return redirect('adminlogin')
    
    dept_count = Department.objects.count()
    emp_count = Employee.objects.count()
    user_count = LoginInfo.objects.count()
    files_count = Files.objects.count()
    open_files_count = Files.objects.filter(status="OPEN").count()
    progress_files_count = Files.objects.filter(status="IN_PROGRESS").count()
    closed_files_count = Files.objects.filter(status="CLOSED").count()
    
    departments = Department.objects.all()
    recent_employees = Employee.objects.select_related('empdept').order_by('-joindate')[:6]
    recent_files = Files.objects.select_related('initiated_by', 'current_holder', 'initiated_by__empdept', 'current_holder__empdept').order_by('-created_at')[:6]
    
    today_str = datetime.date.today().strftime('%A, %d %B %Y')
    
    context = {
        'adminid': adminid,
        'dept_count': dept_count,
        'emp_count': emp_count,
        'user_count': user_count,
        'files_count': files_count,
        'open_files_count': open_files_count,
        'progress_files_count': progress_files_count,
        'closed_files_count': closed_files_count,
        'departments': departments,
        'recent_employees': recent_employees,
        'recent_files': recent_files,
        'today_str': today_str,
    }
    return render(request, 'admindash.html', context)

   

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def AdminLogout(request):
    del request.session['adminid']
    return redirect('adminlogin')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def Adddept(request):
    try:
        
        adminid=request.session.get('adminid')
        if not adminid:
            messages.error(request,'Please Login First')
            return redirect('adminlogin')
        if request.method=="POST":
                dept_name = request.POST['dept_name']
                    # Save the department to the database
                department = Department(deptname=dept_name)
                messages.success(request, 'Department added successfully!')
                department.save()
                return redirect('viewdept')
        return render(request,'adddept.html')
    except KeyError:
        messages.error(request,'Please Login First')
        return redirect('adminlogin')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def ViewDept(request):
    try:
        adminid=request.session.get('adminid')
        if not adminid:
            messages.error(request,'Please Login First')
            return redirect('adminlogin')
        depts = Department.objects.annotate(emp_count=Count('employee')).all()


        if request.method=='POST':
            dept_id=request.POST.get('deptid')
            dept_name=request.POST.get('deptname')
            Department.objects.filter(deptid=dept_id).update(deptname=dept_name)
            messages.success(request, 'Department updated successfully!')
            return redirect('viewdept')
        return render(request,'viewdept.html',{'depts':depts})
    except KeyError:
        messages.error(request,'Please Login First')
        return redirect('adminlogin')  

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def DeleteDept(request, dept_id):
    try:
        adminid=request.session.get('adminid')
        if not adminid:
            messages.error(request,'Please Login First')
            return redirect('adminlogin')
        department = Department.objects.get(deptid=dept_id)
        department.delete()
        messages.success(request, 'Department deleted successfully!')
        return redirect('viewdept')
    except Department.DoesNotExist:
        messages.error(request, 'Department does not exist.')
        return redirect('viewdept')
    except KeyError:
        messages.error(request,'Please Login First')
        return redirect('adminlogin') 

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def AddEmp(request):
    try:
        adminid=request.session.get('adminid')
        if not adminid:
            messages.error(request,'Please Login First')
            return redirect('adminlogin')
        if request.method=="POST":
            empid = request.POST['empid']
            empname = request.POST['empname']
            empemail = request.POST['empemail']
            empdiscription = request.POST['empdiscription']
            empdept = request.POST['empdept']
            joindate = datetime.date.today()  # Set the join date to the current date

            # Get the department object based on the selected department name
            try:
                empdept = Department.objects.get(deptname=empdept)
            except Department.DoesNotExist:
                messages.error(request, 'Selected department does not exist.')
                return redirect('addemp')

            if Employee.objects.filter(empemail=empemail).exists():
                messages.error(request, 'Employee with this email already exists.')
                return redirect('addemp')
            # Save the employee to the database
            employee = Employee(
                empid=empid,
                empname=empname,
                empemail=empemail,
                empdiscription=empdiscription,
                empdept=empdept,
                joindate=joindate,
            )
            employee.save()
            login=LoginInfo(email=empemail,password="12345678",usertype='employee')
            login.save()
            messages.success(request, 'Employee added successfully!')
            return redirect('admindash')
        return render(request,'addemp.html',{'depts':Department.objects.all()})
    except KeyError:
        messages.error(request,'Please Login First')
        return redirect('adminlogin')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def ViewEmp(request):
    try:
        adminid = request.session.get('adminid')
        if not adminid:
            messages.error(request, 'Please Login First')
            return redirect('adminlogin')
        
        if request.method == "POST":
            old_empemail = request.POST.get('old_empemail')
            empid = request.POST.get('empid')
            empname = request.POST.get('empname')
            empemail = request.POST.get('empemail')
            empdept_val = request.POST.get('empdept')
            empdiscription = request.POST.get('empdiscription')

            if Employee.objects.exclude(empemail=old_empemail).filter(Q(empid=empid) | Q(empemail=empemail)).exists():
                messages.error(request, 'User already exists')
                return redirect('viewemp')
            else:
                try:
                    dept = Department.objects.get(deptid=empdept_val) if str(empdept_val).isdigit() else Department.objects.get(deptname=empdept_val)
                    
                    if old_empemail != empemail:
                       
                            old_emp = Employee.objects.get(empemail=old_empemail)
                            
                            # 1. Create new employee record with updated email & fields
                            new_emp = Employee.objects.create(
                                empid=empid,
                                empname=empname,
                                empemail=empemail,
                                empdept=dept,
                                empdiscription=empdiscription,
                                joindate=old_emp.joindate,
                                pictures=old_emp.pictures
                            )

                            # 2. Reassign foreign key references to the new employee record
                            LoginInfo.objects.filter(email=old_empemail).update(email=empemail)
                            Files.objects.filter(initiated_by=old_emp).update(initiated_by=new_emp)
                            Files.objects.filter(current_holder=old_emp).update(current_holder=new_emp)
                            FileMovement.objects.filter(from_employee=old_emp).update(from_employee=new_emp)
                            FileMovement.objects.filter(to_employee=old_emp).update(to_employee=new_emp)

                            # 3. Safely remove the old employee record
                            old_emp.delete()
                    else:
                        emp = Employee.objects.get(empemail=old_empemail)
                        emp.empid = empid
                        emp.empname = empname
                        emp.empdept = dept
                        emp.empdiscription = empdiscription
                        emp.save()

                    messages.success(request, 'Employee updated successfully!')
                except (Employee.DoesNotExist, Department.DoesNotExist):
                    messages.error(request, 'Employee or Department record not found.')

                return redirect('viewemp')

        empinfo = Employee.objects.select_related('empdept').all()
        depts = Department.objects.all()
        return render(request, 'viewemp.html', {'empinfo': empinfo, 'depts': depts})
    except KeyError:
        messages.error(request, 'Please Login First')
        return redirect('adminlogin')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def DeleteEmp(request, empemail):
    try:
        adminid=request.session.get('adminid')
        if not adminid:
            messages.error(request,'Please Login First')
            return redirect('adminlogin')
        employee = Employee.objects.get(empemail=empemail)
        employee.delete()
        LoginInfo.objects.filter(email=empemail).delete()
        messages.success(request, 'Employee deleted successfully!')
        return redirect('viewemp')
    except (KeyError, Employee.DoesNotExist):
        messages.error(request, 'Employee does not exist.')
        return redirect('viewemp')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def ChangeAdminPwd(request):
    
    adminid=request.session.get('adminid')
    if not adminid:
            messages.error(request,'Please Login First')
            return redirect('adminlogin')
    if request.method=="POST":
        oldpwd=request.POST.get("oldpwd")
        newpwd=request.POST.get("newpwd")
        conpwd=request.POST.get("conpwd")

        if newpwd!=conpwd:
                messages.error(request,"Old Password mismatched")
                return redirect('changeadminpwd')
        try:
            LoginInfo.objects.get(email=adminid, password=oldpwd)
            LoginInfo.objects.filter(email=adminid).update(password=newpwd)
            messages.success(request, 'Password updated Successfully')
            return redirect('adminlogout')
        except LoginInfo.DoesNotExist:
            messages.error(request, "Old password does not match")
            return redirect('changeadminpwd')
    return render(request,'changeadminpwd.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def ViewAllFiles(request):
    adminid = request.session.get('adminid')
    if not adminid:
        messages.error(request, 'Please Login First')
        return redirect('adminlogin')
    
    status_filter = request.GET.get('status', 'ALL')
    if status_filter in ['OPEN', 'IN_PROGRESS', 'CLOSED']:
        all_files = Files.objects.filter(status=status_filter).select_related(
            'initiated_by', 'current_holder', 'initiated_by__empdept', 'current_holder__empdept'
        ).order_by('-created_at')
    else:
        all_files = Files.objects.select_related(
            'initiated_by', 'current_holder', 'initiated_by__empdept', 'current_holder__empdept'
        ).order_by('-created_at')

    total_count = Files.objects.count()
    open_count = Files.objects.filter(status="OPEN").count()
    progress_count = Files.objects.filter(status="IN_PROGRESS").count()
    closed_count = Files.objects.filter(status="CLOSED").count()

    context = {
        'adminid': adminid,
        'files': all_files,
        'status_filter': status_filter,
        'total_count': total_count,
        'open_count': open_count,
        'progress_count': progress_count,
        'closed_count': closed_count,
    }
    return render(request, 'viewallfiles.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def AdminFileDetails(request, fid):
    adminid = request.session.get('adminid')
    if not adminid:
        messages.error(request, 'Please Login First')
        return redirect('adminlogin')
    
    try:
        file = Files.objects.select_related(
            'initiated_by', 'current_holder', 'initiated_by__empdept', 'current_holder__empdept'
        ).get(file_no=fid)
    except Files.DoesNotExist:
        messages.error(request, 'File not found')
        return redirect('adminallfiles')
    
    file_movements = FileMovement.objects.filter(file=file).select_related(
        'from_employee', 'to_employee', 'from_employee__empdept', 'to_employee__empdept'
    ).order_by('moved_at')

    context = {
        'adminid': adminid,
        'file': file,
        'file_movements': file_movements,
    }
    return render(request, 'adminfiledetails.html', context)
    
