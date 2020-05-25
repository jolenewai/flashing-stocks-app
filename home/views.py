from django.shortcuts import render
from django.db.models import Q
from photos.models import Photo, Category, Tag

# Create your views here.


def index(request):

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
            queries = queries & Q(caption__icontains=keyword)

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