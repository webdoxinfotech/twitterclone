from django import forms
from django.contrib.auth import get_user_model
from .models import UserProfile
from django.forms import ModelForm

User = get_user_model()

class UserRegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    image = forms.ImageField()
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)


    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError("Password must match")
        return password2

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__icontains=username).exists():
            raise forms.ValidationError("This username is taken")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__icontains=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email


class EditProfileForm(ModelForm):
    class Meta:

        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
        )


class ProfileForm(ModelForm):
    class Meta:
        model = UserProfile

        fields = ('image',)  # Note that we didn't mention user field here.