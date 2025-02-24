
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from .models import Profile
from recipes.models import Recipe
from favorites.models import Favorite
from django.db.models import Count

# Create your views here.

def sign_up_view (request:HttpRequest):
    msg =None
    try:
        if request.method == "POST":
                #create a new user
                user = User.objects.create_user(username=request.POST["username"], first_name=request.POST["first_name"], last_name=request.POST["last_name"], email=request.POST["email"], password=request.POST["password"])
                user.save()
                return redirect("accounts:sign_in_view")
    except Exception as e:
     msg= f"{e}"
     
    return render(request, "accounts/sign_up.html", {"msg" : msg})


def sign_in_view(request:HttpRequest):
    msg=None
# authenticate user
    try:
        if request.method == "POST":
            user = authenticate(request, username=request.POST["username"], password= request.POST["password"])

            if user:
                    login(request, user) #sign in user
                    return redirect("main:home_view")
            else:
                    msg = "Please provide correct username and password"

    except Exception as e:
      msg =f"sothing went wrong {e}"

    return render(request, "accounts/sign_in.html", {"msg" : msg})



def sign_out_view(request: HttpRequest):
   
    if request.user.is_authenticated:
        logout(request)
    
    return redirect("accounts:sign_in_view")
     

def user_profile_view(request: HttpRequest, user_id  ):
    
    try: 
        user = User.objects.get(id=user_id)
        # recipe= Recipe.objects.filter(user=request.user)

    except:
        return render(request, 'main/not_authrized.html')
    
    return render(request, 'accounts/profile.html', { "user":user })




def update_user_view(request: HttpRequest):
    msg = None

    if request.method == "POST":
        try:
            if request.user.is_authenticated:
                user : User = request.user
                user.first_name = request.POST["first_name"]
                user.last_name = request.POST["last_name"]
                user.email = request.POST["email"]
                user.save()

                try:
                    profile : Profile = request.user.profile
                except Exception as e:
                    profile = Profile(user=user, birth_date=request.POST["birth_date"])
                    profile.save()

                profile.birth_date = request.POST["birth_date"]
                if 'avatar' in request.FILES: profile.avatar = request.FILES["avatar"]
                profile.about = request.POST["about"]
                profile.insta_link = request.POST["insta_link"]
                profile.save()

                return redirect("accounts:user_profile_view", user_id = request.user.id)

            else:
                return redirect("accounts:sign_in_view")
        except IntegrityError as e:
            msg = f"Please select another username"
        except Exception as e:
            msg = f"something went wrong {e}"

    return render(request, "accounts/update_profile.html", {"msg" : msg})



def user_recipes_view(request, user_id):
    try:
        # Get the user based on the provided user_id
        user = User.objects.get(id=user_id)

        # Fetch recipes associated with the user
        user_recipes = Recipe.objects.filter(user=user)

        return render(request, 'accounts/user_recipes.html', {"user_recipes": user_recipes, "user": user})

    except User.DoesNotExist:
        # Handle the case where the user is not found
        return render(request, 'main/not_found.html')


def community_view (request:HttpRequest):

    distinct_users = Recipe.objects.values('user').annotate(recipe_count=Count('user')).filter(recipe_count__gt=0)
    
    # Get the User objects based on the distinct user IDs
    users = User.objects.filter(id__in=[user['user'] for user in distinct_users])
    
    return render(request, 'accounts/community.html', {'users': users})
