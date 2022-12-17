from django import forms
from django.forms import ModelForm
from .models import Task
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from captcha.fields import CaptchaField, CaptchaTextInput

class TaskForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class':'form-control'})
        self.fields['description'].widget.attrs.update({'class':'form-control'})
        self.fields['complete'].widget.attrs.update({'class':'form-check-input'})
        self.fields['colors'].widget.attrs.update({'class':'form-select'})

    class Meta:
        model = Task
        exclude = ['user']



class LoginForm(forms.Form):
        username = forms.CharField(label = 'Username', 
                                   widget= forms.TextInput(attrs={'class':'form-control'}))
        password = forms.CharField(label = 'Password',
                                   widget = forms.PasswordInput(attrs={'class':'form-control'}))
        captcha = CaptchaField(label = 'Captcha',
                               widget=CaptchaTextInput(attrs={'class':'form-control'}))




class RegisterForm(UserCreationForm):  
    email = forms.EmailField(max_length=200, help_text='Required', 
                             widget = forms.EmailInput(attrs={'class':'form-control'}))

    captcha = CaptchaField(label = 'Captcha',
                           widget=CaptchaTextInput(attrs={'class':'form-control'})) 


    def __init__(self, *args, **kwargs):
         super().__init__(*args, **kwargs)
         for fieldname in ['username', 'email', 'password1', 'password2']:
            self.fields[fieldname].widget.attrs.update({'class':'form-control'})



    class Meta:  
        model = User  
        fields = ('username', 'email', 'password1', 'password2')