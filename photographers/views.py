from django.shortcuts import render, HttpResponse, get_object_or_404, redirect, reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import PhotographerForm, AvatarForm, AlbumForm
from .models import Photographer, Album
from photos.models import Photo

# Create your views here.


def create_profile(request):

    if request.method == 'POST':

        create_form = PhotographerForm(request.POST)

        if create_form.is_valid():
            profile = create_form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, "Profile Added")
            return redirect(reverse(view_profile))
        else:
            messages.success(
                request,
                "Profile is not added due to an error, please try again"
            )
            return render(
                request,
                'photographers/create_profile.template.html', {
                    'form': create_form
                })
    else:

        form = PhotographerForm()

        return render(request, 'photographers/create_profile.template.html', {
            'form': form
        })


def upload_avatar(request):

    profile = Photographer.objects.get(user=request.user)

    form = AvatarForm(instance=profile)

    if request.method == 'POST':
        avatar_to_update = AvatarForm(
            request.POST,
            request.FILES,
            instance=profile
            )

        if avatar_to_update.is_valid():
            avatar_to_update.save()
            messages.success(request, "Profile image updated successfully")
            return redirect(reverse(view_profile))
        else:
            print(avatar_to_update.errors)
            messages.success(
                request,
                "Unable to update profile image"
            )
            return render(
                request,
                'photographers/upload_avatar.template.html', {
                    'form': form,
                    'profile': profile
                })
    else:

        return render(request, 'photographers/upload_avatar.template.html', {
            'form': form,
            'profile': profile
        })


def view_profile(request):

    user_info = request.user

    try:
        profile = Photographer.objects.get(user=request.user)
    except ObjectDoesNotExist:
        profile = None

    return render(request, 'photographers/view_profile.template.html', {
        'profile': profile,
        'user_info': user_info
    })


def update_profile(request):

    profile = Photographer.objects.get(user=request.user)

    if request.method == 'POST':

        update_form = PhotographerForm(request.POST, instance=profile)
        if update_form.is_valid():
            update_form.save()

            messages.success(request, "Profile updated successfully")
            return redirect(reverse(view_profile))
        else:
            messages.success(
                request,
                "Profile is not updated due to an error, please try again"
            )
            update_form = PhotographerForm(request.POST, instance=profile)

            return render(
                request,
                'photographers/update_profile.template.html', {
                    'form': update_form
                })
    else:
        update_form = PhotographerForm(instance=profile)

        return render(request, 'photographers/update_profile.template.html', {
            'form': update_form
        })


def view_uploads(request):

    photographer = Photographer.objects.get(user=request.user)

    try:
        uploads = Photo.objects.filter(owner=photographer)
    except ObjectDoesNotExist:
        uploads = None

    return render(request, 'photographers/view_uploads.template.html', {
        'photos': uploads
    })


def create_album(request):

    photographer = Photographer.objects.get(user=request.user)

    if request.method == 'POST':
        form = AlbumForm(request.POST)

        if form.is_valid():
            album_created = form.save(commit=False)
            album_created.owner = photographer
            album_created.save()
            form.save_m2m()
            messages.success(
                request,
                f"Album [{album_created.title}] created successfully"
            )
            return redirect(reverse(view_albums))
        else:
            messages.error(request, "Unable to create album")
            return render(
                request,
                'photographers/create_album.template.html', {
                    'form': form
                })

    form = AlbumForm()

    return render(request, 'photographers/create_album.template.html', {
        'form': form
    })


def view_albums(request):

    photographer = Photographer.objects.get(user=request.user)

    try:
        albums = Album.objects.filter(owner=photographer)
    except ObjectDoesNotExist:
        albums = None


    return render(
        request,
        'photographers/view_albums.template.html', {
            'albums': albums
        })


def edit_album(request, album_id):

    try:
        album = Album.objects.get(id=album_id)
    except ObjectDoesNotExist:
        album = None

    if request.method == 'POST':
        form = AlbumForm(request.POST, instance=album)

        if form.is_valid():
            updated_album = form.save()
            messages.success(
                request,
                f"Album [{updated_album.title}] updated successfully"
            )
            return redirect(reverse(view_albums))
        else:
            messages.error(request, "Unable to update album")
            return render(request, 'photographers/edit_album.template.html', {
                'form': form
            })

    form = AlbumForm(instance=album)

    return render(request, 'photographers/edit_album.template.html', {
        'form': form
    })


def delete_album(request, album_id):

    try:
        album = Album.objects.get(id=album_id)
    except ObjectDoesNotExist:
        album = None

    if request.method == 'POST':
        messages.success(request, f'Album [{album.title}] deleted')
        album.delete()
        return redirect(reverse(view_albums))
    else:
        messages.error(request, 'Unable to delete album')
        return redirect(reverse(view_albums))

    return redirect(reverse(view_albums))

