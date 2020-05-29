from django.shortcuts import render, HttpResponse, get_object_or_404, redirect, reverse
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages
from .forms import PhotographerForm, AvatarForm, AlbumForm
from .models import Photographer, Album
from photos.models import Photo
from customers.models import Download

# Create your views here.

def check_user_in_group(user):

    photographer_group = Group.objects.get(name='photographers')
    if photographer_group in user.groups.all():
        return True
    else:
        return False



@login_required
def create_profile(request):

    is_photographer = check_user_in_group(request.user)
    if is_photographer:
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
    else:
        raise PermissionDenied


@login_required
def upload_avatar(request):

    is_photographer = check_user_in_group(request.user)
    if is_photographer:

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
    else:
        raise PermissionDenied


@login_required
def view_profile(request):

    is_photographer = check_user_in_group(request.user)
    if is_photographer:

        user_info = request.user

        try:
            profile = Photographer.objects.get(user=request.user)
        except ObjectDoesNotExist:
            profile = None
        
        if profile is None:
            return redirect(reverse('photographer_create_profile'))
        else:
            return render(request, 'photographers/view_profile.template.html', {
                'profile': profile,
                'user_info': user_info
            })
    else:
        raise PermissionDenied


@login_required
def update_profile(request):

    is_photographer = check_user_in_group(request.user)
    if is_photographer:

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
    else:
        raise PermissionDenied


@login_required
def view_uploads(request):

    is_photographer = check_user_in_group(request.user)

    if is_photographer:
        photographer = Photographer.objects.get(user=request.user)

        try:
            uploads = Photo.objects.filter(owner=photographer)
        except ObjectDoesNotExist:
            uploads = None

        return render(request, 'photographers/view_uploads.template.html', {
            'photos': uploads
        })
    else:
        raise PermissionDenied


@login_required
def create_album(request):

    is_photographer = check_user_in_group(request.user)

    if is_photographer:
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
    else:
        raise PermissionDenied


@login_required
def view_albums(request):

    is_photographer = check_user_in_group(request.user)

    if is_photographer:

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
    else:
        raise PermissionDenied


@login_required
def edit_album(request, album_id):

    is_photographer = check_user_in_group(request.user)

    if is_photographer:
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
    else:
        raise PermissionDenied


@login_required
def delete_album(request, album_id):

    is_photographer = check_user_in_group(request.user)

    if is_photographer:
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
    else:
        raise PermissionDenied


def public_profile(request, photographer_id):
 
    photographer = Photographer.objects.get(id=photographer_id)
    photos_by_photographer = Photo.objects.filter(owner=photographer_id)
    photos_count = photos_by_photographer.count()

    return render(request, 'photographers/public_profile.template.html', {
        'photographer': photographer,
        'photos': photos_by_photographer,
        'photos_count': photos_count
    })


@login_required
def view_downloads(request):

    is_photographer = check_user_in_group(request.user)

    if is_photographer:

        photographer = Photographer.objects.get(user=request.user)
        downloads = Download.objects.filter(image__owner=photographer)
        download_count = downloads.count()

        return render(request, 'photographers/view_downloads.template.html', {
            'downloads': downloads,
            'download_count': download_count
        })

    else:
        raise PermissionDenied