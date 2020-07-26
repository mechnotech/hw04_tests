from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Group, Post, User


def get_paginated_view(request, post_list, page_size=10):
    paginator = Paginator(post_list, page_size)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return page, paginator


def index(request):
    post_list = Post.objects.order_by("-pub_date").all()
    page, paginator = get_paginated_view(request, post_list)
    return render(request, 'index.html',
                  {'page': page, 'paginator': paginator})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.order_by('-pub_date').all()
    page, paginator = get_paginated_view(request, post_list)
    return render(request, 'group.html',
                  {'group': group, 'page': page, 'paginator': paginator})


@login_required
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            return redirect('index')
        return render(request, 'new_post.html', {'form': form})

    form = PostForm()
    return render(request, 'new_post.html', {'form': form})


def profile(request, username):
    author = get_object_or_404(User, username=username)
    post_list = author.posts.order_by('-pub_date').all()
    page, paginator = get_paginated_view(request, post_list)
    return render(request, "profile.html",
                  {'page': page, 'paginator': paginator, 'author': author})


def post_view(request, username, post_id):
    author = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, pk=post_id, author=author)
    return render(request, "post.html", {'post': post, 'author': author})


def post_edit(request, username, post_id):
    user = get_object_or_404(User, username=username)
    if request.user != user:
        return redirect('post_detail', username=username, post_id=post_id)
    post = get_object_or_404(Post, author=user, pk=post_id)

    form = PostForm(request.POST or None, files=request.FILES or None,
                    instance=post)

    if request.method == 'POST':
        #form = PostForm(request.POST, instance=post)

        if form.is_valid():
            form.save()
            return redirect('post_detail', username=username, post_id=post.pk)

        return render(request, "new_post.html", {'form': form, 'post': post})


    return render(request, "new_post.html", {'form': form, 'post': post})


def page_not_found(request, exception):
    return render(request, "misc/404.html", {"path": request.path}, status=404)


def server_error(request):
    return render(request, "misc/500.html", status=500)
