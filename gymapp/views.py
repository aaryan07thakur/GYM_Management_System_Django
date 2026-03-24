from django.shortcuts import render
from .models import * 
from django.contrib import messages

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
        else:
            messages.error(request, 'Please fill in all fields.')
            
            
    return render(request, 'home.html')




def about(request):
    return render(request, 'about.html')