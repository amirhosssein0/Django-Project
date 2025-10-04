from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from .forms import ShipingForm
from cart.utils import Cart  
from django.shortcuts import render
from product.models import Product
from decimal import Decimal
from django.contrib import messages
from django.views.generic import TemplateView, DetailView
from django.views.generic import View
from .models import Order, OrderItem
from django.db import transaction


class ShippingView(LoginRequiredMixin, FormView):
    template_name = 'payment/shipping.html'
    form_class = ShipingForm
    success_url = reverse_lazy('payment:checkout')

    def dispatch(self, request, *args, **kwargs):
        cart = Cart(request)
        if len(cart) == 0:  
            messages.error(request, 'Your Cart Is Empty')
            return redirect('cart:cart')  
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        if hasattr(self.request.user, 'profile'):
            profile = self.request.user.profile
            initial.update({
                'shiping_full_name': f"{profile.first_name} {profile.last_name}",
                'shiping_phone': profile.phone,
                'shiping_address': profile.address
            })
        return initial

    def form_valid(self, form):
        shipping_address = form.save(commit=False)
        shipping_address.user = self.request.user
        shipping_address.save()
        return super().form_valid(form)

class CheckoutView(LoginRequiredMixin, TemplateView):
    template_name = 'payment/checkout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        cart_products = []
        total_cart_price = 0
        
        for item in cart.__iter__():
            try:
                product_id = item.get('product_id', str(item['product'].id))
                price = Decimal(item['price'])
                item_total = price * item['quantity']
                total_cart_price += item_total
                cart_products.append({
                    'product_id': product_id,  
                    'product': item['product'],
                    'quantity': item['quantity'],
                    'price': price,
                    'original_price': str(Decimal(item.get('original_price', item['price']))),
                    'is_sale': item.get('is_sale', False),
                    'total_price': item_total,
                    'color_name': item.get('color_name', 'N/A'),
                })
            except (Product.DoesNotExist, ValueError, KeyError):
                del cart.cart[product_id]
                cart.save()
        context['cart_products'] = cart_products
        context['total_cart_price'] = total_cart_price
        return context

class FinalCheckView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        if not cart.cart:
            messages.error(request, "Your Cart Is Empty")
            return redirect('cart:cart')  
        
        user_shipping = {
            'shiping_full_name': request.POST.get('shiping_full_name'),
            'shiping_phone': request.POST.get('shiping_phone'),
            'shiping_address': request.POST.get('shiping_address')
        }
        
        cart_products = []
        total_cart_price = Decimal('0')
        
        for item in cart.__iter__():  
            try:
                product_id = str(item['product'].id)
                price = Decimal(str(item['price']))
                quantity = int(item['quantity'])
                item_total = price * quantity
                total_cart_price += item_total
                
                cart_products.append({
                    'product_id': product_id,
                    'product_name': item['product'].name, 
                    'quantity': quantity,
                    'price': str(price),  
                    'original_price': str(Decimal(item.get('original_price', price))),
                    'is_sale': bool(item.get('is_sale', False)),
                    'total_price': str(item_total),  
                    'color_name': str(item.get('color_name', 'N/A')),
                })
            except (KeyError, ValueError) as e:
                if 'product' in item:
                    del cart.cart[str(item['product'].id)]
                    cart.save()
        
        request.session['checkout_data'] = {
            'shipping_info': user_shipping,
            'cart_products': cart_products,
            'total_cart_price': str(total_cart_price) 
        }
        
        context = {
            'cart_products': [{
                **item,
                'product': cart.cart[item['product_id']]['product'],
                'total_price': Decimal(item['total_price']) if isinstance(item['total_price'], str) else item['total_price']
            } for item in cart_products],
            'total_cart_price': total_cart_price,
            'shipping_info': user_shipping,
        }
        
        return render(request, 'payment/final_check.html', context)
        
class ProcessOrderView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        if not cart.cart:
            messages.error(request, "Your Cart Is Empty")
            return redirect('cart:cart')

        checkout_data = request.session.get('checkout_data')
        if not checkout_data:
            messages.error(request, "Checkout Data Not Found")
            return redirect('payment:checkout')

        try:
            with transaction.atomic():
                for product_id, item in cart.cart.items():
                    product = Product.objects.select_for_update().get(id=int(product_id))
                    if product.quantity < item['quantity']:
                        raise ValueError('Quantity Not Enough')

                total = float(cart.get_total())  
                new_order = Order(
                    user=request.user,
                    full_name=checkout_data['shipping_info'].get('shiping_full_name'),
                    address=checkout_data['shipping_info'].get('shiping_address'),
                    amount_paid=total,
                )
                new_order.save()

                for item in cart.__iter__():
                    product_id = str(item['product'].id)
                    product = Product.objects.select_for_update().get(id=int(product_id))
                    product.quantity -= item['quantity']
                    product.save()
                    
                    OrderItem.objects.create(
                        order=new_order,
                        product=product,
                        user=request.user,
                        quantity=item['quantity'],
                        price=float(item['price'])  
                    )

                cart.clear()
                messages.success(request, "Your Order Received")
                return redirect('product:products')

        except Product.DoesNotExist as e:
            messages.error(request, "One Of Your Order Not Found")
            return redirect('payment:checkout')
            
        except ValueError as e:
            messages.warning(request, str(e))
            return redirect('cart:cart_summary')
            
        except Exception as e:
            messages.error(request, "There Is A Problem")
            return redirect('payment:checkout')
        
class OrderDetailView(LoginRequiredMixin, DetailView):
    model=Order
    template_name = 'payment/order_detail.html'
    context_object_name = 'order'
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.object
        context['items'] = OrderItem.objects.filter(order=order)
        return context
