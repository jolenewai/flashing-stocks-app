from django.shortcuts import render, redirect, reverse
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import Group
from photos.models import Photo, Category, Tag
from customers.models import Customer, Favourite


def index(request):

    photographer_group = Group.objects.get(name='photographers')
    customer_group = Group.objects.get(name='customers')

    if request.user.is_authenticated:
        if photographer_group in request.user.groups.all():
            return redirect(reverse('photographer_view_profile'))
        elif customer_group in request.user.groups.all():
            return redirect(reverse('list_photos'))
        else:
            return redirect(reverse('admin_homepage'))
    else:
        return render(request, 'home/index.template.html')


def search(request):

    photos = Photo.objects.all()
    categories = Category.objects.all()
    tags = Tag.objects.all().order_by('name')

    # initialise keyword to empty string
    keyword = ''

    # if GET parameter exists
    if request.GET:

        # always true query
        queries = ~Q(pk__in=[])

        # get keyword if keyword found in query string
        if 'keyword' in request.GET and request.GET['keyword']:
            keyword = request.GET['keyword']
            # get photo object that contains keyword in
            # caption, description, tag and category name
            queries = queries & (
                Q(caption__icontains=keyword) |
                Q(desc__icontains=keyword) |
                Q(tags__name__icontains=keyword) |
                Q(category__name__icontains=keyword)
                )

        # if category is found in query string
        if 'category' in request.GET and request.GET['category']:
            category = request.GET['category']
            # filter result by specified category
            queries = queries & Q(category__id=category)

        # filter unique result with combined queries above
        photos = photos.filter(queries).distinct()

        # if sortby is found in query string
        if 'sortby' in request.GET and request.GET['sortby']:

            # get the field to sort
            sortby_field = request.GET['sortby']

            # if 'Most Recent' is chosen for sorting
            if sortby_field == 'mr':
                # sort result by 'Date added' field
                photos = photos.order_by('date_added')
            # if 'Alphabetical Order' is chosen for sorting
            elif sortby_field == 'al':
                # sort result by 'caption' field
                photos = photos.order_by('caption')

    # do a count for the final search results
    photos_count = photos.count()

    # to determine if a photo has been favourited by the user
    # variable initialised as empty array to avoid error in template
    favourited_photo = []

    # if user is logged in and in customer group
    if request.user.is_authenticated and request.user.groups.first() == 'customers':

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

    return render(request, 'home/search.template.html', {
            'photos': photos,
            'categories': categories,
            'tags': tags,
            'keyword': keyword,
            'photos_count': photos_count,
            'favourited_photo': favourited_photo
        })


def search_by_tag(request, tag_id):
    selected_tag = Tag.objects.get(id=tag_id)
    # get all photo objects for filtering later
    photos = Photo.objects.all()
    categories = Category.objects.all()
    tags = Tag.objects.all()

    # always true query
    queries = ~Q(pk__in=[])

    # create query with selected tag
    queries = queries & Q(tags=selected_tag)

    # filter result with query
    photos = photos.filter(queries)

    # initialise empty array for user favourite photos
    favourited_photo = []
    photos_count = photos.count()

    # if user is logged in and in customer group
    if request.user.is_authenticated and request.user.groups.first() == 'customers':

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

    return render(request, 'home/search.template.html', {
        'photos': photos,
        'categories': categories,
        'tags': tags,
        'favourited_photo': favourited_photo,
        'photos_count': photos_count
    })


def terms_of_use(request):
    return render(request, 'home/terms_of_use.html')


def license_agreements(request):
    return render(request, 'home/license_agreements.html')
