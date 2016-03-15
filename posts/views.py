from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
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
    instance = get_object_or_404(Post, id=id)
    context = {
        "instance": instance,
        "title": instance.title
    }
    return render(request, 'post_detail.html', context)

def post_create(request):
    form = create_form(request)
    submit_button = 'Create'
    context = {
        'form': form,
        'submit_button': submit_button,
    }

    return render(request, 'post_form.html', context)

def post_update(request, id):
    instance = get_object_or_404(Post, id=id)
    form = create_form(request, instance)
    submit_button = 'Update'
    context = {
        "title": instance.title,
        "instance": instance,
        'form': form,
        'submit_button': submit_button,
    }
    return render(request, 'post_form.html', context)

def post_delete(request, id):
    instance = get_object_or_404(Post, id=id)
    instance.delete()
    return redirect("posts:list")

def create_form(request, instance = None):
    form = PostForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())
    return form