from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('product/<str:pk>/',views.ProductView,name='product'),
    path('Update-Product/<str:pk>/',views.updateProduct,name="update-product"),
    path('delete-Product/<str:pk>/',views.deleteProduct,name="delete-product"),
    path('Add-Product/',views.addProduct,name="add-product"),
    path('search-product/',views.SearchedProduct,name="search-product"),
    path('navbar/', views.navbar, name='navbar'),
    path('login-page/',views.LoginPage,name="login"),
    path('logout-page/',views.logoutUser,name="logout"),
    path('register/',views.registerPage,name="register"),
    path('cart/',views.CartView,name="cart-product"),
    path('AddtoCart/<str:pk>/',views.AddtoCart,name='add-cart'),
]
