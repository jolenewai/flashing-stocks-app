from django.shortcuts import render, redirect, reverse
from django.db.models import Q, Count
from photos.models import Photo, Category, Tag
from django.contrib.auth.models import Group
from customers.models import Customer, Favourite, Download


def index(request):

    photographer_group = Group.objects.get(name='photographers')

    if request.user.is_authenticated:

        if photographer_group in request.user.groups.all():
            return redirect(reverse('photographer_view_profile'))
        else:
            return redirect(reverse('list_photos'))
    else:
        return render(request, 'home/index.template.html')


def search(request):

    photos = Photo.objects.all()
    categories = Category.objects.all()
    tags = Tag.objects.all().order_by('name')

    keyword = ''
    if request.GET:
        queries = ~Q(pk__in=[])

        if 'keyword' in request.GET and request.GET['keyword']:
            keyword = request.GET['keyword']
            queries = queries & (Q(caption__icontains=keyword) | Q(desc__icontains=keyword) | Q(tags__name=keyword))

        if 'category' in request.GET and request.GET['category']:
            category = request.GET['category']
            queries = queries & Q(category__id=category) 

        photos = photos.filter(queries)
        photos_count = photos.count()

        if 'sortby' in request.GET and request.GET['sortby']:
            sortby_field = request.GET['sortby']
            
            if sortby_field == 'mr':
                photos = photos.order_by('date_added')
            elif sortby_field == 'al':
                photos = photos.order_by('caption')
            elif sortby_field == 'pp':
                downloads = Download.objects.values('image__id').annotate(num_download=Count('image')).order_by('-num_download')

                queries = ~Q(pk__in=[])

                if 'keyword' in request.GET and request.GET['keyword']:
                    keyword = request.GET['keyword']
                    queries = queries & (
                        Q(image__caption__icontains=keyword) | Q(image__desc__icontains=keyword) | Q(image__tags__name=keyword)
                    )

                if 'category' in request.GET and request.GET['category']:
                    category = request.GET['category']
                    queries = queries & Q(image__category__id=category) 

                photos = downloads.filter(queries)

    favourited_photo = []

    
    if request.user.is_authenticated:
        customer = Customer.objects.get(user=request.user)
        favourites = Favourite.objects.filter(user=customer)

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
    photos = Photo.objects.all()
    categories = Category.objects.all()
    tags = Tag.objects.all()

    queries = ~Q(pk__in=[])

    queries = queries & Q(tags=selected_tag)

    photos = photos.filter(queries)
    favourited_photo = []
    photos_count = photos.count()

    if request.user.is_authenticated:
        customer = Customer.objects.get(user=request.user)
        favourites = Favourite.objects.filter(user=customer)

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

