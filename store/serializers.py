from rest_framework import serializers
from .models import Product, Collection, Reviews, Cart, CartItem
from decimal import Decimal

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ["id", "title"]




class ProductSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)
    # changed_price = serializers.DecimalField(max_digits=10, decimal_places=2, source="amount")
    # inventory = serializers.IntegerField()
    price_with_tax = serializers.SerializerMethodField(method_name="calculate_price_with_tax")
    collection = CollectionSerializer()

    def calculate_price_with_tax(self, prod:Product):
            price = prod.amount * Decimal(0.5) # making sure decimal multiplies decimal
            return price
    
    class Meta:
        model = Product
        fields = ["id", "title", "amount", "inventory", "price_with_tax", "collection"] # "__all__" 

    


class ReviewSerializer(serializers.ModelSerializer):
     class Meta:
          model = Reviews
          fields = ["id", "name", "description", "product", "date"]




class CartItemsSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cartitem: CartItem):
         return cartitem.quantity * cartitem.product.amount
    class Meta:
        model = CartItem
        fields = ["id", "quantity", "total_price", "product"]

class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def save(self, **kwargs):
        # we can get all the data supplied during create request through the validated_data dict
        product_id = self.validated_data["product_id"]
        quantity = self.validated_data["quantity"]
        # we get the cart id from the context we setup in our views
        cart_id = self.context["cart_id"]

        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            # We update this item if it exists
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            # We create a new cart item
            created_item = CartItem.objects.create(cart_id=cart_id, product_id=product_id, quantity=quantity)
            self.instance = created_item

        return self.instance
    class Meta:
        model = CartItem
        fields = ["id", "product_id", "quantity"]


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["quantity"]


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    items = CartItemsSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart: Cart):
         return sum([item.quantity * item.product.amount for item in cart.items.all()])
    
    class Meta:
        model = Cart
        fields = ["id", "created_at", "items", "total_price"]


"""
ADDING NEW FIELDS
We can add fields that are not originally in our Data Model, just like in "price_with_tax"

CHANGING FIELD NAMES
You can change name if the fields in this serializer, by utilizing "source=" to point it to the DB

"""