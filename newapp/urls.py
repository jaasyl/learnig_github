from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
   path('', index),
   path('shop/', shopfn, name='shopfn'),  # Added name for shop view
   path('view/<int:s_id>', viewfn),
   path('category/<int:c_id>', catfn),
   path('register/', registerfn),
   path('login/', loginfn),
   path("add-to-cart/<int:product_id>/", add_to_cart, name='add-to-cart'),  # Updated to accept product_id
   path("cart/", cart_view),
   path('remove-from-cart/<int:product_id>/', remove_from_cart),
]
