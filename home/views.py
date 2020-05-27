from django.shortcuts import render, redirect, reverse, HttpResponse
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from photos.models import Photo, Category, Tag
from django.contrib.auth.models import Group



# Create your views here.


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
    tags = Tag.objects.all()

    keyword = ''
    if request.GET:
        queries = ~Q(pk__in=[])

        if 'keyword' in request.GET and request.GET['keyword']:
            keyword = request.GET['keyword']
            queries = queries & (Q(caption__icontains=keyword) | Q(desc__icontains=keyword))

        if 'category' in request.GET and request.GET['category']:
            category = request.GET['category']
            queries = queries & Q(category__id=category) 

        photos = photos.filter(queries)
        
    return render(request, 'home/search.template.html', {
        'photos': photos,
        'categories': categories,
        'tags': tags,
        'keyword': keyword
    })


def search_by_tag(request, tag_id):
    selected_tag = Tag.objects.get(id=tag_id)
    photos = Photo.objects.all()
    categories = Category.objects.all()
    tags = Tag.objects.all()

    queries = ~Q(pk__in=[])

    queries = queries & Q(tags=selected_tag)

    photos = photos.filter(queries)

    return render(request, 'home/search.template.html', {
        'photos': photos,
        'categories': categories,
        'tags': tags
    })