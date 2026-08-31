from django.db import models
from django.core.validators import MinValueValidator
from uuid import uuid4

# Create your models here.


class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()

    def __str__(self):
        shortened = self.description[:60] + "..."
        return shortened

class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey("Product", on_delete=models.SET_NULL, null=True, related_name="+")

    def __str__(self):
        return self.title

    # class Meta:
    #     ordering = ["title"]

class Product(models.Model):
    BRONZE = "B"
    SILVER = "S"
    GOLD = "G"

    MEMBERSHIP_CHOICES = [
        (BRONZE, "Bronze"),
        (SILVER, "Silver"),
        (GOLD, "Gold"),
    ]

    # custom_id = models.CharField(max_length=20, primary_key= True) # if you want another pk aside the auto id created by django
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators= [MinValueValidator(1)])
    inventory = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=BRONZE)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT, related_name="products") # With PROTECT, deleting a collection doesn't delete all the products in it
    promotions = models.ManyToManyField(Promotion, related_name="products", blank=True) # So one product can have multiple promotions vice versa; the related name overrides the default text Django will use to store products (product_set) in the Promotion Table. 

    def __str__(self):
        return f"{self.title} - Amount #{self.amount}"



class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    birth_date = models.DateField(null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    class Meta:
        indexes = [
            models.Index(fields=["last_name", "first_name"])
        ]



class Order(models.Model):
    PENDING = "P"
    COMPLETE = "C"
    FAILED = "F"

    PAYMENT_STATUS = [
        (PENDING, "Pending"),
        (COMPLETE, "Complete"),
        (FAILED, "Failed"),
    ]

    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS, default=PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return f"Order Placed At - {self.placed_at}"




class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="orderitems")
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.title} | Quantity: {self.quantity}"

class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    # Case where a customer can have only one address
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, primary_key=True) # We can have SET_NULL -  to set this field NULL after customer is deleted, SET_DEFAULT - to set a default value to this field after customer is deleted, PROTECT - to protect deletion
    # Case where a customer can have many/multiple addresses. NB -  the pk field is removed to allow many-to-one relationship
    # customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.customer.first_name} - {self.city},{self.state}"



class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.created_at.isoformat()


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.product.title} | In Cart: {self.quantity}"   

    class Meta:
        unique_together = [["cart", "product"]] 


class Reviews(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)





"""
NB: Product has a circular dependency on Collection | A collection can have a featured_product but the field is nullable

In Django models.py files, this usually happens when Model A has a ForeignKey to Model B, and Model B simultaneously has a ForeignKey to Model A.

Imagine you have two apps: orders and customers:

#### Inside orders/models.py
from customers.models import Customer  # <-- Imports Customer

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    
#### Inside customers/models.py
from orders.models import Order  # <-- Crucial mistake: Imports Order back!

class Customer(models.Model):
    favorite_order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)


PROBLEM: When Django starts, it reads orders/models.py, which stops to read customers/models.py, which stops to read orders/models.py... Python gets stuck in a loop and crashes.

SOLUTION: Pass the relationship as a String format...this tells Python -- "Don't look for this model right now during import. Wait until all apps are fully loaded, then link them together.

BELOW ARE THE SOLVED MODELS:

# Inside orders/models.py
class Order(models.Model):
    # No import needed! Django finds it via the app name string
    customer = models.ForeignKey('customers.Customer', on_delete=models.CASCADE)

# Inside customers/models.py
class Customer(models.Model):
    # No import needed! 
    favorite_order = models.ForeignKey('orders.Order', on_delete=models.SET_NULL, null=True)



    

UNDOING A MIGRATIONS:
Run the command: python3 manage.py migrate store 0003

Where 0003 is the migrations number and the "store" is the name of the app
"""



