from django.contrib.auth.mixins import UserPassesTestMixin

def in_group(user, group_name):
    return user.is_authenticated and user.groups.filter(name=group_name).exists() 

def is_patient(user):
    return in_group(user, 'Patient')

def is_doctor(user):
    return in_group(user, 'Doctor')

def is_clinic_admin(user):
    return user.is_authenticated and (user.is_superuser or in_group(user, 'Admin'))

class ClinicAdminRequiredMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        return is_clinic_admin(self.request.user)

class StaffRequiredMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return is_clinic_admin(user) or is_doctor(user)