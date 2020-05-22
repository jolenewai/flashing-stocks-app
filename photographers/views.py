from django.shortcuts import render, HttpResponse, get_object_or_404, redirect, reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import PhotographerForm, AvatarForm
from .models import Photographer

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
            messages.success(request, "Profile is not added due to an error, please try again")
            return render(request, 'photographers/create_profile.template.html', {
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
            messages.success(request, "Profile image is not updated due to an error, please try again")
            return render(request, 'photographers/upload_avatar.template.html', {
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
            messages.success(request, "Profile is not updated due to an error, please try again")
            update_form = PhotographerForm(request.POST, instance=profile)

            return render(request, 'photographers/update_profile.template.html', {
                'form': update_form
            })
    else: 
        update_form = PhotographerForm(instance=profile)

        return render(request, 'photographers/update_profile.template.html', {
            'form': update_form
        })
