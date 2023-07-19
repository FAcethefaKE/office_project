from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm  # default django user creation form
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from django import forms
from .models import CustomUser, EmployeeProfile, Task, TaskAssignmentConfirm


class EmployeeRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()

    class Meta:
        model = EmployeeProfile
        fields = ('time_card_nr', 'first_name', 'last_name', 'email', 'mobile', 'dob', 'nationality', 'address')
        widgets = {
            'dob': forms.DateInput(attrs={'class': 'datepicker'}),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email:
            raise forms.ValidationError("Email field is required.")
        return email

    def save(self, commit=True):
        user = CustomUser(username=self.cleaned_data['email'])
        user.set_password(self.cleaned_data['password'])
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        employee_profile = super().save(commit=False)
        employee_profile.user = user
        if commit:
            employee_profile.save()
        return employee_profile


# class CustomUserChangeForm(UserChangeForm):
#     class Meta:
#         model = CustomUser
#         fields = ('username',)


class EmployeeUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    # username = forms.CharField(max_length=60)

    class Meta:
        model = EmployeeProfile
        fields = ('time_card_nr', 'first_name', 'last_name',
                  'email', 'mobile', 'dob', 'nationality', 'address')
        widgets = {
            'dob': forms.DateInput(attrs={'class': 'datepicker'}),
        }

    def __init__(self, *args, **kwargs):
        super(EmployeeUpdateForm, self).__init__(*args, **kwargs)
        self.fields['time_card_nr'].widget.attrs['readonly'] = True  # Make time_card_nr field read-only
        # self.fields['username'].initial = self.instance.user.username  # Set the initial value of username

        # self.fields['username'] = forms.CharField(max_length=60, initial=self.instance.user.username, disabled=True)
    def save(self, commit=True):
        employee_profile = super().save(commit=False)
        user = employee_profile.user
        # user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        employee_profile.user.first_name = self.cleaned_data['first_name']
        employee_profile.user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            employee_profile.save()
            user.save()
        return employee_profile


class TaskCreateForm(forms.ModelForm):

    employees = forms.ModelMultipleChoiceField(
        queryset=EmployeeProfile.objects.order_by('user__first_name', 'user__last_name'),
        widget=forms.SelectMultiple(attrs={'class': 'form-control', 'multiple': 'multiple'})
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'assign_date', 'employees']

        widgets = {
            'assign_date': forms.DateInput(attrs={'class': 'datepicker'}),
        }

    def save(self, commit=True):
        task = super().save(commit=False)
        if commit:
            task.save()
            task.assigned_to.set(self.cleaned_data['employees'].values_list('user_id', flat=True))  # Assign the selected employees

            for user in task.assigned_to.all():
                TaskAssignmentConfirm.objects.create(task=task, employee=user)
        return task






    # User = get_user_model()

# class EmployeeRegistrationForm(UserCreationForm):
#     class Meta:
#         model = get_user_model()
#         fields = ('username', 'password1', 'password2', 'time_card_nr', 'full_name', 'mobile',
#                   'address', 'email', 'nationality')
#
#     def __init__(self, *args, **kwargs):
#         super(EmployeeRegistrationForm, self).__init__(*args, **kwargs)
#         self.fields.pop('user')


# class EmployeeProfileForm(forms.ModelForm):
#     class Meta:
#         model = EmployeeProfile
#         fields = ['username', 'password1', 'password2', 'time_card_nr', 'full_name', 'mobile', 'address']


# class EmployeeCreationForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput)
#
#     class Meta:
#         model = Employee
#         fields = ['full_name', 'email', 'password', 'time_card_nr', 'mobile', 'address', 'nationality']
#
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.user = User.objects.create_user(
#             username=self.cleaned_data['username'],
#             email=self.cleaned_data['email'],
#             password=self.cleaned_data['password']
#         )
#         if commit:
#             user.save()
#         return user

# class EmployeeForm(forms.Form):
#     time_card_nr = forms.CharField(max_length=5)
#     username = forms.CharField(max_length=15, required=False)
#     full_name = forms.CharField(max_length=100)
#     dob = forms.DateField(required=False)
#     email = forms.EmailField(max_length=50)
#     mobile = forms.CharField(max_length=15, required=False)
#     nationality = forms.CharField(max_length=30, required=False)
#     address = forms.CharField(max_length=100, required=False)
#     password1 = forms.CharField(widget=forms.PasswordInput)
#     password2 = forms.CharField(widget=forms.PasswordInput)
#
#     def clean(self):
#         cleaned_data = super().clean()
#         password1 = cleaned_data.get('password1')
#         password2 = cleaned_data.get('password2')
#
#         if password1 and password2 and password1 != password2:
#             raise forms.ValidationError("Passwords do not match.")
#
#     def save(self):
#         time_card_nr = self.cleaned_data['time_card_nr']
#         full_name = self.cleaned_data['full_name']
#         dob = self.cleaned_data['dob']
#         mobile = self.cleaned_data['mobile']
#         nationality = self.cleaned_data['nationality']
#         address = self.cleaned_data['address']
#         username = self.cleaned_data['username']
#         password = self.cleaned_data['password1']
#         email = self.cleaned_data['email']
#
#         user = User.objects.create_user(username=username, password=password, email=email)
#         profile = Employee(user=user, time_card_nr=time_card_nr, dob=dob, full_name=full_name, mobile=mobile,
#                            nationality=nationality, address=address)
#         profile.save()
#         return user


# class EmployeeForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput)
#
#     class Meta:
#         model = Employee
#         fields = ['full_name', 'password', 'time_card_nr', 'mobile', 'address', 'nationality', 'dob']
