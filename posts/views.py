from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Group, Post, User


def get_one_page(request, post_list, rec_per_page=10):
    paginator = Paginator(post_list, rec_per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return page, paginator


def index(request):
    post_list = Post.objects.order_by("-pub_date").all()
    page, paginator = get_one_page(request, post_list)
    return render(request, 'index.html',
                  {'page': page, 'paginator': paginator})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.order_by('-pub_date').all()
    page, paginator = get_one_page(request, post_list)
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
    user = get_object_or_404(User, username=username)
    post_list = user.posts.order_by('-pub_date').all()
    page, paginator = get_one_page(request, post_list)
    return render(request, "profile.html",
                  {'page': page, 'paginator': paginator, 'author': user})


def post_view(request, username, post_id):
    user = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, pk=post_id, author=user)
    counter = user.posts.count()
    return render(request, "post.html",
                  {'post': post, 'counter': counter, 'author': user})


def post_edit(request, username, post_id):
    user = get_object_or_404(User, username=username)

    if request.user != user:
        return redirect('post', username=username, post_id=post_id)

    post = get_object_or_404(Post, author=user, pk=post_id)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save(commit=True)

            return redirect('post', username=username, post_id=post.pk)
        return render(request, "new_post.html", {'form': form, 'post': post})

    form = PostForm(instance=post)
    return render(request, "new_post.html", {'form': form, 'post': post})
