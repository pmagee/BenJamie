from django.shortcuts import redirect, render, get_object_or_404
from products.models import Product
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
import stripe
from django.conf import settings
from django.urls import reverse
from order.models import Order, OrderItem
from stripe import StripeError


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist: 
        cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        if (cart_item.quantity < cart_item.product.stock):
            cart_item.quantity +=1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(product=product, quantity=1,cart=cart)
    return redirect('cart:cart_detail') 

def cart_detail(request, total=0, counter=0, cart_items = None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            counter += cart_item.quantity
    except ObjectDoesNotExist:
        pass

    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe_total = int(total * 100)  # Convert total to cents
    description = 'Online Shop - New Order'
    

    if request.method == 'POST':
        try:
            # Create a new Stripe Checkout session
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'eur',
                        'product_data': {
                            'name': 'Order from Computer Store',
                        },
                        'unit_amount': stripe_total,
                    },
                    'quantity': 1,
                }],
                mode='payment',
 		   billing_address_collection='required', 
                shipping_address_collection={},
                payment_intent_data={'description': description},
                success_url=request.build_absolute_uri(reverse('cart:new_order'))+ f"?session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url=request.build_absolute_uri(reverse('cart:cart_detail')),    
            )
            # Redirect to Stripe Checkout
            return redirect(checkout_session.url, code=303)
        except Exception as e:
            # Render the template with an error message
            return render(request, 'cart.html', {
                'cart_items': cart_items,
                'total': total,
                'counter': counter,
                'error': str(e),  # Display error if there's an issue with Stripe
            })

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total,
        'counter': counter,
    })


def cart_remove(request, product_id):
    cart= Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart:cart_detail')

def full_remove(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart:cart_detail')

def empty_cart(request):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, active=True)
        cart_items.delete()  
        cart.delete()
        return redirect('products:all_products')
    except Cart.DoesNotExist:
        pass
    return redirect('cart:cart_detail')

def create_order(request):
    try:
        session_id = request.GET.get('session_id')
        if not session_id:
            raise ValueError("Session ID not found.")

        try:
            session = stripe.checkout.Session.retrieve(session_id)
        except StripeError as e:
            return redirect("products:all_products") 

        customer_details = session.customer_details
        if not customer_details or not customer_details.address:
            raise ValueError("Missing information in the Stripe session.")

        billing_name = customer_details.name
        shipping_address = customer_details.address
        shipping_name = customer_details.name

        try:
            order_details = Order.objects.create(
                token=session.id,
                total=session.amount_total / 100,  # Convert cents to currency units
                emailAddress=customer_details.email,
                billingName=billing_name,
                shippingName=shipping_name,
                shippingAddress1=shipping_address.line1, 
                shippingCity=shipping_address.city, 
                shippingCountry=shipping_address.country,
            )
            order_details.save()
        except Exception as e: 
            print(f"Error: {e}")
            return redirect("products:all_products") 

        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, active=True)
        except ObjectDoesNotExist:
            return redirect("products:all_products")  
        except Exception as e:
            print(f"Error: {e}")
            return redirect("products:all_products")  

        for item in cart_items:
            try:
                oi = OrderItem.objects.create(
                    product=item.product.name,
                    quantity=item.quantity,
                    price=item.product.price,
                    order=order_details
                )
                oi.save()
                '''Reduce stock when order is placed or saved'''
                product = Product.objects.get(id=item.product.id)
                product.stock = int(item.product.stock - item.quantity)
                product.save()
                empty_cart(request)
            except Exception as e:
                return redirect("products:all_products")  
        return redirect('order:thanks', order_details.id)

    except ValueError as ve:
        print(f"Error: {ve}")
        return redirect("products:all_products")  

    except StripeError as se:
        print(f"Stripe Error: {se}")
        return redirect("products:all_products") 

    except Exception as e:
        print(f"Unexpected error: {e}")
        return redirect("products:all_products") 
