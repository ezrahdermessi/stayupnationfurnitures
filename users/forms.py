from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, UserProfile


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone')

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('bio', 'avatar', 'address', 'city', 'state', 'postal_code', 'country')


class EmailOrUsernameAuthenticationForm(AuthenticationForm):
    """
    Authentication form that allows entering either username or email
    into the same field.
    """

    username = forms.CharField(
        label="Username or Email",
        widget=forms.TextInput(attrs={"autofocus": True}),
    )