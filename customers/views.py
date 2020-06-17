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

    # check if user is in group 'customers'
    customer_group = Group.objects.get(name='customers')
    if customer_group in user.groups.all():
        return True
    else:
        return False


def get_customer(user):

    # return customer object if found else return None
    try:
        customer = Customer.objects.get(user=user)
    except ObjectDoesNotExist:
        customer = None

    return customer


@login_required
def create_profile(request):

    # check if user is in group 'customers'
    is_customer = check_user_in_group(request.user)

    # get customer object from Customer model if user is in customer group
    if is_customer:

        customer = get_customer(request.user)

        # if customer has already created a profile,
        # redirect customer to view profile page
        # else display form to create profile
        if customer:
            return redirect(reverse(view_profile))

        else:

            # if user has submitted the form    
            if request.method == "POST":
                create_form = CustomerForm(request.POST)

                # check if form is valid, add to database if valid
                if create_form.is_valid():
                    profile = create_form.save(commit=False)
                    profile.user = request.user
                    profile.save()
                    messages.success(
                        request,
                        "Profile created successfully."
                    )
                    return redirect(reverse(view_profile))

                else:
                    # if form is not valid, display error message
                    # and render the form again
                    messages.error(
                        request,
                        "Error, please check your form and resubmit"
                    )

                    return render(
                        request,
                        'customers/create_profile.template.html',
                        {
                            'form': create_form
                        })

            else:
                # if user has not submitted any form, render an empty form
                form = CustomerForm()

                return render(
                    request,
                    'customers/create_profile.template.html',
                    {
                        'form': form
                    })
    else:
        # raise permission denied error if user is not in group 'customers'
        raise PermissionDenied


@login_required
def view_profile(request):
    # check if user is in group 'customers'
    is_customer = check_user_in_group(request.user)

    # if customer is in group 'customers'
    if is_customer:

        user_info = request.user
        # get customer profile
        profile = get_customer(user_info)

        return render(request, 'customers/profile.template.html', {
            'profile': profile,
            'user_info': user_info
        })
    else:
        # raise permission denied error if user is not in group 'customers'
        raise PermissionDenied


@login_required
def update_profile(request):

    # check if user is in group 'customers'
    is_customer = check_user_in_group(request.user)

    # if customer is in group 'customers'
    if is_customer:
        # get customer profile
        profile = get_customer(request.user)

        # if user has submitted a form
        if request.method == 'POST':
            # create form object with posted information
            profile_form = CustomerForm(request.POST, instance=profile)

            # if form has no errors
            if profile_form.is_valid():
                # update the profile of the user instance 
                profile_form.save()
                return redirect(reverse(view_profile))
            else:
                return render(request, 'customers/update_profile.template.html', {
                    'form': profile_form
                })
        else:
            # if user has not submitted any form
            # retrieve and display data in the rendered form
            profile_form = CustomerForm(instance=profile)
            return render(request, 'customers/update_profile.template.html', {
                'form': profile_form
            })
    else:
        # raise permission denied if user is not in group 'customers'
        raise PermissionDenied


@login_required
def view_download(request):

    is_customer = check_user_in_group(request.user)

    if is_customer:
        customer = get_customer(request.user)
        downloads = Download.objects.filter(user=customer)
        return render(request, 'customers/download.template.html', {
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
