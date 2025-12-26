from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [

    # register 
    path('register/',views.register_view.as_view()),
    path('token/',TokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),



    # product
    path('products/',views.get_products.as_view(),name="get_products"),
    path('products/<int:pk>/',views.product_id.as_view(),name="product_id"),

    # category
    path('categories/',views.get_categories.as_view(),name="get_categories"),


    # Cart
    path('cart/',views.get_cart.as_view(),name='get_cart'),
    path('cart/add/',views.add_to_cart.as_view()),
    path('cart/remove/',views.remove_from_cart.as_view()),
    path('cart/update/',views.update_cart_quantity),
    path('orders/create/',views.create_order.as_view()),

    # path('cart/',views.get_cart,name='get_cart'),
    # path('cart/add/',views.add_to_cart),
    # path('cart/remove/',views.remove_from_cart),
    # path('cart/updatequantity/',views.update_cart_quantity),
]
