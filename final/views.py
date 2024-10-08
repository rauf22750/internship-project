# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.signing import Signer, BadSignature
from .models import product, UserProfile, ProductImage, cartitem ,Order , OrderItem
from django.http import Http404
from django.views.decorators.cache import never_cache
from django.contrib.auth.models import User
from django.core import signing
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import timedelta
from django.http import HttpResponseForbidden
from django.db.models import Avg
from .models import  ProductReview  # Adjust imports as necessary
from .forms import ProductReviewForm
from django.core.files.storage import FileSystemStorage
import stripe
from django.conf import settings

import json

stripe.api_key = settings.STRIPE_SECRET_KEY

@never_cache
def welcomepage(request):
    data = product.objects.filter(is_approved=True).prefetch_related('images')
    for item in data:
        item.encrypted_id = signing.dumps(item.id)
    return render(request, 'app1/main.html', {'data': data})

@never_cache
def signaction(request):
    if request.method == "POST":
        if request.POST.get('password1') == request.POST.get('password2'):
            try:
                saveuser = User.objects.create_user(
                    username=request.POST.get("name"),
                    email=request.POST.get("email"),
                    password=request.POST.get("password1")
                )
                saveuser.save()
                
                user_profile = UserProfile(
                    user=saveuser,
                    email=request.POST.get("email")
                )
                user_profile.save()

                return render(request, 'app1/signup_page.html', {'form': UserCreationForm(), 'info': f'This user {request.POST.get("name")} is successfully registered'})
            except IntegrityError:
                return render(request, 'app1/signup_page.html', {'form': UserCreationForm(), 'info': f'This user {request.POST.get("name")} already exists'})
        else:
            return render(request, 'app1/signup_page.html', {'form': UserCreationForm(), 'error': 'Passwords do not match'})
    else:
        return render(request, 'app1/signup_page.html')
@never_cache
def loginuser(request):
    if request.method == "POST":
        username = request.POST.get('name')
        password = request.POST.get('password')
        loginsuccess = authenticate(request, username=username, password=password)
        if loginsuccess is None:
            return render(request, 'app1/login_page.html', {'form': AuthenticationForm(), 'error': 'This name and password do not match'})
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return render(request, 'app1/login_page.html', {'form': AuthenticationForm(), 'error': 'This user does not exist'})

        try:
            userprofile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            return render(request, 'app1/login_page.html', {'form': AuthenticationForm(), 'error': 'User profile does not exist'})

        if not userprofile.is_approved:
            return render(request, 'app1/login_page.html', {'form': AuthenticationForm(), 'error': 'This user is not approved'})

        login(request, loginsuccess)
        
        return redirect('/')
    else:
        return render(request, 'app1/login_page.html', {'form': AuthenticationForm()})
    
@login_required
def add_to_cart(request):
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        
        prod = get_object_or_404(product, id=product_id)
        total_price = prod.price * quantity
        
        # Check if the cart item already exists
        cart_item, created = cartitem.objects.get_or_create(
            user=request.user,
            product=prod,
            defaults={'quantity': quantity, 'total_price': total_price}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.total_price = cart_item.quantity * prod.price
            cart_item.save()
        
        return redirect('cart_view')

    return redirect('productdetail/<str:id>/', id=product_id)


@login_required
def cart_view(request):
    if request.method == "POST":
        action = request.POST.get('action')
        item_id = int(request.POST.get('item_id'))
        cart_item = get_object_or_404(cartitem, id=item_id, user=request.user)
        
        if action == "increase":
            cart_item.quantity += 1
        elif action == "decrease":
            cart_item.quantity -= 1
            if cart_item.quantity <= 0:
                cart_item.delete()
                return JsonResponse({'success': True, 'item_removed': True})
        cart_item.total_price = cart_item.quantity * cart_item.product.price
        cart_item.save()
        return JsonResponse({'success': True, 'quantity': cart_item.quantity, 'total_price': cart_item.total_price})
    
    cart_items = cartitem.objects.filter(user=request.user)
    context = {
        'cart_items': cart_items
    }
    return render(request, 'app1/cart.html', context)

@login_required
def remove_from_cart(request):
    if request.method =="POST":
        item_id = request.POST.get('item_id')
        cart_item = get_object_or_404(cartitem, id = item_id , user=request.user)
        cart_item.delete()
        return JsonResponse({'success':True})
    return redirect('cart_view')

# @login_required
# def checkout(request):
#     if request.method == "POST":
#         phone = request.POST.get('phone')
#         address = request.POST.get('address')
#         cart_items = cartitem.objects.filter(user=request.user)

#         if cart_items.exists():
#             total_amount = sum(item.total_price for item in cart_items)
            
#             # Create a new order
#             order = Order.objects.create(
#                 user=request.user,
#                 total_amount=total_amount,
#                 mobile=phone,
#                 address=address
#             )
            
#             # Save each cart item as an order item
#             for item in cart_items:
#                 OrderItem.objects.create(
#                     order=order,
#                     product=item.product,
#                     quantity=item.quantity,
#                     total_price=item.total_price
#                 )
#                 item.delete()

#             return JsonResponse({'success': True})
#         else:
#             return JsonResponse({'success': False, 'error': 'Cart is empty'})

#     return redirect('cart_view')
@login_required
def checkout(request):
    if request.method == "POST":
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        cart_items = cartitem.objects.filter(user=request.user)

        if cart_items.exists():
            total_amount = sum(item.total_price for item in cart_items)
            order = Order.objects.create(
                user=request.user,
                total_amount=total_amount,
                mobile=phone,
                address=address
            )

            line_items = []
            total_amount = 0
            
            for item in cart_items:
                total_amount += item.total_price
                # Add the item to the line_items for Stripe
                line_items.append({
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': item.product.p_name,  # Assuming 'p_name' is the correct field
                        },
                        'unit_amount': int(item.product.price * 100),  # Price in cents
                    },
                    'quantity': item.quantity,
                })
                
                # Create an OrderItem for each item in the cart
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    total_price=item.total_price
                )
                
                

                # Remove item from the cart
                item.delete()

            # Create a Stripe Checkout session
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                success_url='http://localhost:8000/success/',  # Define your success URL
                cancel_url='http://localhost:8000/cancel/',  # Define your cancel URL
            )
            
            return redirect(session.url, code=303)
        else:
            return JsonResponse({'success': False, 'error': 'Cart is empty'})

    return redirect('cart_view')


