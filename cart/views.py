from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist


from photos.models import Photo
from photos.views import list_photos


def add_to_cart(request, photo_id):
    # to get existng card from the session using the key "shopping cart"
    cart = request.session.get('shopping_cart', {})
    print("find cart")
    if photo_id not in cart:
        print("find photo")
        try:
            photo = Photo.objects.get(id=photo_id)
        except ObjectDoesNotExist:
            photo = None

        if photo:
            print("found photo")
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

            return redirect(reverse(list_photos))
    else:

        messages.error(
            request,
            "Image is already in your cart"
        )
        return redirect(reverse(list_photos))


def view_cart(request):
    cart = request.session.get('shopping_cart', {})
    photos = Photo.objects.all()

    return render(request, 'cart/view_cart.template.html', {
        'shopping_cart': cart,
        'photos': photos
    })