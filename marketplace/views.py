from django.shortcuts import get_object_or_404, render, redirect
from marketplace.models import Category, Item

# Create your views here.
def index(request):
    items = Item.object.filter(is_sold=False)[0:6]
    categories = Category.objects.all()
    
    return render(request, 'templates/index.html',{
                'category': categories,
                  'item': items,
                    }  )

def contact(request):

    return render(request, 'templates/contact.html')

def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item,object.filter(category=item.category, is_sold=False).exclude(pk=pk)[0:3]

    return render(request, 'templates/detail.html', {
        'item' : item,
        'related_item' : related_items,
    })