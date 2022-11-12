from datetime import datetime
import json
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import HttpResponse, redirect, render

from .models import Order, OrderUpdate, Product, Review
from .templatetags import extras


# Template rendering functions
def index(request):
    categories = {item['category'] for item in Product.objects.values('category')}
    products = []
    for category in categories:
        product = Product.objects.filter(category=category)
        products.append(product)

    params = {'products': products}
    return render(request, 'shop.html', params)


def product_view(request, id):
    product = Product.objects.filter(product_id=id)
    reviews = Review.objects.filter(product=product[0])
    stars, rating, no_reviews = make_binary(reviews)
    print(rating)

    if request.method == 'POST':
        stars = request.POST.get('stars')
        title = request.POST.get('title')
        comment = request.POST.get('comment')

        review = Review(stars=stars, title=title, comment=comment, product=product[0], user=request.user)
        review.save()

    params = {'product': product[0], 'reviews': reviews, 'ratings': rating, 'no_reviews': no_reviews, 'stars':stars}
    return render(request, 'product.html', params)


def cart(request):
    return render(request, 'cart.html')


def search(request):
    query = request.GET.get('search')
    all_products = Product.objects.all()
    products = []

    for product in all_products:
        if search_alg(query, product):
            products.append(product)

    params = {'products': products, 'query': query}
    print(products)
    return render(request, 'search.html', params)


def account(request):
    if request.user.is_anonymous:
        if request.method == 'POST':
            login = request.POST.get('login')
            signup = request.POST.get('signup')

            if login is not None:
                email = request.POST.get('email')
                password = request.POST.get('pwd')
                logged_in = login_user(request, email, password)
                
                if logged_in:
                    return redirect('StoreHome')
                else:
                    messages.add_message(request, messages.ERROR, 'Incorrect email or password!')

            elif signup is not None:
                first_name = request.POST.get('first-name')
                last_name = request.POST.get('last-name')
                email = request.POST.get('email')
                password_1 = request.POST.get('pwd')
                password_2 = request.POST.get('c-pwd')
                correct_password = password_1 == password_2

                if correct_password:
                    user_created = create_user(request, first_name, last_name, email, password_1)
                    if user_created:
                        return redirect('StoreHome')
                    else:
                        messages.add_message(request, messages.ERROR, 'Email already exists!')
                        return render(request, 'account.html', {'Signup':True})

                else:
                    messages.add_message(request, messages.ERROR, 'Password does not match!')
                    return render(request, 'account.html', {'Signup':True})

        return render(request, 'account.html')
    else:

        order_history = Order.objects.filter(user=request.user)
        final_cart = []
        for order in order_history:
            cart = json.loads(order.json_field)
            keys = [x for x in cart]
            for key in keys:
                final_cart.append(cart[key])
        return render(request, 'accounts.html', {'history':final_cart[::-1]})

def checkout(request):
    if request.user.is_anonymous:
        return redirect('StoreAccount')
    
    if request.method == 'POST':
        f_name = request.POST.get('f-name')
        l_name = request.POST.get('l-name')
        address = request.POST.get('address')
        city = request.POST.get('city')
        country = request.POST.get('country')
        zip = request.POST.get('zip-postalcode')
        contact = request.POST.get('contact')
        email = request.POST.get('email')

        json_field = request.POST.get('json-products')

        delivery = request.POST.get('dlvry')
        payment = request.POST.get('pymnt')

        order = Order(f_name=f_name, l_name=l_name, address=address, city=city, country=country, zip=zip, contact=contact, email=email, delivery=delivery, payment=payment, json_field=json_field, user=request.user)
        order.save()

        update = OrderUpdate(order=order)
        update.save()

        order_id = order.order_id
        return render(request, 'checkout.html', {'success': 'true', 'id': order_id})

    return render(request, 'checkout.html', {'success': 'false'})


def tracker(request):
    if request.user.is_authenticated:
        orders_ids = Order.objects.filter(user=request.user).values('order_id')
        orders_ids = sorted(orders_ids, key=get_val, reverse=True)

        if len(orders_ids) != 0:
            orders = []
            for order_id in orders_ids:
                order = Order.objects.filter(order_id=order_id['order_id'])
                update_progress = OrderUpdate.objects.filter(order=order[0]).values('progress')
                update = sorted(update_progress, key=get_choices, reverse=True)
                orders.append([order, update])

            params = {'orders': orders}
            return render(request, 'tracker.html', params)
        else:
            params = {'error': 'Looks like you haven\'t placed any orders yet!'}
            return render(request, 'tracker.html', params)
    else:
        return redirect('StoreAccount')

 # Extra usage functions

def make_binary(reviews):
    no_reviews = len(reviews)
    stars = [0, 0, 0, 0, 0]

    if no_reviews > 0:    
        rating = 0
        
        for review in reviews:
            rating += review.stars
        
        star = rating//no_reviews
        rating = rating/no_reviews

        for i in range(star):
            stars[i] = 2

        if (rating - star) > 0:
            stars[star] = 1

        return round(rating, 1), stars, no_reviews
    else:
        return 0.0, stars, no_reviews


def search_alg(query, item):
    query = query.lower()
    query_match = (query in item.features.lower()) or (query in item.name.lower()) or (
            query in item.category.lower()) or (query in item.sub_category.lower())
    if query_match:
        return True
    else:
        return False


def login_user(request, email, password):
    username = email.split('@')[0]
    user = authenticate(username=username, password=password)

    if user is not None:
        login(request=request, user=user)
        return True
    else:
        return False


def create_user(request, first_name, last_name, email, password):
    username = email.split('@')[0]
    user_exists = User.objects.filter(username=username).exists()
    if user_exists:
        return False
    else:
        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = first_name
        user.last_name = last_name
        # user.password = password
        user.save()

        login(request, user)
    
    return True


def get_val(element):
    return element['order_id']

def get_choices(element):
    return element['progress']
    

# Abdullah Func
def logout_user(request):
    logout(request)
    return redirect('StoreHome')