from . import views
from django.urls import path

# Setting the URLs for our different webpages (URL, action of URl, URL name)
urlpatterns = [
    path('', views.index, name='StoreHome'),
    path('search/', views.search, name='StoreSearch'),
    path('cart/', views.cart, name='StoreCart'),
    path('account/', views.account, name='StoreAccount'),
    path('checkout/', views.checkout, name='StoreCheckout'),
    path('tracker/', views.tracker, name='StoreTracker'),
    path('logout/', views.logout_user, name='logout'),

    # <dataStructure:variable> Used to send function parameter
    path('product/<int:id>', views.product_view, name='ProductView'),
]
