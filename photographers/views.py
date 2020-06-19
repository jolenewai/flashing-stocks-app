from django.shortcuts import render, redirect, reverse
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages
from .forms import PhotographerForm, AvatarForm, AlbumForm
from .models import Photographer, Album
from photos.models import Photo
from customers.models import Download


def check_user_in_group(user):
    # return True if user is in group photographer else return False
    photographer_group = Group.objects.get(name='photographers')
    if photographer_group in user.groups.all():
        return True
    else:
        return False


def get_photographer(user):
    # return profile object if found else return none
    try:
        profile = Photographer.objects.get(user=user)
    except ObjectDoesNotExist:
        profile = None

    return profile


def get_album(album_id):
    # return album object if found else return none
    try:
        album = Album.objects.get(id=album_id)
    except ObjectDoesNotExist:
        album = None

    return album


@login_required
def create_profile(request):
    # check if user is a photographer
    is_photographer = check_user_in_group(request.user)
    # if user is a photographer
    if is_photographer:
        # if form is submitted
        if request.method == 'POST':
            create_form = PhotographerForm(request.POST)
            # if form is validated
            if create_form.is_valid():
                # create an instance of the form without actually saving it
                profile = create_form.save(commit=False)
                # save logged in user as user
                profile.user = request.user
                # commit to database
                profile.save()
                messages.success(request, "Profile Added")
                return redirect(reverse(view_profile))
            # if form is not valid, display an error message
            else:
                messages.error(
                    request,
                    "Profile is not added due to an error, please try again"
                )
                return render(
                    request,
                    'photographers/create_profile.template.html', {
                        'form': create_form
                    })
        # if form is not submitted, render an empty form
        else:

            form = PhotographerForm()
            return render(
                request,
                'photographers/create_profile.template.html', {
                    'form': form
                })
    # if user is not a photographer
    else:
        raise PermissionDenied


@login_required
def upload_avatar(request):

    # check if user is a photographer
    is_photographer = check_user_in_group(request.user)

    # if user is a photographer
    if is_photographer:
        # get photographer profile
        profile = get_photographer(request.user)

        # create form object with profile
        form = AvatarForm(instance=profile)

        # if form is submitted
        if request.method == 'POST':
            # get data from posted form
            avatar_to_update = AvatarForm(
                request.POST,
                request.FILES,
                instance=profile
                )

            # update avatar field with image url to profile if form is valid
            if avatar_to_update.is_valid():
                avatar_to_update.save()
                messages.success(request, "Profile image updated successfully")
                return redirect(reverse(view_profile))
            # if form is not valid, render the form again with error message
            else:
                print(avatar_to_update.errors)
                messages.success(
                    request,
                    "Unable to update profile image"
                )
                return render(
                    request,
                    'photographers/upload_avatar.template.html',
                    {
                        'form': form,
                        'profile': profile
                    })
        # if form is not submitted, render form with data from database
        else:
            return render(
                request,
                'photographers/upload_avatar.template.html',
                {
                    'form': form,
                    'profile': profile
                })
    # deny access if user is not a photographer
    else:
        raise PermissionDenied


@login_required
def view_profile(request):

    # check if user is a photographer
    is_photographer = check_user_in_group(request.user)

    # if user is a photographer
    if is_photographer:

        user_info = request.user
        # get photographer profile
        profile = get_photographer(user_info)

        # if profile is not exist, redirect user to create profile page
        if profile is None:
            return redirect(reverse('photographer_create_profile'))
        else:
            return render(
                request,
                'photographers/view_profile.template.html',
                {
                    'profile': profile,
                    'user_info': user_info
                })
    # deny access if user is not a photographer
    else:
        raise PermissionDenied


@login_required
def update_profile(request):
    # check if user is a photographer
    is_photographer = check_user_in_group(request.user)

    # if user is a photographer
    if is_photographer:

        # get photographer profile
        profile = get_photographer(user_info)

        # if form is submitted
        if request.method == 'POST':
            # get data from posted form object
            update_form = PhotographerForm(request.POST, instance=profile)
            # save to database if form is valid
            if update_form.is_valid():
                update_form.save()
                messages.success(request, "Profile updated successfully")
                return redirect(reverse(view_profile))
            # if form is not valid, render the form with error message
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
        # if form is not submitted, render form with data from database
        else:
            update_form = PhotographerForm(instance=profile)

            return render(request, 'photographers/update_profile.template.html', {
                'form': update_form
            })
    # deny access if user is not a photographer
    else:
        raise PermissionDenied


@login_required
def view_uploads(request):
    # check if user is a photographer
    is_photographer = check_user_in_group(request.user)

    # if user is a photographer
    if is_photographer:
        # get photographer object
        photographer = get_photographer(request.user)

        # filter uploads by this photographer
        try:
            uploads = Photo.objects.filter(owner=photographer)
        except ObjectDoesNotExist:
            uploads = None

        return render(request, 'photographers/view_uploads.template.html', {
            'photos': uploads
        })
    # deny access if user is not a photographer
    else:
        raise PermissionDenied


