from django.shortcuts import render, redirect
from .models import * 
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def home(request):
    '''simple home page + contact/enquiry form'''
    if request.method == 'POST':
        name= request.POST.get('name')
        email= request.POST.get('email')
        mobile= request.POST.get('mobile')
        message= request.POST.get('message')

# validate the form data and save the enquiry to the database
        if name and email and mobile and message:
            Enquiry.objects.create(name=name, email=email, mobile=mobile, message=message)
            messages.success(request, 'Your enquiry has been submitted successfully.')
            return redirect('home') # Redirect to the home page after successful submission
        else:
            messages.error(request, 'Please fill in all fields.')
                
    return render(request, 'home.html')




def about(request):
    return render(request, 'about.html')



def admin_login_view(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

# authenticate function le check garxa ki username ra password sahi cha ki nai database ma , ani user object return garxa
        user = authenticate(request, username=username, password=password) 

        if user is not None and getattr(user, 'role', None) == 'ADMIN':  # Check if the user is authenticated and has the admin role
            login(request, user) # Login the user and create a session
            messages.success(request, 'Login successful!')
            return redirect('admin_dashboard')  # Redirect to admin dashboard upon successful login
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'admin_login.html')


#decorator 
def admin_required(view_func):
    '''Decorator to check if the user is authenticated and has the admin role  '''

    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or getattr(request.user, 'role', None) != 'ADMIN':
            messages.error(request, 'You must be an admin to access this page.')
            return redirect('admin_login')
        return view_func(request, *args, **kwargs)
    return wrapper




@admin_required
def admin_dashboard_view(request):
   return render(request, 'admin_dashboard.html')


def logout_view(request):
    logout(request)  # Log out the user and end the session
    messages.success(request, 'You have been logged out successfully.')
    return redirect('admin_login')  # Redirect to admin login page after logout



@admin_required
def admin_plans_list(request):
    plans= MembershipPlan.objects.all().order_by("duration_months")
    return render(request, 'admin_plans_list.html', {'plans': plans})


@admin_required
def admin_plan_add(request):
    if request.method == "POST":
        name = request.POST.get('name')
        duration_months = request.POST.get ('duration_months ')
        fee = request.POST.get('fee')
        description = request.POST.get('description')

        if name and duration_months and fee:
            MembershipPlan.objects.create(
                name=name,
                duration_months=duration_months,
                fee=fee,
                description=description
            )
            messages.success(request, 'Membership plan added successfully!! ')
            return redirect('admin_plans_list')
        else:
            messages.error(request, 'Please fill in all required fields.')
            return redirect('admin_plan_form.html', {'mode': 'add'})








#=====================================================================================
def members_login_view(request):
    # Similar to admin_login_view but checks for MEMBER role
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None and getattr(user, 'role', None) == 'MEMBER':
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('member_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'members_login.html')




