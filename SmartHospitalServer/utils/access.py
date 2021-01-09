from django.contrib.auth.decorators import user_passes_test

# Checks whether current user is a patient
def is_patient(request):
    try:
        is_patient = request.user.patient.all_patient
        return True
    except:
        return False

# Decorator function to check patient login
def patient_access():
    def check_patient(user):
        try:
            is_patient = user.patient.all_patient
            return True
        except:
            return False
    return user_passes_test(check_patient, login_url='unauthorized')

# Decorator function to check staff login
def staff_access():
    def check_staff(user):
        try:
            is_staff = user.staff.all_staff
            return True
        except:
            return False
    return user_passes_test(check_staff, login_url='unauthorized')

# Decorator function to check admin login
def admin_access():
    def check_admin(user):
        if(user.is_superuser):
            return True
        else:
            return False
    return user_passes_test(check_admin, login_url='unauthorized')

# Returns patient access in a dictionary for passing to the HTTP files
# Other variables are also added to this function before being passed to the HTTP pages
def http_dict_func(request):
    return {'is_patient': is_patient(request)}