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
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
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


class EmployeeUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()

    class Meta:
        model = EmployeeProfile
        fields = ('time_card_nr', 'first_name', 'last_name',
                  'email', 'mobile', 'dob', 'nationality', 'address')
        widgets = {
            'dob': forms.DateInput(attrs={'class': 'datepicker'}),
        }

    def __init__(self, *args, **kwargs):
        super(EmployeeUpdateForm, self).__init__(*args, **kwargs)
        self.fields['time_card_nr'].widget.attrs['readonly'] = True

    def save(self, commit=True):
        employee_profile = super().save(commit=False)
        user = employee_profile.user
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
        queryset=CustomUser.objects.order_by('first_name', 'last_name'),
        widget=forms.SelectMultiple(attrs={'class': 'form-control', 'multiple': 'multiple'}),
        to_field_name='id',
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
            task.assigned_to.set(self.cleaned_data['employees'].values_list('id', flat=True))

            for user in task.assigned_to.all():
                TaskAssignmentConfirm.objects.get_or_create(task=task, employee=user)
        return task
