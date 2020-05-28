
from django.shortcuts import render, redirect
from .models import Contact 
from django.contrib import messages

def contact(request):
    if request.method == 'POST':
        fullname = request.POST['fullname']
        email = request.POST['email']
        message = request.POST['message']
        user_id = request.POST['user_id']
        
        contact = Contact(fullname=fullname, message=message, email=email, user_id=user_id)
        contact.save()
        messages.success(request, 'You have succesfully submitted your message. We will be in touch with you shortly')

        return redirect('index')