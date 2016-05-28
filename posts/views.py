from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from urllib import quote_plus

# Create your views here.

from .models import Post
from .forms import PostForm


def post_list(request):
    queryset_list = Post.objects.all()
    #queryset = Post.objects.all().order_by("-timestamp")

    paginator = Paginator(queryset_list, 2) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    context = {
        "queryset": queryset,
        "queryset_list_len": len(queryset_list),
        "title": "All posts"
    }
    return render(request, 'post_list.html', context)
    
@login_required
def my_posts(request):
    
    username = request.user.id
    queryset_list = Post.objects.filter(user=username)
    
    paginator = Paginator(queryset_list, 2) # Show 25 contacts per page

    page = request.GET.get('page')
    queryset = queryset_list
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)
        
    context = {
        "queryset": queryset,
        "queryset_list_len": len(queryset_list),
        "title": "Your posts"
    }
    return render(request, 'post_list.html', context)

def post_detail(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    absolute_url = request.build_absolute_uri
    share_url = quote_plus(instance.content)
    context = {
        "instance": instance,
        "title": instance.title,
        "absolute_url": absolute_url,
        "share_url": share_url
    }
    return render(request, 'post_detail.html', context)

def post_create(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request, "Successfully created new post")
        return HttpResponseRedirect(instance.get_absolute_url())
    submit_button = 'Create'
    context = {
        'form': form,
        'submit_button': submit_button,
    }

    return render(request, 'post_form.html', context)

def post_update(request, slug=None):

    instance = get_object_or_404(Post, slug=slug)

    if instance.user != request.user:
        raise Http404

    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Successfully updated post: " + instance.title)
        return HttpResponseRedirect(instance.get_absolute_url())
    submit_button = 'Update'
    context = {
        "title": instance.title,
        "instance": instance,
        'form': form,
        'submit_button': submit_button,
    }
    return render(request, 'post_form.html', context)

def post_delete(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)

    if instance.user != request.user:
        raise Http404

    instance.delete()
    return redirect("posts:list")
