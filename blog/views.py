from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.forms import formset_factory

from blog import forms, models


# Create your views here.
@login_required
@permission_required('blog/add_photo', raise_exception=True)
def photo_upload(request):
    form = forms.PhotoForm()
    if request.method == "POST":
        form = forms.PhotoForm(request.POST, request.FILES)
        photo = form.save(commit=False)
        photo.uploader = request.user
        photo.save()
        return redirect('home')
    return render(request, "blog/photo_upload.html", context={'form': form})



@login_required
def home(request):
    photos = models.Photo.objects.all()
    blogs = models.Blog.objects.all()

    context = {
        'photos': photos,
        'blogs': blogs
    }
    return render(request, 'blog/home.html', context=context)


@login_required
def blog_and_photo_upload(request):
    blog_form = forms.BlogForm()
    photo_form = forms.PhotoForm()
    if request.method == "POST":
        blog_form = forms.BlogForm(request.POST)
        photo_form = forms.PhotoForm(request.POST, request.FILES)
        if all([blog_form.is_valid(), photo_form.is_valid()]):
            photo = photo_form.save(commit=False)
            photo.uploader = request.user
            photo.save()
            blog = blog_form.save(commit=False)
            blog.author = request.user
            blog.photo = photo
            blog.save()
            blog.contributors.add(request.user, through_defaults={'contribution': 'Auteur principal'})
            return redirect('home')

    context = {
        'blog_form': blog_form,
        'photo_form': photo_form,
    }
    return render(request, 'blog/create_blog_post.html', context=context)


@login_required
def view_blog(request, blog_id):
    blog = get_object_or_404(models.Blog, id=blog_id)
    return render(request, 'blog/view_blog.html', {'blog': blog})

@login_required
def edit_blog(request, blog_id):
    blog = get_object_or_404(models.Blog, id=blog_id)
    photo = get_object_or_404(models.Photo, id=blog.photo.id)
    edit_form = forms.BlogForm(instance=blog)
    delete_form = forms.DeleteBlogForm()
    if request.method == 'POST':
        if 'edit_blog' in request.POST:
            edit_form = forms.BlogForm(request.POST, instance=blog)
            if edit_form.is_valid():
                edit_form.save()
                return redirect('home')
        if 'delete_blog' in request.POST:
            delete_form = forms.DeleteBlogForm(request.POST)
            if delete_form.is_valid():
                blog.delete()
                photo.delete()
                return redirect('home')

    context = {
        'edit_form': edit_form,
        'delete_form': delete_form,
    }
    return render(request, 'blog/edit_blog.html', context=context)

@login_required
def create_multiple_photos(request):
    PhotoFormset = formset_factory(forms.PhotoForm, extra=5)
    formset = PhotoFormset()
    if request.method == 'POST':
        formset = PhotoFormset(request.POST, request.FILES)
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data:
                    photo = form.save(commit=False)
                    photo.uploader = request.user
                    photo.save()
            return redirect('home')
    return render(request, 'blog/create_multiple_photos.html', {'formset': formset})


@login_required
def follow_users(request):
    form = forms.FollowUsersForm(instance=request.user)
    if request.method == "POST":
        form = forms.FollowUsersForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'blog/follow_user_form.html', context={'form': form})
