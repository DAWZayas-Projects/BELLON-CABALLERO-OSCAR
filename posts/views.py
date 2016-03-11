from django.shortcuts import render
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
    context = {
        "title": "First list detail"
    }
    return render(request, 'index.html', context)

def post_create(request):
    return HttpResponse("<h1>Create</h1>")

def post_update(request):
    return HttpResponse("<h1>Update</h1>")

def post_delete(request):
    return HttpResponse("<h1>Delete</h1>")
