from django.conf import settings
from product.models import Product
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)

class Cart:
    def __init__(self, request):
        self.session = request.session
        self.request = request
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        
    def add(self, product, color=None):
        try:
            # Validate product exists and is active
            if not Product.objects.filter(id=product.id, is_active=True).exists():
                raise ValueError('Product Not Found or Inactive!')
            
            # Check stock availability
            current_quantity = self.cart.get(str(product.id), {}).get('quantity', 0)
            if current_quantity >= product.quantity:
                raise ValueError('Insufficient stock!')
            
            product_id = str(product.id)
            
            # Determine price
            if product.is_sale and product.sale_price > 0:
                price = str(product.sale_price)
            else:
                price = str(product.price)
            
            # Validate color if provided
            color_name = None
            if color:
                if not hasattr(color, 'color') or not color.color:
                    raise ValueError('Invalid color!')
                color_name = color.color
            
            if product_id not in self.cart:
                self.cart[product_id] = {
                    'quantity': 1,
                    'price': price,
                    'original_price': str(product.price),
                    'is_sale': product.is_sale,  
                    'color_name': color_name
                }
            else:
                self.cart[product_id]['quantity'] += 1
            self.save()
            
        except Exception as e:
            logger.error(f"Error adding product to cart: {str(e)}")
            raise

    def save(self):
        self.session.modified = True
        
    def remove(self, product):
        try:
            product_id = str(product.id)
            if product_id in self.cart:
                if self.cart[product_id]['quantity'] > 1:
                    self.cart[product_id]['quantity'] -= 1
                else:
                    del self.cart[product_id]
                self.save()
        except Exception as e:
            logger.error(f"Error removing product from cart: {str(e)}")
            raise
    
    def delete(self, product):
        try:
            product_id = str(product.id)
            if product_id in self.cart:
                del self.cart[product_id]
                self.save()
        except Exception as e:
            logger.error(f"Error deleting product from cart: {str(e)}")
            raise
        
    def __iter__(self):
        try:
            product_ids = list(self.cart.keys())
            if not product_ids:
                return
            
            # Get only active products
            products = Product.objects.filter(id__in=product_ids, is_active=True)
            cart = self.cart.copy()
            
            # Remove products that no longer exist or are inactive
            for product_id in list(cart.keys()):
                if not any(str(p.id) == product_id for p in products):
                    del cart[product_id]
                    self.cart = cart
                    self.save()
            
            for product in products:
                product_id = str(product.id)
                if product_id in cart:
                    cart[product_id]['product_id'] = product.id
                    cart[product_id]['product'] = product
                    
            for item in cart.values():
                if 'product' in item:  # Only process items with valid products
                    item['price'] = Decimal(item['price'])
                    item['total_price'] = item['price'] * item['quantity']
                    yield item
                    
        except Exception as e:
            logger.error(f"Error iterating cart: {str(e)}")
            return

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values() if isinstance(item, dict))

    def get_total(self):
        return float(sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values()))

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()