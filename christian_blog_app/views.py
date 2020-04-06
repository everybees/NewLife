from django.shortcuts import render, redirect

# Create your views here.

def posts(request):
    return render(request, 'blog/index.html')
