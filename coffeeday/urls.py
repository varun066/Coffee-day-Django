from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),

    path("register/",views.register_view,name="register"),
    path("login/",views.login_view,name="login"),
    path("logout/",views.logout_view,name="logout"),

    path('create_superuser/', views.create_superuser_view, name='create_superuser'),
    path("login_superuser/",views.login_superuser_view,name="login_superuser"),
    path("logout_superuser/",views.logout_superuser_view,name="logout_superuser"),

    path("home/",views.home_view,name="home"),
    path("about_us/",views.about_us_view,name="about_us"),
    # path('exploreitems/',views.exploreitems_view,name="exploreitems"),
    path("items/",views.item_list_view,name="item_list"),
    path("items/<int:id>/",views.item_detail_view,name="item_detail"),
    path("menus/",views.menu_list_view,name="menu_list"),
    path("menus/<int:menu_id>",views.menu_detail_view,name="menu_detail"),
    path('addmenu/',views.add_menu_view,name="add_menu"),

    path('cart/',views.cart_view,name="cart"),
    path('cart/increase/<int:id>/', views.increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:id>/', views.decrease_quantity, name='decrease_quantity'),
    path('remove_from_cart/<int:id>/', views.remove_from_cart, name='remove_from_cart'),
    path('add_to_cart/<int:item_id>/', views.add_to_cart_view, name='add_to_cart'),
    path('cart/confirm_the_order/',views.confirm_the_order_view,name="confirm_the_order"),
    path('cart/order_confirmation/', views.order_confirmation, name='order_confirmation'),
    path('cart/order_success/', views.order_success, name='order_success'),

    path('past_orders/', views.past_orders, name='past_orders'), 

    path('dashboard/', views.dashboard_view, name='dashboard'),  

    path('dashboard/item_list/',views.dashboard_item_list_view,name="dashboard_item_list"),
    path('item_list/add/',views.add_item_view,name="add_item"),
    path('item_list/edit/<int:id>/', views.edit_item_view, name='edit_item'),
    path('item_list/delete/<int:id>/', views.delete_item_view, name='delete_item'),

    path('dashboard/menu_list/', views.dashboard_menu_list_view, name='dashboard_menu_list'),
    path('menu_list/add/', views.add_menu_view, name='add_menu'),
    path('menu_list/edit/<int:id>/', views.edit_menu_view, name='edit_menu'),
    path('menu_list/delete/<int:id>/', views.delete_menu_view, name='delete_menu'),

    path('dashboard/users/', views.user_list, name='user_list'),
    path('users/<int:user_id>/orders/', views.user_orders, name='user_orders'),
    
    path('ask_question/', views.ask_question, name='ask_question'),
    path('answer_questions/', views.answer_questions, name='answer_questions'),
    path('answer_question/<int:pk>/', views.answer_question, name='answer_question'),
    path('qa/', views.que_and_ans, name='qa'),

]



urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)