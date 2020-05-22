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
    avatar_url = profile.profile_img

    print(avatar_url)
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
                'form': form,
                'avatar_url': avatar_url
            })
    else:

        return render(request, 'photographers/upload_avatar.template.html', {
            'form': form,
            'avatar_url': avatar_url
        })



def set_profile_img_to_null(request):

    all_photographers = Photographer.objects.all()

    for p in all_photographers:
        print(p.profile_img)
        p.profile_img = Null

    return render(request, 'photographers/setnull_template.html')