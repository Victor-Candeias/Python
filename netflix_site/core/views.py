from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Movie

# Create your views here.
# *********************************************************
# index.html function
@login_required(login_url='login')
def index(request):
    movies = Movie.objects.all()
    
    context = {
        'movies': movies
    }
    
    return render(request, 'index.html', context)

# *********************************************************
# Movie play function  
@login_required(login_url='login')
def movie(request, pk):
    movie_uuid = pk
    movie_detail = Movie.objects.get(uu_id=movie_uuid)
    
    context = {
        'movie_details': movie_detail
    }

    return render(request, 'movie.html', context)

# *********************************************************
# My list of movies page
@login_required(login_url='login')
def my_list(request):
    pass

# *********************************************************
# My list of movies page
@login_required(login_url='login')
def add_to_list(request):
    pass

# *********************************************************
# Login page
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Log user in
        login_result = authenticate(request, username=username, password=password)
        
        if True:
            return redirect('/')   
        else:
            messages.info(request, 'Credentials invalid!!!')
            return redirect('login')
        
        # user_login = auth.authenticate(request, username=username, password=password)
        
        # if user_login is not None:
        #     auth.login(request, user_login)
        #     return redirect('/')   
        # else:
        #     messages.info(request, 'Credentials invalid!!!')
        #     return redirect('login')   
    else:                      
        return render(request, 'login.html')

# *********************************************************
# Signup page
def signup(request):
    if request.method == 'POST':
        # collect all details send
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        
        if password == password2:
            # create user
            # Check email
            if (User.objects.filter(email=email).exists()):
                messages.info(request, 'Email Already Exists!!!')
                return redirect('signup')  
              
            # Checks user name
            elif (User.objects.filter(username=username).exists()):
                messages.info(request, 'User Name Already Exists!!!')
                return redirect('signup')  
                  
            else:
                # create user
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password)
                user.save()
                
                # Log user in
                login_result = authenticate(request, username=username, password=password)

                if True:
                    return redirect('/')   
                else:
                    messages.info(request, 'Credentials invalid!!!')
                    return redirect('login')
                
                # Log user in
                # user_login = auth.authenticate(request, username=username, password=password)
                # auth.login(request, user_login)
                # return redirect('/')  

        else:
            # Wrong password
            messages.info(request, 'Password not Matching!!!')
            return redirect('signup')
    else:
        return render(request, 'signup.html')

# *********************************************************
# Logout function 
@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    # redirect to home page
    return redirect('/login')

# *********************************************************
# Authenticate function
def authenticate(request, username: str | None, password: str | None):
    # Log user in
    user_login = auth.authenticate(request, username=username, password=password)
    
    if user_login is not None:
        auth.login(request, user_login)
        return True  
    else:
        return False