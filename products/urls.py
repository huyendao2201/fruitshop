from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    # Product listing
    path('', views.ProductListView.as_view(), name='product_list'),
    path('category/<slug:slug>/', views.ProductListView.as_view(), name='products_by_category'),
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    
    # Product details
    path('product/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    
    # Reviews
    path('product/<slug:slug>/add-review/', views.AddReviewView.as_view(), name='add_review'),
    
    # Shop Reviews
    path('add-shop-review/', views.AddShopReviewView.as_view(), name='add_shop_review'),
    
    # Wishlist
    path('product/<slug:slug>/toggle-wishlist/', views.ToggleWishlistView.as_view(), name='toggle_wishlist'),
    path('wishlist/', views.WishlistView.as_view(), name='wishlist'),
    
    # Newsletter
    path('newsletter/subscribe/', views.NewsletterSubscribeView.as_view(), name='newsletter_subscribe'),
]