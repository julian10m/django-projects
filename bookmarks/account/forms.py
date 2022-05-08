from django import forms
from django.contrib.auth.models import User
from .models import Profile
# from string import Template
# from django.utils.safestring import mark_safe

# class PictureWidget(forms.widgets.Widget):
#     def render(self, name, value, attrs=None, **kwargs):
#         html =  Template("""<img src="$link"/>""")
#         return mark_safe(html.substitute(link=value))

class LoginForm(forms.Form):
    username = forms.CharField(label='Username / email')
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',
                               widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    # clean_<fieldname>()
    # This is called when we make form.is_valid()
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileEditForm(forms.ModelForm):
    # photo = forms.ImageField(required=False, 
                            #  widget=PictureWidget)
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')
