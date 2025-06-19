from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import BlogPost
from .forms import BlogPostForm

def blog(request):
    blogposts = BlogPost.objects.all().order_by('-date_created')
    return render(request, 'blog/blog.html', {'blogposts': blogposts})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def create_post(request):
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save()  # Save and get the BlogPost instance
            return redirect('view_post', pk=post.pk)  # Redirect to the view_post page
    else:
        form = BlogPostForm()
    return render(request, 'blog/create_post.html', {'form': form})


def view_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    return render(request, 'blog/view_post.html', {'post': post})