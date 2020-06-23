from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.http import HttpResponse
from .models import Topic, Post
from .forms import PostForm

def topic_list(request):
	topics=Topic.objects.all()
	return render(request, 'blog/topic_list.html', {'topics':topics} )


def topic_detail(request, pk):
    try:
        topics=Topic.objects.all()
        topic= Topic.objects.get(pk=pk)
        posts=Post.objects.filter(topic__pk=pk)
    except posts.DoesNotExist:
        raise Http404
    return render(request, 'blog/topic_detail.html', {'posts': posts,'topics':topics})


def post_edit(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('topic_detail', pk=topic.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def myblog(request):
	topics=Topic.objects.all()
	return render(request, 'blog/myblog.html', {'topics':topics} )


