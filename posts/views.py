from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
# Create your views here.

from .models import Post

def post_list(request):
    queryset = Post.objects.all()
    context = {
        "queryset": queryset,
        "title": "First list"
    }
    return render(request, 'index.html', context)

def post_detail(request):
    #instance = Post.objects.get(id=121)
    instance = get_object_or_404(Post, id=3)
    context = {
        "instance": instance,
        "title": instance.title
    }
    return render(request, 'post_detail.html', context)

def post_create(request):
    return HttpResponse("<h1>Create</h1>")

def post_update(request):
    return HttpResponse("<h1>Update</h1>")

def post_delete(request):
    return HttpResponse("<h1>Delete</h1>")
