from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from photos.models import Photo
from photos.views import list_photos
from customers.models import Download, Customer
import datetime


@login_required
def add_to_cart(request, photo_id):

    # check if customer profile exist in database
    # proceed to add to cart if profile exists
    # else redirect user to create profile page
    try:
        customer = Customer.objects.get(user=request.user)
    except ObjectDoesNotExist:
        customer = None

    if customer:

        if request.POST['size']:
            # to get existing cart from the session using the key "shopping cart"
            cart = request.session.get('shopping_cart', {})

            # to check if the photo is already in cart
            if photo_id not in cart:
                try:
                    photo = Photo.objects.get(id=photo_id)
                except ObjectDoesNotExist:
                    photo = None

                # to check if the user has downloaded the photo before
                customer_downloaded = Download.objects.filter(user=customer)

                if customer_downloaded:
                    try:
                        downloaded = customer_downloaded.filter(image=photo)
                    except ObjectDoesNotExist:
                        downloaded = None
                else:
                    downloaded = None

                if photo:
                    # if the user has already paid for the photo, add a new record to download
                    # so that the user can download the image again with the desired size
                    if downloaded:
                        new_download = Download(
                            user=customer,
                            image=photo,
                            size=request.POST['size'],
                            date=datetime.datetime.now(),
                            )
                        new_download.save()

                        messages.error(
                            request,
                            "Image has already been purchased, please download it on My Download page"
                        )
                    else:
                        cart[photo_id] = {
                            'id': photo_id,
                            'caption': photo.caption,
                            'price': photo.price,
                            'size': request.POST['size']
                        }

                        request.session['shopping_cart'] = cart

                        messages.success(
                            request,
                            f"{photo.caption} has been added to your cart!"
                        )

                    return redirect(reverse(
                        'view_photo',
                        kwargs={'photo_id': photo.id})
                    )
            else:
                # if the image is already in the cart, redirect user back to
                # the previous page and display an error message
                messages.error(
                    request,
                    "Image is already in your cart"
                )
                return redirect(reverse(list_photos))
        else:
            # if request.GET['size'] is empty, redirect user back to the
            # previous page and make user select a size
            messages.error(
                request,
                "Please select a size!"
            )
            return redirect(reverse(
                'view_photo',
                kwargs={'photo_id': photo.id})
            )
    else:
        # if customer profile not exist
        # redirect user to create a profile before proceed
        messages.error(
            request,
            "Please create a profile before adding to cart"
        )
        return redirect(reverse('cust_create_profile'))


@login_required
def view_cart(request):
    cart = request.session.get('shopping_cart', {})
    photos = Photo.objects.all()
    total = 0

    # get price from database and calculate total in cents
    for id, photo in cart.items():
        try:
            photo_object = Photo.objects.get(id=id)
        except ObjectDoesNotExist:
            photo_object = None

        total = total + int(photo_object.price*100)

    # convert total back to dollars
    total = total / 100

    return render(request, 'cart/view_cart.template.html', {
        'shopping_cart': cart,
        'photos': photos,
        'total': total
    })


def remove_from_cart(request, photo_id):

    # get cart from session
    cart = request.session.get('shopping_cart', {})

    # delete selected photo from cart
    if photo_id in cart:
        del cart[photo_id]
        request.session['shopping_cart'] = cart
        messages.success(request, "Photo removed from cart successfully")
        return redirect(reverse(view_cart))
    else:
        messages.error(request, "Photo not in cart!")
        return redirect(reverse(view_cart))


def update_size(request, photo_id):

    # get cart from session
    cart = request.session.get('shopping_cart')

    # update the size for the selected photo in cart
    if photo_id in cart:
        cart[photo_id]['size'] = request.POST['size']
        request.session['shopping_cart'] = cart
        messages.success(
            request,
            f"Size for {cart[photo_id]['caption']} has been changed"
        )

        return redirect(reverse(view_cart))
