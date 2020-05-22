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
            return HttpResponse("Profile Added")
        else:
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
            return HttpResponse("Avatar Updated")
        else:
            print(avatar_to_update.errors)
            return render(request, 'photographers/upload_avatar.template.html', {
                'form': form
            })
    else:

        return render(request, 'photographers/upload_avatar.template.html', {
            'form': form
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

    update_form = PhotographerForm(instance=profile)

    return render(request, 'photographers/update_profile.template.html', {
        'form': update_form
    })