def success(request):
    return render(request, 'app1/order_success.html')

def cancel(request):
    return render(request, 'app1/cancel.html')


def order(request):
    orders = Order.objects.filter(user=request.user)
    
    # Get the set of product IDs that the user has reviewed
    reviewed_products = ProductReview.objects.filter(user=request.user).values_list('product_id', flat=True)
    reviewed_products_set = set(reviewed_products)
    
    context = {
        'orders': orders,
        'reviewed_products': reviewed_products_set,  # Pass the set of reviewed product IDs
    }
    return render(request, 'app1/order.html', context)

@login_required
def vendor_orders(request):
    vendor = request.user
    orders = Order.objects.filter(items__product__user=vendor).distinct()
    
    context = {
        'orders': orders,
    }
    return render(request, 'app1/vendor_orders.html', context)

@login_required
def update_item_status(request, item_id):
    if request.method == "POST":
        item = get_object_or_404(OrderItem, id=item_id, product__user=request.user)
        item.order_status = request.POST.get('order_status')
        item.save()
        return redirect('vendor_orders')
    return HttpResponseForbidden("You cannot update this item.")

@login_required
def add_review(request, product_id):
    prod = get_object_or_404(product, id=product_id)
    
    if request.method == 'POST':
        review_text = request.POST.get('review_text')
        review_rating = request.POST.get('review_rating')
        review_images = request.FILES.getlist('review_images')

        if review_text and review_rating:
            review = ProductReview.objects.create(
                user=request.user,
                product=prod,
                review_text=review_text,
                review_rating=review_rating
            )

            image_urls = []
            fs = FileSystemStorage()

            for image in review_images:
                file_name = fs.save(f'reviews/{image.name}', image)
                file_url = fs.url(file_name)
                image_urls.append(file_url)

            review.images = image_urls
            review.save()
            
            return redirect('order')
    return redirect('order')
@login_required
@never_cache
def signout(request):
    logout(request)
    request.session.flush()
    return redirect('/')

@login_required
@never_cache
def productlist(request):
    current_user = request.user
    data = product.objects.filter(user=current_user).prefetch_related('images')
    signer = Signer()
    for item in data:
        item.signed_id = signer.sign(item.id)

    return render(request, 'app1/productlist.html', {'data': data})

@login_required
@never_cache
def productadd(request):
    if request.method == "POST":
        p_name = request.POST.get("productname")
        pictures = request.FILES.getlist("pictures[]")
        color = request.POST.get("color")
        price = request.POST.get("price")
        detail = request.POST.get("details")

        product_instance = product(
            p_name=p_name,
            color=color,
            price=price,
            detail=detail,
            user=request.user
        )
        product_instance.save()

        for picture in pictures:
            ProductImage.objects.create(product=product_instance, image=picture)

        return redirect('/productlist/')
    
    return render(request, 'app1/productadd.html')

def productdetail(request, id):
    try:
        decrypted_id = signing.loads(id)
        data = product.objects.prefetch_related('images', 'reviews').get(id=decrypted_id)
    except signing.BadSignature:
        raise Http404("Invalid product ID")
    
    return render(request, 'app1/productdetail.html', {'data': data, 'reviews': data.reviews.all()})

@login_required
@never_cache
def productupdate(request, signed_product_id):
    signer = Signer()
    try:
        product_id = signer.unsign(signed_product_id)
    except BadSignature:
        return redirect('error_page')

    prod = get_object_or_404(product, id=product_id)

    if request.method == "POST":
        p_name = request.POST.get("productname")
        pictures = request.FILES.getlist("pictures[]")
        color = request.POST.get("color")
        price = request.POST.get("price")
        detail = request.POST.get("details")
        images_to_keep = request.POST.getlist("existing_images")

        prod.p_name = p_name
        prod.color = color
        prod.price = price
        prod.detail = detail
        prod.save()

        ProductImage.objects.filter(product=prod).exclude(id__in=images_to_keep).delete()

        current_image_count = ProductImage.objects.filter(product=prod).count()
        new_images_limit = 8 - current_image_count

        for picture in pictures[:new_images_limit]:
            ProductImage.objects.create(product=prod, image=picture)

        return redirect('/productlist/')

    current_user = request.user
    data = product.objects.prefetch_related('images').filter(user=current_user)
    signed_product_id = signer.sign(product_id)

    return render(request, 'app1/update.html', {'product': prod, 'data': data, 'signed_product_id': signed_product_id})

@login_required
@never_cache
def productdelete(request):
    current_user = request.user
    if request.method == "POST":
        p_id = request.POST.get('product_id')
        if p_id:
            data_id = get_object_or_404(product, id=p_id, user=current_user)
            data_id.delete()
        return redirect('productlist')
    
    return render(request, 'app1/productlist.html')
def sign(request):
    return render(request, 'app1/sign.html')
