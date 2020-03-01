import os
import requests

from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.core.files.base import ContentFile
from . import forms as user_forms
from . import models as user_models

# Create your views here.


class SignUpView(FormView):
    template_name = "users/signup.html"
    form_class = user_forms.SignUpForm
    success_url = reverse_lazy("core:home")
    initial = {
        "first_name": "Jihwan",
        "last_name": "Oh",
        "email": "amzojh@naver.com",
    }

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(request=self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


class LoginView(FormView):

    template_name = "users/login.html"
    form_class = user_forms.LoginForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(request=self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)

        return super().form_valid(form)


def complete_verification(request, key):
    try:
        user = user_models.User.objects.get(email_secret=key)
        user.email_verified = True
        user.email_secret = ""
        user.save()
        # to do : add success message
    except user_models.User.DoesNotExists:
        # to do : add error message
        pass

    return redirect(reverse("core:home"))


def logout_view(request):
    logout(request)
    return redirect(reverse("core:home"))


"""
    Reference : https://developer.github.com/apps/building-oauth-apps/authorizing-oauth-apps/
"""


def github_login(request):
    client_id = os.environ.get("GITHUB_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/github/callback"
    return redirect(
        f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user&scope=read:user&scope=user:email"
    )


class GithubException(Exception):
    pass


# github access token !
def github_callback(request):
    try:
        client_id = os.environ.get("GITHUB_ID")
        client_secret = os.environ.get("GITHUB_SECRET")
        code = request.GET.get("code", None)
        print(code)

        headers = {"Accept": "application/json"}
        if code is not None:
            data = {
                "client_id": client_id,
                "client_secret": client_secret,
                "code": code,
            }

            token_reqeust = requests.post(
                f"https://github.com/login/oauth/access_token",
                headers=headers,
                data=data,
            )

            token_json = token_reqeust.json()
            print(token_json, data)
            error = token_json.get("error", None)

            if error is not None:
                raise GithubException
            else:
                access_token = token_json.get("access_token")
                api_result = requests.get(
                    "https://api.github.com/user",
                    headers={
                        "Authorization": f"token {access_token}",
                        "Accept": "application/json",
                    },
                )

                profile_json = api_result.json()
                username = profile_json.get("login", None)
                if username is not None:
                    name = profile_json.get("name")
                    bio = profile_json.get("bio")
                    email = profile_json.get("email")
                    if email is None:
                        api_result = requests.get(
                            "https://api.github.com/user/emails",
                            headers={
                                "Authorization": f"token {access_token}",
                                "Accept": "application/json",
                            },
                        )
                        profile_json = api_result.json()
                        email = profile_json[0].get("email")
                        print(profile_json)
                    try:
                        user = user_models.User.objects.get(email=email)
                        if user.login_method == user_models.User.LOGIN_GITHUB:
                            pass
                        else:
                            raise GithubException()
                    except user_models.User.DoesNotExist:
                        user = user_models.User.objects.create(
                            email=email,
                            first_name=email,
                            username=email,
                            bio=bio,
                            email_verified=True,
                            login_method=user_models.User.LOGIN_GITHUB,
                        )
                        user.set_unusable_password()
                        user.save()
                    login(request, user)
                    return redirect(reverse("core:home"))
                else:
                    return redirect(reverse("users:login"))

    except GithubException:
        return redirect(reverse("users:login"))


class KakaoException(Exception):
    pass


def kakao_login(request):
    app_key = os.environ.get("KAKAO_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={app_key}&redirect_uri={redirect_uri}&response_type=code"
    )


def kakao_callback(request):
    try:
        code = request.GET.get("code")
        data = {
            "grant_type": "authorization_code",
            "client_id": os.environ.get("KAKAO_ID"),
            "redirect_uri": "http://127.0.0.1:8000/users/login/kakao/callback",
            "code": code,
        }
        token_request = requests.post("https://kauth.kakao.com/oauth/token", data=data)

        token_json = token_request.json()
        error = token_json.get("error", None)
        if error is not None:
            raise KakaoException()

        access_token = token_json.get("access_token")

        profile_request = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        profile_json = profile_request.json()

        kakao_account = profile_json.get("kakao_account")
        email = kakao_account.get("email")
        print(profile_json)
        if email is None:
            raise KakaoException()

        properties = profile_json.get("properties")
        name = properties.get("nickname")
        avatar_url = properties.get("profile_image")

        try:
            user = user_models.User.objects.get(email=email)
            if user.login_method != user_models.User.LOGIN_KAKAO:
                raise KakaoException()

        except user_models.User.DoesNotExist:
            user = user_models.User.objects.create(
                email=email,
                username=email,
                first_name=name,
                login_method=user_models.User.LOGIN_KAKAO,
                email_verified=True,
            )
            user.set_unusable_password()
            user.save()

            """
            ImageField : F
            """
            if avatar_url is not None:
                avatar_response = requests.get(avatar_url)
                user.avatar.save(f"{name}-avatar", ContentFile(avatar_response.content))
        login(request, user)
        return redirect(reverse("core:home"))

    except KakaoException:
        return redirect(reverse("users:login"))
