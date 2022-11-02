from django.shortcuts import render
from basic_app.forms import UserForm, UserProfileInfoForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate,login,logout

# Create your views here.
def index(request):
    inx_cont={'welcome':'Hello its index file'}
    return render(request,'basic_app/index.html',inx_cont)

def register(request):

    registered = False
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save() #save in database
            user.set_password(user.password) #hashing the password
            user.save() #save hash password to database

            profile = profile_form.save(commit=False) #commit is false because we don't want to save it in the database
            profile.user = user #check onetoone relationship

            if 'profile_pic' in request.FILES: #if profile_pic has files
                profile.profile_pic = request.FILES['profile_pic']
    
            profile.save()
            registered=True

        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request,'basic_app/registration.html',
                            {   'user_form':user_form,
                                'profile_form':profile_form,
                                'registered': registered,    })

@login_required
def special(request): #in order to return something special
    return HttpResponse("You are logged in ,nice")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def user_login(request):
    if request.method =='POST':
        username = request.POST.get('username') #get usename
        password = request.POST.get('password') #get password and declear it

        user = authenticate(username=username,password=password) #authenticate if the user is valid

        if user: #if the user is valid then
            if user.is_active: #user is active
                login(request,user) #log the user in
                return HttpResponseRedirect(reverse('index')) #redirect the page to index
            else:
                return HttpResponse("Account is not active")
        else:
            print("Someone tried to login and faild")
            print("username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login")
    else:
        return render(request,'basic_app/login.html',{})
