from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post

def post_list(request):
    POSTS_PER_PAGE = 3
    object_list = Post.published.all()
    paginator = Paginator(object_list, POSTS_PER_PAGE)
    page = request.GET.get('page') # current page number
    try:
        posts = paginator.page(page) # objects for current page
    except PageNotAnInteger: # if number is weird, then give the first
        posts = paginator.page(1)
    except EmptyPage: # if it exceeds the max, then set the last one
        posts = paginator.page(paginator.num_pages)
    return render(request, 
                 'blog/post/list.html', 
                 {'posts': posts})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                                   status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)
    return render(request,
                'blog/post/detail.html',
                {'post': post})