from django.shortcuts import render, HttpResponse, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from .forms import CustomerForm
from .models import Customer

def view_profile(request):

    user_info = request.user

    try:
        profile = Customer.objects.get(user=request.user)
    except ObjectDoesNotExist:
        profile = None

    return render(request, 'customers/profile.template.html', {
        'profile': profile,
        'user_info': user_info
    })


def create_profile(request):

    if request.method == "POST":
        create_form = CustomerForm(request.POST)

        if create_form.is_valid():

            profile = create_form.save(commit=False)
            profile.user = request.user
            profile.save()
            return HttpResponse("profile added")

        else:
            print (create_form._errors)
            return HttpResponse("form not valid")
    else:
        form = CustomerForm()

        return render(request, 'customers/create_profile.template.html', {
            'form': form
        })

