from django.urls import path 
from . import views

app_name = "accounts"

urlpatterns = [
   path("signup/", views.sign_up_view, name="sign_up_view"),
    path("signin/", views.sign_in_view, name="sign_in_view"),
    path("signout/" , views.sign_out_view , name="sign_out_view"),
   # path("profile/" , views.sign_out_view , name="sign_out_view"),

]