from django.shortcuts import render , get_object_or_404 , redirect
from blog.models import Post 
from blog.forms import CommentForm
from django.utils import timezone
import logging
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django.urls import reverse
# Create your views here.

logger = logging.getLogger(__name__)


def index(request):
  posts = Post.objects.filter(published_at__lte=timezone.now()).select_related("author")
  logger.debug("Got %d posts", len(posts))
  logger.debug("Got %d posts" % len(posts))
  return render(request,"blog/index.html",{"posts":posts})

def post_table(request):
  return render(request, "blog/post-table.html",{"post_list_url":reverse("post-list")})

def post_detail(request,slug):
  post = get_object_or_404(Post,slug=slug)
  if request.user.is_active:
        if request.method == "POST":
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)

                logger.info("Created comment on Post %d for user %s", post.pk, request.user)
                comment.content_object = post
                comment.creator = request.user
                comment.save()
                return redirect(request.path_info)
        else:
          comment_form=CommentForm()
  else:
    comment_form=None
  return render(request,"blog/post-detail.html",{'post':post,"comment_form":comment_form})

def get_ip(request):
  from django.http import HttpResponse
  return HttpResponse(request.META["REMOTE_ADDR"])