@login_required
def create_album(request):
    # check if user is a photographer
    is_photographer = check_user_in_group(request.user)

    # if user is a photographer
    if is_photographer:

        # get user profile
        photographer = get_photographer(request.user)

        # if form is submitted
        if request.method == 'POST':
            # get data from posted form object
            form = AlbumForm(request.POST)

            # commit data to database if form is valid
            if form.is_valid():
                album_created = form.save(commit=False)
                # save logged in user as owner
                album_created.owner = photographer
                album_created.save()
                # to save many-to-many field
                form.save_m2m()
                messages.success(
                    request,
                    f"Album [{album_created.title}] created successfully"
                )
                return redirect(reverse(view_albums))
            # if form is not valid, render the form with error message
            else:
                messages.error(request, "Unable to create album")
                return render(
                    request,
                    'photographers/create_album.template.html', {
                        'form': form
                    })
        # if form is not submitted, render an empty form
        form = AlbumForm()

        return render(request, 'photographers/create_album.template.html', {
            'form': form
        })
    # deny access if user is not a photographer
    else:
        raise PermissionDenied


@login_required
def view_albums(request):
    # check if user is a photographer
    is_photographer = check_user_in_group(request.user)

    # if user is a photographer
    if is_photographer:

        # get user profile
        photographer = get_photographer(request.user)

        # get albums created by logged in user
        try:
            albums = Album.objects.filter(owner=photographer)
        except ObjectDoesNotExist:
            albums = None

        return render(
            request,
            'photographers/view_albums.template.html', {
                'albums': albums
            })
    # deny access if user is not a photographer
    else:
        raise PermissionDenied


@login_required
def edit_album(request, album_id):
    # check if user is a photographer
    is_photographer = check_user_in_group(request.user)

    # if user is a photographer
    if is_photographer:

        # get album object of the specified album_id
        album = get_album(album_id)

        # if form is submitted
        if request.method == 'POST':
            # get data from posted form object
            form = AlbumForm(request.POST, instance=album)

            # save to database if form is valid
            if form.is_valid():
                updated_album = form.save()
                messages.success(
                    request,
                    f"Album [{updated_album.title}] updated successfully"
                )
                return redirect(reverse(view_albums))
            # if form is not valid, render form with error message
            else:
                messages.error(request, "Unable to update album")
                return render(request, 'photographers/edit_album.template.html', {
                    'form': form
                })
        # if form is not submitted, render form with data from database
        form = AlbumForm(instance=album)

        return render(request, 'photographers/edit_album.template.html', {
            'form': form
        })
    # deny access if user is not a photographer
    else:
        raise PermissionDenied


@login_required
def delete_album(request, album_id):
    # check if user is a photographer
    is_photographer = check_user_in_group(request.user)

    # if user is a photographer
    if is_photographer:
        # get album of specified album_id
        album = get_album(album_id)

        # if form is submitted
        if request.method == 'POST':
            if album:
                messages.success(request, f'Album [{album.title}] deleted')
                album.delete()
            else:
                messages.error(request, 'Invalid album id')
            return redirect(reverse(view_albums))
        else:
            messages.error(request, 'Unable to delete album')
            return redirect(reverse(view_albums))

        return redirect(reverse(view_albums))
    else:
        raise PermissionDenied


def public_profile(request, photographer_id):

    # get photographer by photographer_id
    try:
        photographer = Photographer.objects.get(id=photographer_id)
    except ObjectDoesNotExist:
        photographer = None

    # if photographer exists
    if photographer:
        # fitler photos uploaded by specified photographer
        photos_by_photographer = Photo.objects.filter(owner=photographer_id)
        # count no of results
        photos_count = photos_by_photographer.count()
    # to handle invalid photographer id entered by user
    else:
        messages.error(request, 'Invalid photographer id')
        return redirect(reverse('list_photos'))

    return render(request, 'photographers/public_profile.template.html', {
        'photographer': photographer,
        'photos': photos_by_photographer,
        'photos_count': photos_count
    })


@login_required
def view_downloads(request):
    # check if user is a photographer
    is_photographer = check_user_in_group(request.user)

    # if photographer exists
    if is_photographer:

        photographer = get_photographer(request.user)
        # filter downloads of photo owned by this photographer
        downloads = Download.objects.filter(image__owner=photographer)
        # count no of downloads
        download_count = downloads.count()

        return render(request, 'photographers/view_downloads.template.html', {
            'downloads': downloads,
            'download_count': download_count
        })
    # deny access if user is not a photographer
    else:
        raise PermissionDenied
