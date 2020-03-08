from django import forms
from django.contrib.auth.forms import UserCreationForm
from . import models as user_models

"""
CSRF : Cross Site Request Foregery
Authenticate : https://docs.djangoproject.com/en/3.0/topics/auth/
"""


class SignUpForm(forms.ModelForm):
    class Meta:
        model = user_models.User
        fields = (
            "first_name",
            "last_name",
            "email",
        )
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "Firstname"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Secondname"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email"}),
        }

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirmed Password"})
    )

    def clean(self):
        email = self.cleaned_data["email"]

    # class Meta:
    #     model = user_models.User
    #     fields = ("first_name", "last_name", "email")

    # password = forms.CharField(widget=forms.PasswordInput)
    # password1 = forms.CharField(widget=forms.PasswordInput, label="confirm password")

    # def clean_password1(self):
    #     password = self.cleaned_data.get("password")
    #     password1 = self.cleaned_data.get("password1")

    #     if password != password1:
    #         raise forms.ValidationError("Password dose not match ")
    #     else:
    #         return password

    # def save(self, *arg, **kwargs):
    #     user = super().save(commit=False)
    #     email = self.cleaned_data.get("email")
    #     password = self.cleaned_data.get("password")
    #     user.username = email
    #     user.set_password(password)
    #     user.verify_email()
    #     user.save()


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email",}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password",})
    )
    pass

    # 기구현되어있는 method임. {clean_}명 return이 없으면 view의 cleaned_data는 없어짐

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        try:
            user = user_models.User.objects.get(username=email)
            if user.check_password(password):
                print(self.cleaned_data)
                return self.cleaned_data
            else:
                self.add_error("password", forms.ValidationError("Password is wrong"))
        except user_models.User.DoesNotExists:
            self.add_error("email", forms.ValidationError("User does not exists"))
