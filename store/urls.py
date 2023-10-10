
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name = 'home'),
    path('store/', views.store,name='store'),
    path('cart/', views.cart,name='cart'),
    path('checkout/', views.checkout,name='checkout'),
    path('update_item/', views.updateItem,name='update_item'),
    path('process_order/', views.processOrder,name='process_order'),
    path('loginaccount/',views.loginaccount, name = 'loginaccount'),
    path('logout/', views.logoutaccount,name='logoutaccount'),
    path('signupaccount/', views.signupaccount,name='signupaccount'),
    path('product_details/<str:productName>', views.productDetails,name='productDetails'),
    path('contact_us/', views.contactUs,name='contactUs'),


]