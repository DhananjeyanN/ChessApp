from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

from accounts.models import Profile


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'confirm_password']
        # widgets = {
        #     'email': forms.EmailInput(attrs = {'class': 'form-field', 'placeholder':'Enter Email', 'type':'email'})
        # }

    def clean(self):
        clean_data = super().clean()
        password = clean_data.get('password')
        confirm_password = clean_data.get('confirm_password')
        if password != confirm_password:
            self.add_error('confirm_password', 'password do not match')

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-field'
            self.fields[field].widget.attrs['placeholder'] = f'Enter {field}'


class LoginForm(AuthenticationForm):
    class Meta:
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = []

    def __init__(self, *args, **kwargs):
        super(EditPostForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-field'


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'dob']
