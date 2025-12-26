from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework import generics
from .models import Product,Category,Cart,CartItem,Order,OrderItem
from .serializers import ProductSerializer,CategorySerializer,CartItemSerializer,CartSerializer
from .paginations import CustomPagination
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.contrib.auth.models import User
from .serializers import RegisterSerializer,UserSerializer


# Create your views here.

# PRODUCT
# get products
class get_products(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # pagination_class = CustomPagination

# product with id
class product_id(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "pk"




# CATEGORY
# get category 
class get_categories(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # pagination_class = CustomPagination



# Cart

class get_cart(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
# ADD TO CART

class add_to_cart(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get("product_id")

        if not product_id:  
            return Response(
                {"error": "product_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        product = get_object_or_404(Product, id=product_id)
        cart, _ = Cart.objects.get_or_create(user=request.user)

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product
        )

        if not created:
            item.quantity += 1
            item.save()

        return Response(
            {
                "message": "Product added to cart",
                "cart": CartSerializer(cart).data,
            },
            status=status.HTTP_200_OK
        )

# REMOVE ITEM FROM CART

class remove_from_cart(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        item_id = request.data.get("item_id")

        if not item_id:  
            return Response(
                {"error": "item_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        item = get_object_or_404(
            CartItem,
            id=item_id,
            cart__user=request.user  
        )

        item.delete()
        return Response(
            {"message": "Item removed from cart"},
            status=status.HTTP_200_OK
        )

    
# Update CART
# class update_cart_quantity(APIView):
#     def post(self,request):
#         item_id = request.data.get("item_id")
#         quantity = request.data.get("quantity")

#         if item_id is None or quantity is None:
#             return Response(
#                 {"error" : "Item ID and quantity are required"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
        
#         item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)


@api_view(["POST"])
@permission_classes([IsAuthenticated]) 
def update_cart_quantity(request):
    item_id = request.data.get("item_id")
    quantity = request.data.get("quantity")

    if item_id is None or quantity is None: 
        return Response(
            {"error": "item_id and quantity are required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user  
    )

    quantity = int(quantity)

    if quantity < 1:
        item.delete()
        return Response(
            {"message": "Item removed from cart"},
            status=status.HTTP_200_OK
        )

    item.quantity = quantity
    item.save()

    return Response(
        CartItemSerializer(item).data,
        status=status.HTTP_200_OK
    )


class create_order(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        try :
            data = request.data
            name = data.get('name')
            address = data.get('address')
            phone = data.get('phone')
            payment_method = data.get('payment_method','COD')
            

            # Validate Phone No
            if not phone.isdigit() or len(phone) < 10:
                return Response({'error': 'Invalid phone number'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Get user's cart
            cart,created = Cart.objects.get_or_create(user=request.user)
            if not cart.items.exists():
                return Response({'error' : 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

            total = sum([item.product.price * item.quantity for item in cart.items.all()])

            order = Order.objects.create(user = request.user,total_amount=total)


            # Create order Items
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )
            
            # clear the cart
            cart.items.all().delete()

            return Response({
                "message" : "Order placed Successfully",
                "order_id" : order.id,
            })
        
        except Exception as e:
            return Response({"error" : str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class register_view(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message':"User created successfully", "user" : UserSerializer(user).data},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)