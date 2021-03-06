from django.shortcuts import render, redirect
from django.views.generic import View,CreateView

from .models import Post,Tag
from .utils import ObjectDetailMixin, ObjectCreateMixin, ObjectUpdateMixin, ObjectDeleteMixin
from .forms import TagForm,PostForm,CreateUserForm,CommentForm
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

def search(request):
    search_query = request.GET.get('search', '')
    if search_query:
        posts = Post.objects.filter(Q(title__icontains=search_query) | Q(body__icontains=search_query))
    else:
        posts = Post.objects.all()
    return posts

def posts_list(request):
    posts = search(request)
    tags = Tag.objects.all()[:5]

    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    is_paginated = page.has_other_pages()
    if page.has_previous():
        prev_page_url = '?page={}'.format(page.previous_page_number())
    else:
        prev_page_url=''

    if page.has_next():
        next_page_url = '?page={}'.format(page.next_page_number())
    else:
        next_page_url=''
    print(page.object_list)
    context = {
        'page_obj': page,
        'is_paginated': is_paginated,
        'next_page_url': next_page_url,
        'prev_page_url':prev_page_url,
        'tags': tags
    }

    return render(request,'xforum/index.html', context=context)

class PostDetail(ObjectDetailMixin,View):
    form_class = CommentForm
    model = Post
    template = 'xforum/post_detail.html'

class PostCreate(ObjectCreateMixin,View):
    model_form = PostForm
    template = 'xforum/post_create.html'

class PostUpdate(ObjectUpdateMixin, View):
    model = Post
    model_form = PostForm
    template = 'xforum/post_update.html'

class PostDelete(ObjectDeleteMixin,View):
    model = Post
    model_form = PostForm
    template = 'xforum/post_delete.html'
    redirect_url  = 'posts_list_url'

def tags_list(request):
    tags = Tag.objects.order_by('title')
    return render(request, 'xforum/tags_list.html', context={'tags':tags})

class TagDetail(ObjectDetailMixin,View):
    model = Tag
    template = 'xforum/tag_detail.html'

class TagCreate(ObjectCreateMixin,View):
    model_form = TagForm
    template = 'xforum/tag_create.html'

class TagUpdate(ObjectUpdateMixin, View):
    model = Tag
    model_form = TagForm
    template = 'xforum/tag_update.html'

class TagDelete(ObjectDeleteMixin,View):
    model = Tag
    model_form = PostForm
    template = 'xforum/tag_delete.html'
    redirect_url  = 'tags_list_url'

def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('login_url')
    context = {'form':form}
    return render(request, 'xforum/register_form.html', context)

def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username = username,password = password)

        if user is not None:
            login(request, user)
            return redirect('posts_list_url')
        else:
            messages.info(request, 'Username Or password incorect')
    context = {}
    return render(request,'xforum/login_form.html', context)

def logoutUser(request):
    logout(request)
    return redirect('posts_list_url')
