from django.urls import path

from app.views import *

urlpatterns = [
    path('', index_view, name='index'),
    path('about/', about, name='about'),
    path('blog_grid_left_sidebar/', blog_grid_left_sidebar, name='blog_grid_left_sidebar'),
    path('blog_single_left_sidebar/', blog_single_left_sidebar, name='blog_single_left_sidebar'),

    path('contact/', contact, name='contact'),
    path('shop/', shop, name='shop'),
    path('product_details/<int:product_id>/', single_view, name='single_product'),
    path('single_product_affiliate/', single_product_affiliate, name='single_product_affiliate'),
    path('single_product_variable/', single_product_variable, name='single_product_variable'),
    path('thank_you_page/', thank_you_page, name='thank_you_page'),

    path('product-wishlist-page/', product_wishlist_page, name='product-wishlist-page'),
    path('add-wishlist/<int:product_id>', add_wishlist_view, name='add-wishlist'),
    path('delete-wishlist/<int:product_id>', delete_wishlist_view, name='delete-wishlist'),

    path('my-account/', my_account, name='my_account'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    path('product-cart-page/', product_cart, name='product-cart-page'),
    path('add-cart/<int:product_id>', add_cart_view, name='add-cart'),
    path('delete-cart/<int:product_id>', delete_cart, name='delete-cart'),
    path('edit-cart/<int:product_id>', edit_cart_item_view, name='edit-cart'),

    path('checkout/', checkout_view, name='product-checkout-page'),
]