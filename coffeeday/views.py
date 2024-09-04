from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout

from django.contrib.auth.models import User
from .forms import SuperuserCreationForm

from .forms import ItemForm,MenuForm

from .models import *
from .forms import *

# Create your views here.


def home_view(request):
    return render(request,'home.html')

def about_us_view(request):
    return render(request,'about_us.html')

def register_view(request):
    if request.method == "POST":
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return redirect('login')
        else:
            return render(request,"register.html",{"form":form}) 

    else:
        initial_data={'username':'','password1':'','password2':''}
        form=UserCreationForm(initial=initial_data)
        return render(request,"register.html",{"form":form}) 

def login_view(request):
    if request.method == "POST":
        form=AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request,user)
            return redirect('home')
        else:
            return render(request,"login.html",{"form":form})
    else:
        initial_data={'username':'','password':''}
        form=AuthenticationForm(initial=initial_data)
        return render(request,"login.html",{"form":form}) 

def logout_view(request):
    logout(request)
    return redirect("login")


def create_superuser_view(request):
    if request.method == 'POST':
        form = SuperuserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_superuser = True
            user.is_staff = True  # Required for admin access
            user.save()
            # Optionally log in the new superuser
            login(request, user)
            return redirect('login_superuser')  # Redirect to a suitable page
    else:
        initial_data={'username':'','email':'','password1':'','password2':''}

        form = SuperuserCreationForm(initial=initial_data)

    return render(request, 'create_superuser.html', {'form': form})


def login_superuser_view(request):
    if request.method == "POST":
        form=AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request,user)
            return redirect('dashboard')
        else:
            return render(request,"login_superuser.html",{"form":form})
    else:
        initial_data={'username':'','password':''}
        form=AuthenticationForm(initial=initial_data)
        return render(request,"login_superuser.html",{"form":form}) 


def logout_superuser_view(request):
    logout(request)
    return redirect("login_superuser")

# def exploreitems_view(request):
#     menus=Menu.objects.all()
#     return render(request,'exploreitems.html',{"menus":menus})


def add_menu_view(request):
    if request.method == "POST":
        form = MenuForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('menu_list')
        else:
            return render(request, 'add_menu.html', {'form': form})
    else:
        form = MenuForm()

    menus = Menu.objects.all()
    return render(request, 'add_menu.html', {'form': form, 'menus': menus})


def item_list_view(request):
    items=Item.objects.all()
    return render(request,"item_list.html",{"items":items})

def item_detail_view(request,id):
    item=Item.objects.get(id=id)
    return render(request,'item_detail.html',{"item":item})

def menu_list_view(request):
    menus=Menu.objects.all()
    return render(request,'menu_list.html',{"menus":menus})

def menu_detail_view(request, menu_id):
    menu = Menu.objects.get(id=menu_id)
    return render(request, 'item_list.html', {'menu': menu})

@login_required()
def cart_view(request):
    # cart_items = CartItem.objects.filter(user=request.user)
    user=request.user

    try:
        cart=Cart.objects.get(user=user)
    except cart.DoesNotExist:
        cart=Cart.objects.create(user=request.user)

    if cart:
        cart_items=CartItem.objects.filter(cart=cart)
    else:
        cart_items=[]

    total_price = sum(item.item.price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price,'cart':cart})

