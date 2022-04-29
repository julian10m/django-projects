from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.views.generic import ListView
from django.db.models import Count
from .forms import EmailPostForm, CommentForm
from taggit.models import Tag
from .models import Post, Comment

POSTS_PER_PAGE = 3
NUMBER_OF_RELATED_POSTS_TO_DISPLAY = 4
class PostListView(ListView):
    # model = Post uses Post.objects.all()
    queryset = Post.published.all()
    # context_object_name = object_list  ...by default
    context_object_name = 'posts'
    paginate_by = POSTS_PER_PAGE
    # template_name = 'blog/post_list.html ...by default
    template_name = 'blog/post/list.html'

def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
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
                 {'posts': posts,
                  'tag': tag})

def post_detail(request, year, month, day, slug_title):

    post = get_object_or_404(Post, slug=slug_title,
                                   status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published \
        .filter(tags__in=post_tags_ids) \
        .exclude(id=post.id)
    similar_posts = similar_posts \
        .annotate(same_tags=Count('tags')) \
        .order_by('-same_tags', '-publish')[:NUMBER_OF_RELATED_POSTS_TO_DISPLAY]
    return render(request,
                'blog/post/detail.html',
                {'post': post,
                 'comments': comments,
                 'new_comment': new_comment,
                 'comment_form': comment_form,
                 'similar_posts': similar_posts,
                 })

def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"You should read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 
                                                    'form': form, 
                                                    'sent': sent,})