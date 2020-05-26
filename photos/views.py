from django.shortcuts import render, redirect, reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.db.models import Q
from photographers.models import Photographer
from photographers.views import view_uploads
from .models import Photo, Tag, Category
from .forms import PhotoForm, TagForm, CategoryForm
from customers.models import Favourite, Customer


def list_photos(request):
    try:
        photos = Photo.objects.all()
    except ObjectDoesNotExist:
        photos = None

    photos_count = photos.count()
    customer = Customer.objects.get(user=request.user)
    favourites = Favourite.objects.filter(user=customer)
    favourited_photo = []

    for fav in favourites:
        favourited_photo.append(
            fav.image
        )

    return render(request, 'photos/list_photos.template.html', {
        'photos': photos,
        'photos_count': photos_count,
        'favourited_photo': favourited_photo
    })


def add_photo(request):

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


def edit_photo(request, photo_id):

    try:
        photo = Photo.objects.get(id=photo_id)
    except ObjectDoesNotExist:
        photo = None

    if request.method == "POST":
        edit_form = PhotoForm(request.POST, instance=photo)

        if edit_form.is_valid():
            edit_form.save()
            messages.success(request, "Profile updated successfully")
            return redirect(reverse(view_photo, kwargs={'photo_id': photo.id}))
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


def delete_photo(request, photo_id):

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


def add_tags(request):

    tags = Tag.objects.all()

    form = TagForm()

    if request.method == 'POST':

        tag_form = TagForm(request.POST)

        if tag_form.is_valid():
            tag = tag_form.save()
            messages.success(
                request, f"Tag [{tag.name}] added successful"
            )
        else:
            messages.error(
                request, f"Unable to add new Tag"
            )
            return render(request, 'photos/add_tags.template.html', {
                'tags': tags,
                'form': tag_form
            })

    return render(request, 'photos/add_tags.template.html', {
        'tags': tags,
        'form': form
    })


def edit_tag(request, tag_id):

    try:
        tag = Tag.objects.get(id=tag_id)
    except ObjectDoesNotExist:
        tag = None

    if tag:
        form = TagForm(instance=tag)

    if request.method == 'POST':
        tag_form = TagForm(request.POST, instance=tag)

        if tag_form.is_valid():
            saved_tag = tag_form.save()
            messages.success(request, f"Tag {saved_tag.name} has been updated")
            return redirect(reverse(add_tags))
        else:
            messages.error(request, f"Update failed.")
            return render(request, 'photos/edit_tag.template.html', {
                'form': tag_form
            })

    return render(request, 'photos/edit_tag.template.html', {
        'form': form
    })


def delete_tag(request, tag_id):

    try:
        tag = Tag.objects.get(id=tag_id)
    except ObjectDoesNotExist:
        tag = None

    if request.method == 'POST':
        tag.delete()
        return redirect(reverse(add_tags))

    return redirect(reverse(add_tags))


def add_category(request):

    categories = Category.objects.all()

    if request.method == 'POST':
        category_form = CategoryForm(request.POST)

        if category_form.is_valid():
            category = category_form.save()
            messages.success(
                request, f"Category [{category.name}] added successful"
            )
        else:
            messages.error(
                request, f"Unable to add new category"
            )
            return render(request, 'photos/add_category.template.html', {
                'categories': categories,
                'form': category_form
            })

    form = CategoryForm()

    return render(request, 'photos/add_category.template.html', {
        'categories': categories,
        'form': form
    })


def edit_category(request, category_id):

    try:
        category = Category.objects.get(id=category_id)
    except ObjectDoesNotExist:
        category = None

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            saved_category = form.save()
            messages.success(
                request,
                f"Category Name [{saved_category.name}] has been updated"
                )
            return redirect(reverse(add_category))
        else:
            messages.error(request, "Unable to update category name")
            return render(request, 'photos/edit_category.template.html', {
                'form': form
            })

    form = CategoryForm(instance=category)

    return render(request, 'photos/edit_category.template.html', {
        'form': form
    })


def delete_category(request, category_id):

    try:
        category = Category.objects.get(id=category_id)
    except ObjectDoesNotExist:
        category = None

    if request.method == 'POST':
        messages.success(
            request,
            f"Category [{category.name}] has been deleted"
        )
        category.delete()
        return redirect(reverse(add_category))
    else:
        messages.error(request, f"Unable to delete category")
        return redirect(reverse(add_category))

    return redirect(reverse(add_category))

