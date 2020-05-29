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

    photographer_group = Group.objects.get(name='photographers')
    if photographer_group in user.groups.all():
        return True
    else:
        return False


def list_photos(request):
    try:
        photos = Photo.objects.all().order_by('-date_added')
    except ObjectDoesNotExist:
        photos = None

    favourited_photo = []

    categories = Category.objects.all()

    photos_count = photos.count()
    if request.user.is_authenticated and request.user.groups.first() == 'customers':
        customer = Customer.objects.get(user=request.user)
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
    is_photographer = check_user_in_group(request.user)
    if is_photographer:
        photographer = Photographer.objects.get(user=request.user)

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
        else:

            form = PhotoForm()

            return render(request, 'photos/add_photo.template.html', {
                'form': form
            })
    else:
        raise PermissionDenied


def view_photo(request, photo_id):

    try:
        photo = Photo.objects.get(id=photo_id)
    except ObjectDoesNotExist:
        photo = None

    category = photo.category.all()
    photos = Photo.objects.all()

    queries = ~Q(pk__in=[])

    queries_1 = queries & Q(category__in=category)
    related_photos = photos.filter(queries_1)

    queries_2 = queries & Q(owner=photo.owner)
    photographer_set = photos.filter(queries_2) 

    return render(request, 'photos/view_photo.template.html', {
        'photo': photo,
        'related_photos': related_photos,
        'photographer_set': photographer_set
    })


@login_required
def edit_photo(request, photo_id):

    is_photographer = check_user_in_group(request.user)
    if is_photographer:

        try:
            photo = Photo.objects.get(id=photo_id)
        except ObjectDoesNotExist:
            photo = None

        if request.method == "POST":
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
        else:

            form = PhotoForm(instance=photo)

            return render(request, 'photos/edit_photo.template.html', {
                'form': form,
                'photo': photo
            })
    else:
        raise PermissionDenied


@login_required
def delete_photo(request, photo_id):
    is_photographer = check_user_in_group(request.user)
    if is_photographer:
        try:
            photo = Photo.objects.get(id=photo_id)
        except ObjectDoesNotExist:
            photo = None

        if request.method == "POST":
            photo.delete()
            return redirect(reverse(view_uploads))

        return render(request, 'photos/delete_photo.template.html', {
            'photo': photo
        })
    else:
        raise PermissionDenied


def photo_by_category(request, category_id):

    all_categories = Category.objects.all()
    category = Category.objects.get(id=category_id)

    photos_in_category = Photo.objects.filter(category=category)
    photos_count = photos_in_category.count()

    return render(request, 'photos/view_category.template.html', {
        'photos': photos_in_category,
        'photos_count': photos_count,
        'category': category,
        'all_categories': all_categories
    })
