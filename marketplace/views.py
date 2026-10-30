from django.shortcuts import get_object_or_404, render, redirect
from marketplace.models import Category, Item, Conversation, ConversationMessage
from django.contrib.auth.decorators import login_required
from marketplace.forms import NewItemForm, EditItemForm, ConversationMessageForm

# Create your views here.
def show_market(request):
    items = Item.objects.filter(is_sold=False)[0:6]
    categories = Category.objects.all()
    
    return render(request, 'market.html',{
                'category': categories,
                  'items': items,
                    }  )

def contact(request):

    return render(request, 'templates/contact.html')

def items(request):
    item = Item.objects.filter(is_sold=False)

    return render(request, 'templates/items.html', {
        'items': item,
    })

def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[0:3]

    return render(request, 'detail_item.html', {
        'item' : item,
        'related_item' : related_items,
    })

@login_required
def new(request):
    categories = Category.objects.all()

    if request.method == "POST":
        form = NewItemForm(request.POST, request.FILES)

        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()

            return redirect('marketplace:detail', pk=item.id)
    else:
        form = NewItemForm()

    return render(request, 'form.html', {
        'form' : form,
        'categories': categories, # Kirim variabel categories ke template
        'title' : 'New item',
    })

@login_required
def delete(request, pk):
    if request.method == "POST":
        item = get_object_or_404(Item, pk=pk, created_by=request.user)
        item.delete()
        return redirect('marketplace:index', pk=item.id)

@login_required
def edit(request, pk):
    item = get_object_or_404(Item, pk=pk)

    if item.created_by != request.user:
        return redirect('marketplace:show_market')

    if request.method == "POST":
        form = EditItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('marketplace:detail', pk=item.id)
    else:
        form = EditItemForm(instance=item)

    return render(request, 'form.html', {
        'form': form,
        'title': 'Edit item',
    })

@login_required
def delete(request, pk):
    item = get_object_or_404(Item, pk=pk)

    if item.created_by == request.user:
        item.delete()
    
    # WAJIB menggunakan redirect agar kembali ke halaman market dan tidak merusak tampilan
    return redirect('marketplace:show_market')

def new_conversation(request, item_pk):
    item = get_object_or_404(Item, pk=item_pk)

    if item.created_by == request.user:
        return redirect('index.html')

    conversations = Conversation.objects.filter(item=item).filter(members__in=[request.user.id])

    if conversations:
        pass

    if request.method == "POST":
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation = Conversation.objects.create(item=item)
            conversation.members.add(request.user)
            conversation.members.add(item.created_by)
            conversation.save()

            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            return redirect('marketplace:detail', pk=item_pk)

    else:
        form = ConversationMessageForm()

    return render(request, 'templates/contact.html', {
        'form' : form,
    })