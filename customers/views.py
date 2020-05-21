from django.shortcuts import render, HttpResponse
from .forms import CustomerForm
from .models import Customer



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

