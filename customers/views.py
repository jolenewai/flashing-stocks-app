from django.shortcuts import render, HttpResponse, get_object_or_404, redirect, reverse
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from .forms import CustomerForm
from .models import Customer, Download, Favourite
from photos.models import Photo


def check_user_in_group(user):

    customer_group = Group.objects.get(name='customers')
    if customer_group in user.groups.all():
        return True
    else:
        return False


@login_required
def create_profile(request):

    is_customer = check_user_in_group(request.user)

    if is_customer:

        try:
            customer = Customer.objects.get(user=request.user)
        except ObjectDoesNotExist:
            customer = None

        if customer:
            return redirect(reverse(view_profile))

        else:

            if request.method == "POST":
                create_form = CustomerForm(request.POST)

                if create_form.is_valid():

                    profile = create_form.save(commit=False)
                    profile.user = request.user
                    profile.save()
                    messages.success(request, "Thank you! Your profile has been created successfully.")
                    return redirect(reverse(view_profile))

                else:
                    print (create_form._errors)
                    return render(request, 'customers/create_profile.template.html', {
                        'form': form
                    })

                    return HttpResponse("form not valid")

            else:
                form = CustomerForm()

                return render(request, 'customers/create_profile.template.html', {
                    'form': form
                })
    else:
        raise PermissionDenied


@login_required
def view_profile(request):

    is_customer = check_user_in_group(request.user)

    if is_customer:

        user_info = request.user

        try:
            profile = Customer.objects.get(user=request.user)
        except ObjectDoesNotExist:
            profile = None

        return render(request, 'customers/profile.template.html', {
            'profile': profile,
            'user_info': user_info
        })
    else:
        raise PermissionDenied


@login_required
def update_profile(request):

    is_customer = check_user_in_group(request.user)

    if is_customer:

        profile = Customer.objects.get(user=request.user)

        if request.method == 'POST':
            profile_form = CustomerForm(request.POST, instance=profile)

            if profile_form.is_valid():
                profile_form.save()
                return redirect(reverse(view_profile))
            else:
                return render(request, 'customers/update_profile.template.html', {
                    'form': profile_form
                })
        else:
            profile_form = CustomerForm(instance=profile)
            return render(request, 'customers/update_profile.template.html', {
                'form': profile_form
            })
    else:
        raise PermissionDenied


@login_required
def view_download(request):

    is_customer = check_user_in_group(request.user)

    if is_customer:
        customer = Customer.objects.get(user=request.user)
        downloads = Download.objects.filter(user=customer)
        return render(request, 'customers/download.template.html',{
            'downloads': downloads
        })
    else:
        raise PermissionDenied


@login_required
def add_to_favourite(request, photo_id):
    is_customer = check_user_in_group(request.user)

    if is_customer:

        customer = Customer.objects.get(user=request.user)
        photo = Photo.objects.get(id=photo_id)
        customer_favourite = Favourite.objects.filter(user=customer)
        
        try:
            favourited = customer_favourite.get(image=photo)
        except ObjectDoesNotExist:
            favourited = None

        if favourited is None:
            new_favourite = Favourite(
                user = customer,
                image = photo
            )
            new_favourite.save()
            messages.success(request, f"{photo.caption} has been added to your favourite")

        else:
            messages.success(request, f"{photo.caption} has been removed from your favourite")
            favourited.delete()

        redirect_url = request.POST['redirect_url']

        return redirect(redirect_url)
    else:
        raise PermissionDenied


@login_required
def view_favourites(request):

    is_customer = check_user_in_group(request.user)

    if is_customer:
        customer = Customer.objects.get(user=request.user)
        favourites = Favourite.objects.filter(user=customer)

        return render(request, 'customers/view_favourite.template.html', {
            'favourites': favourites
        })
    else:
        raise PermissionDenied
