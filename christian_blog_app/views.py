from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.views import generic
from .models import Post, Comment, Post, Article, Prayer
from .forms import CommentForm
import re
from django.views.generic.base import TemplateView
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm,
)
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect, QueryDict
from django.shortcuts import resolve_url
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.http import (
    url_has_allowed_host_and_scheme, urlsafe_base64_decode,
)
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic.edit import FormView
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect, HttpResponse,QueryDict
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from xml.dom import minidom
from django.db.models import Count
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
import smtplib
from christian_blog.settings import EMAIL_HOST_USER
from .import forms
            
fromaddr='django.registeractivate@gmail.com'
username='django.registeractivate'
password='django_register_activate'


# Create your views here.
class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-published_date')
    template_name = 'index.html'

def testing(request):
    return render(request, 'blog/testing.html')
def index(request):
    post = Post.objects.all()
    paginator = Paginator(post, 3)
    page = request.GET.get('page')
    page_post = paginator.get_page(page)

    context = {
        'post': page_post
    }
    return render(request, 'blog/index.html', context)

def dashboard(request):
    post = Post.objects.all()
    context = {
        'post': post
    }
    return render(request, 'blog/dashboard.html', context)

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('dashboard')
        else:
            messages.error(request, "Incorrect username or password")
            return redirect('login')
    else:
        return render(request, 'blog/login.html')

def post_detail(request, slug):
    template_name = 'post_detail.html'
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True)
    new_comment = None
    #Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()
        context = {'post': post,
                'comments': comments,
                'new_comment': new_comment,
                'comment_form': comment_form}

    return render(request, 'blog/post_detail.html', context)


def posts(request):
    return render(request, 'blog/post.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You have logged out successfully')
        return redirect('index')

def articles(request):
    if request.method == 'POST':
        author = request.POST['author']
        title = request.POST['title']
        article = request.POST['article']

        articles = Article(author=author, title=title, article=article)
        articles.save()
        messages.success(request, "You have successfully submitted your article for review. We will get back to you soon!")
        return redirect ('dashboard')
    else:
        return render(request, 'blog/post.html')
          
def prayers(request):
    if request.method == 'POST':
        username = request.POST['username']
        prayer = request.POST['prayer']

        prayers = Prayer(username=username, prayer= prayer)
        prayers.save()
        messages.success(request, "We have received your prayer requests and will join you in prayers")
        return redirect('dashboard')
    else:
        return render(request, 'blog/prayer_request.html')


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password']

        if password  == password2:
            
            if re.search('[A-Z]', password)!=None and re.search('[0-9]', password)!=None and re.search('[^A-Za-z0-9]', password)!=None:
                print('Strong Password')

            if User.objects.filter(username=username).exists():
                messages.error(request, 'username already exists')
                return redirect('register')
            else:
                user = User.objects.create_user(first_name=first_name, last_name = last_name, username=username, email=email, 
                                                password=password)
                user.save()
                id=user.id
                subject = 'Welcome to LifeStream'
                message= '"Hi!\nHow are you?\nHere is the link to activate your account:\nhttp://127.0.0.1:8005/blog/activation/?id=%s" %(id)'
                recipient = str(user.email)
                send_mail(subject, message, EMAIL_HOST_USER, [recipient], fail_silently=False)
                return render(request,'blog/thankyou.html')
    
                #messages.success(request, 'Registration successful! You can now login!')
                #return redirect('login')
        else:
            messages.error(request, 'passwords do not match')
            return redirect('register')
    else:
        return render(request, 'blog/register.html')

    

class PasswordContextMixin:
    extra_context = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title,
            **(self.extra_context or {})
        })
        return context


class PasswordChangeDoneView(PasswordContextMixin, TemplateView):
    template_name = 'registration/password_change_done.html'
    title = _('Password change successful')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class PasswordChangeView(PasswordContextMixin, FormView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('password_change_done')
    template_name = 'registration/password_change_form.html'
    title = _('Password change')

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        # Updating the password logs out all other sessions for the user
        # except the current one.
        update_session_auth_hash(self.request, form.user)
        return super().form_valid(form)

class PasswordResetConfirmView(PasswordContextMixin, FormView):
    form_class = SetPasswordForm
    post_reset_login = False
    post_reset_login_backend = None
    reset_url_token = 'set-password'
    success_url = reverse_lazy('password_reset_complete')
    template_name = 'registration/password_reset_confirm.html'
    title = _('Enter new password')
    token_generator = default_token_generator

    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        assert 'uidb64' in kwargs and 'token' in kwargs

        self.validlink = False
        self.user = self.get_user(kwargs['uidb64'])

        if self.user is not None:
            token = kwargs['token']
            if token == self.reset_url_token:
                session_token = self.request.session.get(INTERNAL_RESET_SESSION_TOKEN)
                if self.token_generator.check_token(self.user, session_token):
                    # If the token is valid, display the password reset form.
                    self.validlink = True
                    return super().dispatch(*args, **kwargs)
            else:
                if self.token_generator.check_token(self.user, token):
                    # Store the token in the session and redirect to the
                    # password reset form at a URL without the token. That
                    # avoids the possibility of leaking the token in the
                    # HTTP Referer header.
                    self.request.session[INTERNAL_RESET_SESSION_TOKEN] = token
                    redirect_url = self.request.path.replace(token, self.reset_url_token)
                    return HttpResponseRedirect(redirect_url)

        # Display the "Password reset unsuccessful" page.
        return self.render_to_response(self.get_context_data())

    def get_user(self, uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist, ValidationError):
            user = None
        return user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.user
        return kwargs

    def form_valid(self, form):
        user = form.save()
        del self.request.session[INTERNAL_RESET_SESSION_TOKEN]
        if self.post_reset_login:
            auth_login(self.request, user, self.post_reset_login_backend)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.validlink:
            context['validlink'] = True
        else:
            context.update({
                'form': None,
                'title': _('Password reset unsuccessful'),
                'validlink': False,
            })
        return context     



class PasswordResetCompleteView(PasswordContextMixin, TemplateView):
    template_name = 'registration/password_reset_complete.html'
    title = _('Password reset complete')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_url'] = resolve_url(settings.LOGIN_URL)
        return context

def activate(request):
	id=int(request.GET.get('id'))
	user = User.objects.get(id=id)
	user.is_active=True
	user.save()
	return render(request,'activation.html')
    
def send_email(toaddr,id):
	text = "Hi!\nHow are you?\nHere is the link to activate your account:\nhttp://127.0.0.1:8005/blog/activation/?id=%s" %(id)
	# Record the MIME types of both parts - text/plain and text/html.
	part1 = MIMEText(text, 'plain')
	msg = MIMEMultipart('alternative')
	msg.attach(part1)
	subject="Activate your account at Family Host"
	msg="""\From: %s\nTo: %s\nSubject: %s\n\n%s""" %(fromaddr,toaddr,subject,msg.as_string())
	#Use gmail's smtp server to send email. However, you need to turn on the setting "lesssecureapps" following this link:
	#https://www.google.com/settings/security/lesssecureapps
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.ehlo()
	server.starttls()
	server.login(username,password)
	server.sendmail(fromaddr,[toaddr],msg)
	server.quit()