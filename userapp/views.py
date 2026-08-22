
from django.utils import timezone
import datetime
from userapp.models import FileMovement, Files
from django.contrib import messages
from adminapp.models import Employee
from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_control
from django.db.models import Q
from mainapp.models import LoginInfo

# Create your views here.


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def Userdash(request):
    empemail = request.session.get('empemail')
    if not empemail:
        messages.error(request, 'Please Login First')
        return redirect('userlogin')

    try:
        emp = Employee.objects.select_related('empdept').get(empemail=empemail)
    except Employee.DoesNotExist:
        messages.error(request, 'Employee profile not found')
        return redirect('userlogin')

    # Summary Statistics
    initiated_count = Files.objects.filter(initiated_by=emp).count()
    received_count = Files.objects.filter(current_holder=emp).count()
    pending_count = Files.objects.filter(current_holder=emp, status="OPEN").count()
    in_progress_count = Files.objects.filter(
        Q(initiated_by=emp) | Q(current_holder=emp), 
        status="IN_PROGRESS"
    ).distinct().count()
    closed_count = Files.objects.filter(
        Q(initiated_by=emp) | Q(current_holder=emp), 
        status="CLOSED"
    ).distinct().count()
    open_count = Files.objects.filter(
        Q(initiated_by=emp) | Q(current_holder=emp), 
        status="OPEN"
    ).distinct().count()
    total_files = Files.objects.filter(
        Q(initiated_by=emp) | Q(current_holder=emp)
    ).distinct().count()
    movements_count = FileMovement.objects.filter(
        Q(from_employee=emp) | Q(to_employee=emp)
    ).count()

    # Recent Data Lists
    recent_received = Files.objects.filter(current_holder=emp).select_related(
        'initiated_by', 'initiated_by__empdept'
    ).order_by('-created_at')[:5]

    recent_initiated = Files.objects.filter(initiated_by=emp).select_related(
        'current_holder', 'current_holder__empdept'
    ).order_by('-created_at')[:5]

    recent_movements = FileMovement.objects.filter(
        Q(from_employee=emp) | Q(to_employee=emp) | Q(file__initiated_by=emp)
    ).select_related('file', 'from_employee', 'to_employee').order_by('-moved_at').distinct()[:6]

    dept_colleagues = Employee.objects.filter(
        empdept=emp.empdept
    ).exclude(empemail=empemail)[:4]
    dept_colleagues_count = Employee.objects.filter(empdept=emp.empdept).count()

    today_str = datetime.date.today().strftime('%A, %d %B %Y')

    context = {
        'emp': emp,
        'empemail': empemail,
        'initiated_count': initiated_count,
        'received_count': received_count,
        'pending_count': pending_count,
        'in_progress_count': in_progress_count,
        'closed_count': closed_count,
        'open_count': open_count,
        'total_files': total_files,
        'movements_count': movements_count,
        'recent_received': recent_received,
        'recent_initiated': recent_initiated,
        'recent_movements': recent_movements,
        'dept_colleagues': dept_colleagues,
        'dept_colleagues_count': dept_colleagues_count,
        'today_str': today_str,
    }
    return render(request, 'userdash.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def Userlogout(request):
    request.session.pop('empemail', None)
    request.session.pop('empname', None)
    return redirect('userlogin')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def ViewProfile(request):
    empemail = request.session.get('empemail')
    if not empemail:
        messages.error(request, 'Please Login First')
        return redirect('userlogin')

    try:
        user = Employee.objects.get(empemail=empemail)
        return render(request, 'viewprofile.html', {'user': user})
    except Employee.DoesNotExist:
        messages.error(request, 'Employee profile not found')
        return redirect('userlogin')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def InitiateFile(request):
    empemail = request.session.get('empemail')
    if not empemail:
        messages.error(request, 'Please Login First')
        return redirect('userlogin')

    
    emp = Employee.objects.get(empemail=empemail)
   
    employee_list = Employee.objects.all()
    context = {
        'empemail': empemail,
        'emp': emp,
        'employee_list': employee_list

    }
    if request.method=="POST":
        title=request.POST.get("title")
        file_attachment=request.FILES.get("file_attachment")
        subject=request.POST.get("subject")
        emp_id=request.POST.get("emp_id")
        forwarded_to=Employee.objects.get(empemail=emp_id)
        fi=Files.objects.create(title=title,file_attachment=file_attachment,subject=subject,initiated_by=emp,current_holder=forwarded_to)
        messages.success(request,"File initiatied successfully")
        FileMovement.objects.create(file=fi,from_employee=emp,to_employee=forwarded_to,action="CREATE",remark="File created and forwarded to "+forwarded_to.empname)
        return redirect("viewfiles")


    return render(request, 'initiatefile.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def UpdateProfile(request):
    empemail = request.session.get('empemail')
    if not empemail:
        messages.error(request, 'Please Login First')
        return redirect('userlogin')
    emp = Employee.objects.get(empemail=empemail)

    user=Employee.objects.all()
    context={
        'user':user,
        'emp':emp
    }

    if request.method=='POST':
        emp.empname=request.POST.get("empname")
        emp.empdiscription=request.POST.get("empdiscription")
        emp.pictures=request.FILES.get("pictures")
        emp.save()
        messages.success(request,"Profile updated successfully")
        return redirect("updateprofile")
    return render(request, 'updateprofile.html',context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def ViewFiles(request):
    empemail = request.session.get('empemail')
    if not empemail:
        messages.error(request, 'Please Login First')
        return redirect('userlogin')
    emp=Employee.objects.get(empemail=empemail)
    files=Files.objects.filter(initiated_by=emp).order_by('-created_at')
    context={
        'empemail':empemail,
        'files':files
    }
    return render(request, 'viewfiles.html',context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def RecivedFiles(request):
    empemail = request.session.get('empemail')
    if not empemail:
        messages.error(request, 'Please Login First')
        return redirect('userlogin')
    emp = Employee.objects.get(empemail=empemail)
    files = Files.objects.filter(current_holder=emp).order_by('-created_at')
    context = {
        'empemail': empemail,
        'files': files
    }
    return render(request, 'receivedfile.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def ChangeUserPwd(request):
    empemail = request.session.get('empemail')
    if not empemail:
        messages.error(request, 'Please Login First')
        return redirect('userlogin')
    if request.method=="POST":
        oldpwd=request.POST.get("oldpwd")
        newpwd=request.POST.get("newpwd")
        conpwd=request.POST.get("conpwd")
        emp=LoginInfo.objects.get(email=empemail)
        if emp.password==oldpwd:
            if newpwd==conpwd:
                emp.password=newpwd
                emp.save()
                messages.success(request,"Password changed successfully")
                return redirect("userlogin")
            else:
                messages.error(request,"New password and confirm password do not match")
        else:
            messages.error(request,"Old password is incorrect")

    return render(request, 'changeuserpwd.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def FileDetails(request, fid):
    empemail = request.session.get('empemail')
    if not empemail:
        messages.error(request, 'Please Login First')
        return redirect('userlogin')

    try:
        emp = Employee.objects.get(empemail=empemail)
        file = Files.objects.get(file_no=fid)
    except (Employee.DoesNotExist, Files.DoesNotExist):
        messages.error(request, 'File or Employee not found')
        return redirect('recievedfiles')

    employees = Employee.objects.all()
    file_movements = FileMovement.objects.filter(file=file).order_by('moved_at')

    if request.method == "POST":
        action = request.POST.get("action")
        remark = request.POST.get("remark", "")

        if action == "FORWARD":
            emp_id = request.POST.get("emp_id")
            if not emp_id:
                messages.error(request, "Please select an employee to forward the file.")
                return redirect("filedetails", fid=fid)
            try:
                to_employee = Employee.objects.get(empemail=emp_id)
                FileMovement.objects.create(
                    file=file,
                    from_employee=emp,
                    to_employee=to_employee,
                    action="FORWARD",
                    remark=remark,
                )
                file.current_holder = to_employee
                file.status = "IN_PROGRESS"
                file.save()
                messages.success(request, f"File forwarded to {to_employee.empname} successfully")
                return redirect("recievedfiles")
            except Employee.DoesNotExist:
                messages.error(request, "Selected employee not found")
                return redirect("filedetails", fid=fid)

        elif action == "RETURN":
            # Return to the previous sender or initiator
            last_movement = FileMovement.objects.filter(file=file, to_employee=emp).order_by('-moved_at').first()
            if last_movement and last_movement.from_employee:
                to_employee = last_movement.from_employee
            else:
                to_employee = file.initiated_by

            FileMovement.objects.create(
                file=file,
                from_employee=emp,
                to_employee=to_employee,
                action="RETURN",
                remark=remark,
            )
            file.current_holder = to_employee
            file.status = "OPEN"
            file.save()
            messages.success(request, f"File returned to {to_employee.empname} successfully")
            return redirect("recievedfiles")

        elif action == "CLOSE":
            FileMovement.objects.create(
                file=file,
                from_employee=emp,
                to_employee=None,
                action="CLOSE",
                remark=remark,
            )
            file.status = "CLOSED"
            file.closed_at = timezone.now()
            file.save()
            messages.success(request, "File closed successfully")
            return redirect("recievedfiles")

    context = {
        'emp': emp,
        'empemail': empemail,
        'file': file,
        'employees': employees,
        'file_movements': file_movements
    }
    return render(request, 'filedetails.html', context)
    