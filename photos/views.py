from django.shortcuts import render, redirect, reverse
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from photographers.models import Photographer
from photographers.views import view_uploads
from .models import Photo, Tag, Category
from .forms import PhotoForm, TagForm, CategoryForm
from customers.models import Favourite, Customer


def check_user_in_group(user):
    # return True if user is in photographer group else return False
    photographer_group = Group.objects.get(name='photographers')
    if photographer_group in user.groups.all():
        return True
    else:
        return False


def get_photo(photo_id):

    # return found photo object or none if not exist
    try:
        photo = Photo.objects.get(id=photo_id)
    except ObjectDoesNotExist:
        photo = None

    return photo


def list_photos(request):
    # get all photos and sort by date_added in descending order
    try:
        photos = Photo.objects.all().order_by('-date_added')
    except ObjectDoesNotExist:
        photos = None

    # initialise an array for favourited photo
    favourited_photo = []
    # get all categories from database
    categories = Category.objects.all()
    # count the number of results
    photos_count = photos.count()

    # if user is logged in and in customer group
    if request.user.is_authenticated:

        try:
            customer = Customer.objects.get(user=request.user)
        except ObjectDoesNotExist:
            customer = None

        if customer:
            favourites = Favourite.objects.filter(user=customer)

            for fav in favourites:
                favourited_photo.append(
                    fav.image
                )

    return render(request, 'photos/list_photos.template.html', {
        'photos': photos,
        'photos_count': photos_count,
        'favourited_photo': favourited_photo,
        'categories': categories
    })


@login_required
def add_photo(request):
    # check if user is a photographer
    is_photographer = check_user_in_group(request.user)
    if is_photographer:

        # get photographer profile if exists else assign None
        try:
            photographer = Photographer.objects.get(user=request.user)
        except ObjectDoesNotExist:
            photographer = None

        # if photographer is found and form submitted, add photo to database
        if photographer:
            if request.method == 'POST':
                form = PhotoForm(request.POST)

                if form.is_valid():
                    add_form = form.save(commit=False)
                    add_form.owner = photographer
                    add_form.save()
                    form.save_m2m()
                    messages.success(request, "Photo added successfully")
                    return redirect(reverse(view_uploads))
                else:
                    return render(request, 'photos/add_photos.template.html', {
                        'form': form
                    })
            # if form is not submitted, render an empty form
            else:

                form = PhotoForm()
                return render(request, 'photos/add_photo.template.html', {
                    'form': form
                })
        # if photographer has not created a profile
        # redirect the photographer to create profile page
        else:
            messages.error(request, 'Complete your profile to add a photo')
            return redirect(reverse('photographer_create_profile'))
    # Deny access if the user if not a photographer
    else:
        raise PermissionDenied


def view_photo(request, photo_id):

    # get photo object for specified photo_id
    photo = get_photo(photo_id)

    if photo:
        category = photo.category.all()
        photos = Photo.objects.all()

        # always true query
        queries = ~Q(pk__in=[])

        # find photos in the same category of the specified photo_id
        queries_1 = queries & Q(category__in=category)
        related_photos = photos.filter(queries_1).distinct()

        # find photos by the same photographer of the specified photo_id
        queries_2 = queries & Q(owner=photo.owner)
        photographer_set = photos.filter(queries_2).distinct()

        return render(request, 'photos/view_photo.template.html', {
            'photo': photo,
            'related_photos': related_photos,
            'photographer_set': photographer_set
        })
    # to handle invalid photo_id in url
    else:
        messages.success(request, "Invalid Photo ID")
        return redirect(reverse(list_photos))


@login_required
def edit_photo(request, photo_id):

    # check if user is a photographer
    is_photographer = check_user_in_group(request.user)
    if is_photographer:
        
        # get photo object of specified photo_id
        photo = get_photo(photo_id)

        # if form is submitted
        if request.method == "POST":
            # create instance of the form posted
            edit_form = PhotoForm(request.POST, instance=photo)

            if edit_form.is_valid():
                edit_form.save()
                messages.success(request, "Photo updated successfully")
                return redirect(reverse(view_uploads))
            else:
                return render(request, 'photos/edit_photo.template.html', {
                    'form': edit_form,
                    'photo': photo
                })
        # if form is not submitted, render form with data from database
        else:

            form = PhotoForm(instance=photo)

            return render(request, 'photos/edit_photo.template.html', {
                'form': form,
                'photo': photo
            })
    # if user is not a photographer
    else:
        raise PermissionDenied


@login_required
def delete_photo(request, photo_id):
    # check if user is a photographer
    is_photographer = check_user_in_group(request.user)

    # if user is a photographer
    if is_photographer:
        # get photo of specified photo_id
        photo = get_photo(photo_id)

        if request.method == "POST":
            # if photo exists, delete the photo
            if photo:
                photo.delete()
            # else display message for invalid photo id
            else:
                messages.error(request, "Invalid photo id")

            return redirect(reverse(view_uploads))

        return render(request, 'photos/delete_photo.template.html', {
            'photo': photo
        })
    # deny access if user is not a photographer
    else:
        raise PermissionDenied


def photo_by_category(request, category_id):

    # get all categories from database
    all_categories = Category.objects.all()

    # get category of specified category_id
    try:
        category = Category.objects.get(id=category_id)
    except ObjectDoesNotExist:
        category = None

    # initialise empty array for user favourite photos
    favourited_photo = []

    # if user is logged in
    if request.user.is_authenticated:

        try:
            customer = Customer.objects.get(user=request.user)
        except ObjectDoesNotExist:
            customer = None

        # if customer profile exists, get favourite for this user
        if customer:
            favourites = Favourite.objects.filter(user=customer)

            # append photo to favourited_photo array if record found
            for fav in favourites:
                favourited_photo.append(
                    fav.image
                )

    # if category is found
    if category:
        photos_in_category = Photo.objects.filter(category=category)
        photos_count = photos_in_category.count()

        return render(request, 'photos/view_category.template.html', {
            'photos': photos_in_category,
            'photos_count': photos_count,
            'category': category,
            'all_categories': all_categories,
            'favourited_photo': favourited_photo
        })
    # redirect to all photos page if category is not found
    else:
        messages.success(request, "Invalid Photo Category")
        return redirect(reverse(list_photos))
