from django.urls import path

from . import views

urlpatterns = [
    path("register", views.register, name="register"),
    path("login", views.login, name="login"),
    path("get-inventory", views.get_inventory_details, name="get-inventory"),
    path("save-inventory", views.save_inventory_details, name="save-inventory"),
    # path("verify-token", views.verify_token, name="verify-token"),
    path("",views.hello_world, name="index"),
]