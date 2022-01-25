from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View
from . import forms, models


User = get_user_model()


class MainPageView(View):
    """Представление главной страницы"""

    def get(self, request):
        return render(request=request, template_name='main_page.html')


class UserRegistrationView(View):
    """Представление страницы регистрации"""

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('main_page')
        form = forms.RegisterForm()
        return render(
            request=request,
            template_name='registration.html',
            context={'form': form},
        )

    def post(self, request):
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data.get('firstname')
            user.last_name = form.cleaned_data.get('lastname')
            user.save()
            models.Profile.objects.create(user=user)
            models.Blog.objects.create(user=user)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('main_page')

        return render(
            request=request,
            template_name='registration.html',
            context={'form': form},
        )


class UserLoginView(LoginView):
    """Представлнеие страцины авторизации"""

    template_name = 'login.html'
    redirect_authenticated_user = True
    form_class = forms.UserLoginForm


class UserBlogView(View):
    """Представление страницы блога"""

    def get(self, request, username):
        owner = User.objects.get_by_natural_key(username)
        owner_blog = owner.blog
        blog_posts = owner_blog.blog_posts.filter(delete_date__isnull=True)
        is_owner = request.user == owner
        add_post_form = forms.AddPostForm() if is_owner else None

        return render(
            request=request,
            template_name='user_blog.html',
            context={
                'is_owner': is_owner,
                'user_blog': owner_blog,
                'blog_posts': blog_posts,
                'add_post_form': add_post_form,
                'owner_username': username,
            },
        )

    def post(self, request, username):
        print(request.POST)
        if 'delete' in request.POST:
            blog_post_id = request.POST.get('delete')
            blog_post = models.BlogPost.objects.get(id=blog_post_id)
            blog_post.delete_date = timezone.now()
            blog_post.save()

            return redirect(request.path_info)

        owner = User.objects.get_by_natural_key(username)
        owner_blog = owner.blog
        add_post_form = forms.AddPostForm(request.POST)

        if add_post_form.is_valid():
            models.BlogPost.objects.create(
                blog=owner_blog,
                text=add_post_form.cleaned_data.get('text'),
            )

            owner_blog.save()

            return redirect(request.path_info)

        blog_posts = owner_blog.blog_posts.filter(delete_date__isnull=True)
        is_owner = request.user == owner
        return render(
            request=request,
            template_name='user_blog.html',
            context={
                'is_owner': is_owner,
                'user_blog': owner_blog,
                'blog_posts': blog_posts,
                'add_post_form': add_post_form,
                'owner_username': username,
            },
        )


class PersonalAccountView(LoginRequiredMixin, View):
    """Представление страницы личного кабинета"""

    def get(self, request):
        user = request.user
        user_blog = user.blog
        user_profile = user.profile
        deleted_blog_posts = user_blog.blog_posts.filter(delete_date__isnull=False).order_by('-delete_date')
        deleted_blog_posts_total = deleted_blog_posts.count()

        return render(
            request=request,
            template_name='personal_account.html',
            context={
                'user': user,
                'user_profile': user_profile,
                'deleted_blog_posts': deleted_blog_posts,
                'deleted_blog_posts_total': deleted_blog_posts_total,
            },
        )

    def post(self, request):
        if 'restore' in request.POST:
            blog_post_id = request.POST.get('restore')
            blog_post = models.BlogPost.objects.get(id=blog_post_id)
            blog_post.delete_date = None
            blog_post.save()

            return redirect(request.path_info)

        if 'hard-delete' in request.POST:
            blog_post_id = request.POST.get('hard-delete')
            blog_post = models.BlogPost.objects.get(id=blog_post_id)
            blog_post.delete()

            return redirect(request.path_info)
