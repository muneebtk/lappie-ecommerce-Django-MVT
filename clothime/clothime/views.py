from django .shortcuts import render
from category.models import Category
from store.models import FeaturedProduct,Product, HomeCarousel

def home(request):
    category = Category.objects.all()
    featured = FeaturedProduct.objects.order_by('-id').all()[0:6]
    new_arrivals = Product.objects.order_by('-created_date').all()[0:6]
    try:
        home_carousel1 = HomeCarousel.objects.order_by('-id').all()[0]
        home_carousel2 = HomeCarousel.objects.order_by('-id').all()[1]
        home_carousel3 = HomeCarousel.objects.order_by('-id').all()[2]
    except:
        pass
    context = {
        'categories' : category,
        'featured': featured,
        'home_carousel1':home_carousel1,
        'home_carousel2':home_carousel2,
        'home_carousel3':home_carousel3,
        'new_arrivals':new_arrivals,
    }
    return render(request,'home.html',context)
