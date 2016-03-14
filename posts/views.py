from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
# Create your views here.

from .models import Post
from .forms import PostForm


def post_list(request):
    queryset = Post.objects.all()
    context = {
        "queryset": queryset,
        "title": "First list"
    }
    return render(request, 'index.html', context)

def post_detail(request, id):
    #instance = Post.objects.get(id=121)
    instance = get_object_or_404(Post, id=id)
    context = {
        "instance": instance,
        "title": instance.title
    }
    return render(request, 'post_detail.html', context)

def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
    context = {
        'form': form,
    }

    return render(request, 'post_form.html', context)

def post_update(request):
    return HttpResponse("<h1>Update</h1>")

def post_delete(request):
    return HttpResponse("<h1>Delete</h1>")
