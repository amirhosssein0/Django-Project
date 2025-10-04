from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from .utils import Cart
from product.models import Product, Color
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)


class CartSummaryView(TemplateView):
    template_name = 'cart/cart_summary.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        
        cart_products = []
        total_cart_price = Decimal('0')
        
        for item in cart.__iter__(): 
            try:
                product_id = item.get('product_id', str(item['product'].id))
                
                if item['quantity'] > item['product'].quantity:
                    item['quantity'] = item['product'].quantity
                    cart.cart[product_id]['quantity'] = item['product'].quantity
                    cart.save()
                
                cart_products.append({
                    'product_id': product_id,  
                    'product': item['product'],
                    'quantity': item['quantity'],
                    'price': float(item['price']),
                    'original_price': float(Decimal(item.get('original_price', item['price']))),
                    'is_sale': item.get('is_sale', False),
                    'total_price': float(item['total_price']),
                    'color_name': item.get('color_name', 'N/A'),
                })
                total_cart_price += item['total_price']
                
            except (KeyError, ValueError) as e:
                if 'product' in item:
                    del cart.cart[str(item['product'].id)]
                    cart.save()
        
        context['cart_products'] = cart_products
        context['total_cart_price'] = float(total_cart_price)
        return context


class CartAddView(View):
    def post(self, request, *args, **kwargs):
        try:
            cart = Cart(request)
            if request.POST.get('action') != 'post':
                return JsonResponse({'error': 'Invalid action'}, status=400)
            
            # Validate product_id
            try:
                product_id = int(request.POST.get('product_id'))
                if product_id <= 0:
                    raise ValueError("Invalid product ID")
            except (ValueError, TypeError):
                return JsonResponse({'error': 'Invalid product ID'}, status=400)
            
            # Get product with validation
            try:
                product = Product.objects.get(id=product_id, is_active=True)
            except Product.DoesNotExist:
                return JsonResponse({'error': 'Product not found or inactive'}, status=404)
            
            # Check stock availability
            current_quantity = cart.cart.get(str(product_id), {}).get('quantity', 0)
            if current_quantity >= product.quantity:
                return JsonResponse({'error': 'No Quantity Available'}, status=400)
            
            # Handle color validation
            color = None
            product_color_id = request.POST.get('product_color')
            if product_color_id:
                try:
                    color = Color.objects.get(id=product_color_id, product=product)
                except Color.DoesNotExist:
                    return JsonResponse({'error': 'Invalid color selection'}, status=400)
            
            # Add to cart
            cart.add(product=product, color=color)
            cart_quantity = cart.__len__()
            
            response = JsonResponse({
                'quantity': cart_quantity,
                'item_quantity': cart.cart[str(product_id)]['quantity'],
                'success': True
            })
            return response
            
        except Exception as e:
            logger.error(f"Error in CartAddView: {str(e)}")
            return JsonResponse({'error': 'Internal server error'}, status=500)


class CartRemoveView(View):
    def post(self, request, *args, **kwargs):
        try:
            cart = Cart(request)
            if request.POST.get('action') != 'post':
                return JsonResponse({'error': 'Invalid action'}, status=400)
            
            # Validate product_id
            try:
                product_id = int(request.POST.get('product_id'))
                if product_id <= 0:
                    raise ValueError("Invalid product ID")
            except (ValueError, TypeError):
                return JsonResponse({'error': 'Invalid product ID'}, status=400)
            
            # Get product
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return JsonResponse({'error': 'Product not found'}, status=404)
            
            # Remove from cart
            cart.remove(product=product)
            cart_quantity = cart.__len__()
            
            response = JsonResponse({
                'quantity': cart_quantity,
                'item_quantity': cart.cart.get(str(product_id), {}).get('quantity', 0),
                'success': True
            })
            return response
            
        except Exception as e:
            logger.error(f"Error in CartRemoveView: {str(e)}")
            return JsonResponse({'error': 'Internal server error'}, status=500)


class CartDeleteView(View):
    def post(self, request, *args, **kwargs):
        try:
            cart = Cart(request)
            if request.POST.get('action') != 'post':
                return JsonResponse({'error': 'Invalid action'}, status=400)
            
            # Validate product_id
            try:
                product_id = int(request.POST.get('product_id'))
                if product_id <= 0:
                    raise ValueError("Invalid product ID")
            except (ValueError, TypeError):
                return JsonResponse({'error': 'Invalid product ID'}, status=400)
            
            # Get product
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return JsonResponse({'error': 'Product not found'}, status=404)
            
            # Delete from cart
            cart.delete(product=product)
            cart_quantity = cart.__len__()
            
            response = JsonResponse({
                'quantity': cart_quantity,
                'success': True
            })
            return response
            
        except Exception as e:
            logger.error(f"Error in CartDeleteView: {str(e)}")
            return JsonResponse({'error': 'Internal server error'}, status=500)
