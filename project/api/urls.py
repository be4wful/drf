from django.urls import path
from . import views

urlpatterns = [
    path('products', views.ProductViewDef),
    path('product/<int:pk>', views.ProductChangeDeleteDef),
    path('cart', views.CartViewDef),
    path('signup', views.UserRegDef),
    path('login', views.UserLoginDef),
    path('logout', views.UserLogout.as_view()),
    path('cart/<int:pk>', views.CartAddDeleteView),
    path('order', views.OrderGetAddView),
    path('product', views.ProductAddDef),
]