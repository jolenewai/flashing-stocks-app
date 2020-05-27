from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist


from photos.models import Photo
from photos.views import list_photos


def add_to_cart(request, photo_id):

    if request.POST['size']:
        # to get existing cart from the session using the key "shopping cart"
        cart = request.session.get('shopping_cart', {})
        
        if photo_id not in cart:
            print("find photo")
            try:
                photo = Photo.objects.get(id=photo_id)
            except ObjectDoesNotExist:
                photo = None

            if photo:
                
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

            messages.error(
                request,
                "Image is already in your cart"
            )
            return redirect(reverse(list_photos))
    else:
        messages.error(
            request,
            "Please select a size!"
        )
        return redirect(reverse('view_photo', kwargs={'photo_id': photo.id}))


def view_cart(request):
    cart = request.session.get('shopping_cart', {})
    photos = Photo.objects.all()
    total = 0

    for id, photo in cart.items():
        try:
            photo_object = Photo.objects.get(id=id)
        except ObjectDoesNotExist:
            photo_object = None

        total = total + int(photo_object.price*100)

    total = total / 100

    return render(request, 'cart/view_cart.template.html', {
        'shopping_cart': cart,
        'photos': photos,
        'total': total
    })


def remove_from_cart(request, photo_id):
    cart = request.session.get('shopping_cart', {})

    if photo_id in cart:
        del cart[photo_id]

        request.session['shopping_cart'] = cart
        messages.success(request, "Photo removed from cart successfully")
        return redirect(reverse(view_cart))
    else:
        messages.error(request, "Photo not in cart!")
        return redirect(reverse(view_cart))


def update_size(request, photo_id):
    cart = request.session.get('shopping_cart')

    if photo_id in cart:
        cart[photo_id]['size'] = request.POST['size']
        request.session['shopping_cart'] = cart
        messages.success(
            request,
            f"Size for {cart[photo_id]['caption']} has been changed"
        )

        return redirect(reverse(view_cart))
