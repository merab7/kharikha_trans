from store.models import Product, ProductSize
from datetime import datetime, timedelta

class Cart:
    def __init__(self, request) -> None:
        self.session = request.session
        if 'cart' not in self.session:
            self.session['cart'] = {}
            self.session['cart_last_updated'] = datetime.now().isoformat()
        
        self.cart = self.session['cart']
        self.last_updated = datetime.fromisoformat(self.session['cart_last_updated'])
        
        # Clear the cart if more than 60 minutes have passed since the last update
        if datetime.now() - self.last_updated > timedelta(minutes=60):
            self.clear_cart()

    def update_timestamp(self):
        self.last_updated = datetime.now()
        self.session['cart_last_updated'] = self.last_updated.isoformat()
        self.session.modified = True

    def add(self, product=None, size=int(), quantity=int()):
        product_id = int(product.id)
        name = str(product.name)
        price = int(product.price)
        size = str(size)
        quantity = quantity
        
        # Generate a unique key for the product and size combination
        cart_key = f"{product_id}_{size}"

        # Check if the product and size combination is already in the cart
        if cart_key in self.cart:
            # Update the quantity if it already exists
            self.cart[cart_key]['quantity'] += quantity
        else:
            # If it doesn't exist, add it to the cart
            self.cart[cart_key] = {'id': product_id, 'name': name, 'price': price, 'size': size, 'quantity': quantity}
        
        self.update_timestamp()

    def update(self, cart_key=None, product=None, size=int(), quantity=int()):
        product_id = int(product.id)
        name = str(product.name)
        price = int(product.price)
        size = str(size)
        quantity = quantity
        new_cart_key = f"{product_id}_{size}"
        
        # Delete existing item
        self.cart.pop(cart_key, None)
        # Add new item
        self.cart[new_cart_key] = {'id': product_id, 'name': name, 'price': price, 'size': size, 'quantity': quantity}
        
        self.update_timestamp()

    def delete(self, cart_key=None):
        item_details = self.get_item_details(cart_key)
        if item_details:
            # Remove the item from the cart
            self.cart.pop(cart_key)
            self.session.modified = True
        return item_details  # Return details of the deleted item

    def get_item_details(self, cart_key):
        return self.cart.get(cart_key, None)

    def clear_cart(self):
        # Restore quantities to the database
        self.restore_quantities()
        # Clear the cart and reset timestamp
        self.cart = {}
        self.session['cart'] = {}
        self.update_timestamp()

    def restore_quantities(self):
        for cart_key, item in self.cart.items():
            product_id = item['id']
            size = item['size']
            quantity = item['quantity']

            product = Product.objects.get(id=product_id)
            size_count = ProductSize.objects.filter(product=product)

            for item in size_count:
                if item.size == size:
                    item.quantity += quantity
                    item.save()

        # After restoring quantities, empty the cart
        self.cart = {}
        self.session['cart'] = {}
        self.session.modified = True

    def __len__(self):
        return len(self.cart)

    def get_products(self):
        # Extract product IDs from the keys in the cart
        product_ids = [key.split('_')[0] for key in self.cart.keys()]
        
        # Retrieve products from the database based on the extracted product IDs
        products = Product.objects.filter(id__in=product_ids)
    
        return products

    def get_quantities(self):
        return self.cart

    def contains(self, product, size):
        cart_key = f"{product.id}_{size}"
        return cart_key in self.cart
    
    def is_empty(self):
       return len(self.cart) == 0
