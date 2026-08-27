from rest_framework import serializers
from .models import Product, Collection, Reviews
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

    


class ReviewSerializer(serializers.Serializer):
     class Meta:
          model = Reviews
          fields = ["id", "name", "description", "product", "date"]


"""
ADDING NEW FIELDS
We can add fields that are not originally in our Data Model, just like in "price_with_tax"

CHANGING FIELD NAMES
You can change name if the fields in this serializer, by utilizing "source=" to point it to the DB

"""