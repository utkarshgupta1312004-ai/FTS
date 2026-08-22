from adminapp.models import Employee

def user_context(request):
    empemail = request.session.get('empemail')
    if empemail:
        try:
            emp = Employee.objects.get(empemail=empemail)
            return {'logged_user': emp}
        except Employee.DoesNotExist:
            return {'logged_user': None}
    return {'logged_user': None}