def increase_quantity(request, id):
    cart_item = get_object_or_404(CartItem, id=id, cart__user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')


def decrease_quantity(request, id):
    cart_item = get_object_or_404(CartItem, id=id, cart__user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

def remove_from_cart(request, id):
    if request.method == 'POST':
        user = request.user
        cart = get_object_or_404(Cart, user=user)
        item = get_object_or_404(CartItem, cart=cart, id=id)
        item.delete()
    return redirect('cart')

@login_required()
def add_to_cart_view(request, item_id):
    item = Item.objects.get(id=item_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Check if the item is already in the cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)
    if not created:
        # Item already in cart, just increase the quantity
        cart_item.quantity += 1
        cart_item.save()
    return redirect('menu_detail', menu_id=request.POST.get('menu_id'))

def confirm_the_order_view(request):
    user=request.user

    try:
        cart=Cart.objects.get(user=user)
    except cart.DoesNotExist:
        cart=None

    if cart:
        cart_items=CartItem.objects.filter(cart=cart)
    else:
        cart_items=[]

    total_price = sum(item.item.price * item.quantity for item in cart_items)
    return render(request,'order_confirmation.html',{'cart_items': cart_items, 'total_price': total_price})



def order_confirmation(request):
    # cart = Cart.objects.all(user=request.user)

    user=request.user

    try:
        cart=Cart.objects.get(user=user)
    except cart.DoesNotExist:
        cart=None

    if cart:
        cart_items=CartItem.objects.filter(cart=cart)
    else:
        cart_items=[]

    if request.method == 'POST':
        # Handle order submission
        past_order = PastOrder.objects.create(user=request.user)
        for cart_item in cart.items.all():
            PastOrderItem.objects.create(
                past_order=past_order,
                item=cart_item.item,
                quantity=cart_item.quantity
            )
        cart.items.all().delete()  # Clear the cart
        return redirect('order_success')
    return HttpResponse('Due to some error order is not submitted')

def order_success(request):
    return render(request, 'order_success.html')

def past_orders(request):
    # Retrieve past orders for the logged-in user
    orders = PastOrder.objects.filter(user=request.user).order_by('-created_at')
    
    return render(request, 'past_orders.html', {'orders': orders})




def dashboard_view(request):
    items_count = Item.objects.count()
    menus_count = Menu.objects.count()
    users_count = User.objects.count()
    
    context = {
        'items_count': items_count,
        'menus_count': menus_count,
        'users_count': users_count,
    }
    return render(request, 'dashboard.html', context)


def dashboard_item_list_view(request):
    items=Item.objects.all()
    return render(request,'dashboard_item_list.html',{'items':items})

def edit_item_view(request,id):
    item = Item.objects.get(id=id)
    form = ItemForm(instance=item)
    if request.method == 'POST':
        form=ItemForm(request.POST,instance=item)
        if form.is_valid():
            form.save()
        return redirect('/dashboard/item_list')
    return render(request, 'edit_item.html', {'form': form})


def add_item_view(request):
    if request.method=="POST":
        form=ItemForm(request.POST, request.FILES)
        if form.is_valid:
            form.save()
            return redirect('/dashboard/item_list')
        else:
            return render(request,'add_item.html',{'form':form})
    else:
        form=ItemForm()

    items=Item.objects.all()
    return render(request,'add_item.html',{'form':form,'items':items})



def delete_item_view(request,id):
    item=Item.objects.get(id=id)
    item.delete()
    return redirect('/dashboard/item_list')

def dashboard_menu_list_view(request):
    menus = Menu.objects.all()
    return render(request, 'dashboard_menu_list.html', {'menus': menus})

def add_menu_view(request):
    if request.method=="POST":
        form=MenuForm(request.POST, request.FILES)
        if form.is_valid:
            form.save()
            return redirect('/dashboard/menu_list')
        else:
            return render(request,'add_menu.html',{'form':form})
    else:
        form=MenuForm()

    menus=Menu.objects.all()
    return render(request,'add_item.html',{'form':form,'menus':menus})

def edit_menu_view(request,id):
    menu = Menu.objects.get(id=id)
    
    form = MenuForm(instance=menu)
    if request.method == 'POST':
        form=ItemForm(request.POST,instance=menu)
        if form.is_valid():
            form.save()
            return redirect('/dashboard/menu_list')
        return redirect('/dashboard/menu_list')
    return render(request, 'edit_menu.html', {'form': form})

def delete_menu_view(request,id):
    menu=Menu.objects.get(id=id)
    menu.delete()
    return redirect('/dashboard/menu_list')


def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})

def user_orders(request, user_id):
    user = User.objects.get(id=user_id)
    past_orders = PastOrder.objects.filter(user=user).prefetch_related('items__item')
    return render(request, 'user_orders.html', {'user': user, 'past_orders': past_orders})

def ask_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = QuestionForm()
    return render(request, 'ask_question.html', {'form': form})

def answer_questions(request):
    questions = QA.objects.filter(answered=False)
    return render(request, 'answer_questions.html', {'questions': questions})

def answer_question(request, pk):
    question = get_object_or_404(QA, pk=pk)
    if request.method == 'POST':
        form = AnswerForm(request.POST, instance=question)
        if form.is_valid():
            question.answered = True
            form.save()
            return redirect('answer_questions')
    else:
        form = AnswerForm(instance=question)
    return render(request, 'answer_question.html', {'form': form, 'question': question})

def que_and_ans(request):
    questions = QA.objects.all()
    return render(request, 'qa.html', {'questions': questions})