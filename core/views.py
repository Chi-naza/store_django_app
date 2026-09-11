from django.shortcuts import render

from django.http import HttpResponse
from django.db.models import Q
from django.db.models.aggregates import Count, Max, Min, Avg, Sum
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
# from rest_framework_simplejwt.views import TokenObtainPairView
# from rest_framework_simplejwt.tokens import RefreshToken



from store.models import Product, Order, Promotion, Collection, Customer
from tags.models import TagItem
from .serializers import UserSerializer, CustomTokenObtainPairSerializer, RegisterSerializer



# Create your views here.

def home(request):
    return render(request, "index.html")

def say_hello(request):
    query_set = Product.objects.all()

    # Querying related models. Django quries the main model you are retriving from and to query any model related to it, you need to specify that 
    # Eg Querying Collection Alongside the main Product Model
    query_set = Product.objects.select_related("collection").all()

    # Problem: Get the last 5 orders with their customer and items (including product)
    # Where 'orderitem_set' is the auto field created on the Order Model by Django because of the relationship added to the OrderItem Model
    # User select_related when the other end of the r/lship has one item Eg Product has one customer | select_related (1)
    # User prefetch_related when the other end of the r/lship has many (n) items or in a reverse Foreign Key Eg In Orders - orderitem_set - reverse foreing key | prefetch_related (n)
    # orderitem_set__product - this drills down to reach the product field inside OrderItem Model
    order_query_set = Order.objects.select_related("customer").prefetch_related("orderitem_set__product").order_by("-placed_at")[:5]


    # AGGREGATES
    # return count (integer) of all items in this DB having id | return minimum amount
    prod_result = Product.objects.aggregate(count = Count("id"), min_amount = Min("amount")) 


    # Filter products whose amount are within this range
    # query_set = Product.objects.filter(amount__range = (20, 30))

    # OTHER FILTER EXAMPLES:
    # query_set = Product.objects.filter(last_updated__year = 2026).filter(amount__gt = 100) # more than one filters
    # query_set = Product.objects.filter(last_updated__year = 2026)
    # query_set = Product.objects.filter(title__contains = "coffee")
    # query_set = Product.objects.filter(title__icontains = "coffee") # i here is to filter without case sensitivity
    # query_set = Product.objects.filter(title__startswith = "gr")
    # query_set = Product.objects.filter(title__endswith = "ee")
    # query_set = Product.objects.filter(inventory__lt = 10) # less than 10
    # query_set = Product.objects.filter(inventory__gt = 10) # greater than 10

    # PAGINATION & LIMITING RESULTS RETIURNED
    # query_set = Product.objects.all()[:5] # Return first five objects in this array
    # query_set = Product.objects.all()[5:10] # Return products btw index five and 15
    # query_set = Product.objects.values("id", "title", "collection__title") # This fetches the products, but brings back only those two fields. For collection, we used the double underscore to dig deeper to access it's title field
    # query_set = Product.objects.all().distinct() # Distinct removes all duplicate values from this fetch
    

    # SORTING 
    # query_set = Product.objects.order_by("title") # orderBy title in ASC
    # query_set = Product.objects.order_by("-title") # orderBy title in DESC
    # product = Product.objects.order_by("title")[0] # orderBy title and get the first object on the list.

    # APPLY LOGICAL OR in Query Using Q from Django DB api
    # query_set = Product.objects.filter(Q(inventory__lt = 10) | Q(amount__lt = 20)) # filtering for inventory less than 10 OR amount less than 20


    # QUERYING GENERIC RELATIONSHIPS & MODELS
    # object_id is the id of the particular object, this can be gotten through query parameters when users hit the endpoint, but hardcode it by passing 1.
    # We prefetch the tags so we can have access to the tag, referenced in this ForeignKey 
    content_type = ContentType.objects.get_for_model(Product)
    tag_query = TagItem.objects.select_related("tag").filter(content_type=content_type, object_id=1)

    # CREATING OBJECTS
    # new_obj = Product(
    #        title = "Iphone 18 Plus",
    # description = "Personal assitant in form of a mobile device. New and modern tech",
    # amount = 623000.00,
    # inventory = 40,
    # membership = "B",
    # collection = Collection(pk=2)   
    # )
    new_obj = Product.objects.get(pk=1)

    # UPDATING OBJECTS
    # updated_prod = Product.objects.filter(pk=2).update(title="New Name")

    # WRITING RAW SQL QUERIES (Deployed for complex filtering and querying not easily covered by Django ORM APIs)
    # Egs:
    # raw_query = Product.objects.raw("SELECT id, title FROM store_product")
    # raw_query2 = Product.objects.raw("SELECT * FROM store_product")

    return render(request, "hello.html", {"name": "Chinaza Ugwuoke", "products": list(query_set), "created": new_obj})



class UsersListView(generics.ListAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer



# class CustomTokenObtainPairView(TokenObtainPairView):
#     serializer_class = CustomTokenObtainPairSerializer


# class RegisterView(APIView):
#     # Allow anyone to access this endpoint (even unauthenticated users)
#     permission_classes = [AllowAny]
#     serializer_class = RegisterSerializer

#     def post(self, request):
#         serializer = RegisterSerializer(data=request.data)
        
#         if serializer.is_valid():
#             # Create the user database record
#             user = serializer.save()
            
#             # Instantly generate JWT tokens for the newly registered user
#             refresh = RefreshToken.for_user(user)
            
#             # Return user info alongside tokens
#             return Response({
#                 "message": "User registered successfully!",
#                 "user": {
#                     "first_name": user.first_name,
#                     "last_name": user.last_name,
#                     "email": user.email
#                 },
#                 "tokens": {
#                     "refresh": str(refresh),
#                     "access": str(refresh.access_token),
#                 }
#             }, status=status.HTTP_201_CREATED)
            
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

