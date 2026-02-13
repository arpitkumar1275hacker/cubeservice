from django.urls import path
from . import views
from .views import CompanyDashboardAPI

app_name = "company"

urlpatterns = [
    path('compdashboard/', views.compdashboard, name='compdashboard'),  # /touristadminapp/ → index view
    path('homeservice/', views.homeservice, name='homeservice'),
    path("delete-homeservice/<int:id>/", views.delete_homeservice, name="delete_homeservice"),
    path('popularbooking/', views.popularbooking, name='popularbooking'),
    path("delete_popularbooking/<int:id>/",views.delete_popularbooking,name="delete_popularbooking"),
    path("update-popularbooking/<int:id>/",views.update_popularbooking,name="update_popularbooking"),
    path('kitchen/', views.kitchen, name='kitchen'),
    path("update_kitchen/<int:id>/",views.update_kitchen,name="update_kitchen"),
    path("delete_kitchen/<int:id>/",views.delete_kitchen,name="delete_kitchen"),
    path('sessionalbooking/', views.sessionalbooking, name='sessionalbooking'),
    path("update_sessionalbooking/<int:id>/", views.update_sessionalbooking, name="update_sessionalbooking"),
    path("delete_sessionalbooking/<int:id>/",views.delete_sessionalbooking,name="delete_sessionalbooking"),
    path("logout_admin/", views.logout_admin, name="logout_admin"),
    path("ac_service/", views.ac_service, name="ac_service"),
    path("geyser_service/", views.geyser_service, name="geyser_service"),
    path("geyser_service/update/<int:id>/", views.update_geyser_service, name="update_geyser_service"),
    path("geyser_service/delete/<int:id>/", views.delete_geyser_service, name="delete_geyser_service"),
    path("washing_service/", views.washing_service, name="washing_service"),
    path("washing_service/update/<int:id>/", views.update_washing_service, name="update_washing_service"),
    path("washing_service/delete/<int:id>/", views.delete_washing_service, name="delete_washing_service"),
    path("waterpurifier_service/", views.waterpurifier_service, name="waterpurifier_service"),
    path("waterpurifier_service/update/<int:id>/", views.update_waterpurifier_service, name="update_waterpurifier_service"),
    path("waterpurifier_service/delete/<int:id>/", views.delete_waterpurifier_service, name="delete_waterpurifier_service"),
    path("watercooler_service/", views.watercooler_service, name="watercooler_service"),
    path("watercooler_service/update/<int:id>/", views.update_watercooler_service, name="update_watercooler_service"),
    path("watercooler_service/delete/<int:id>/", views.delete_watercooler_service, name="delete_watercooler_service"),
    path("fridge_service/", views.fridge_service, name="fridge_service"),
    path("fridge_service/update/<int:id>/", views.update_fridge_service, name="update_fridge_service"),
    path("fridge_service/delete/<int:id>/", views.delete_fridge_service, name="delete_fridge_service"),
    path("ac_service/update/<int:id>/", views.ac_service, name="update_ac_service"),
    path("ac_service/delete/<int:id>/", views.delete_ac_service, name="delete_ac_service"),
    path("fan_service/", views.fan_service, name="fan_service"),
    path("fan_service/update/<int:id>/", views.update_fan_service, name="update_fan_service"),
    path("fan_service/delete/<int:id>/", views.delete_fan_service, name="delete_fan_service"),
    path("press-service/", views.press_service, name="press_service"),
    path("press-service/update/<int:id>/", views.update_press_service, name="update_press_service"),
    path("press-service/delete/<int:id>/", views.delete_press_service, name="delete_press_service"),
    path("oven_service/", views.oven_service, name="oven_service"),
    path("oven_service/update/<int:id>/", views.update_oven_service, name="update_oven_service"),
    path("oven_service/delete/<int:id>/", views.delete_oven_service, name="delete_oven_service"),
    path("tv_service/", views.tv_service, name="tv_service"),
    path("tv_service/update/<int:id>/", views.update_tv_service, name="update_tv_service"),
    path("tv_service/delete/<int:id>/", views.delete_tv_service, name="delete_tv_service"),
    path("laptop-service/", views.laptop_service, name="laptop_service"),
    path("laptop-service/<int:id>/", views.laptop_service, name="update_laptop_service"),
    path("laptop-service/delete/<int:id>/", views.delete_laptop_service, name="delete_laptop_service"),
    path("inverter/", views.inverter_service, name="inverter_service"),
    path("inverter/<int:id>/", views.inverter_service, name="update_inverter_service"),
    path("inverter/delete/<int:id>/", views.delete_inverter_service, name="delete_inverter_service"),
    path("chimney/", views.chimney_service, name="chimney_service"),
    path("chimney/update/<int:id>/", views.chimney_service, name="update_chimney_service"),
    path("chimney/delete/<int:id>/", views.delete_chimney_service, name="delete_chimney_service"),
    path("review/", views.review, name="review"),
    path("reviews/delete/<int:feedback_id>/", views.delete_feedback, name="delete_feedback"),
    path('cancelorder/', views.cancelorder, name='cancelorder'),
    path("company_orders/", views.company_orders, name="company_orders"),
    path('see_all_product/', views.see_all_product, name='see_all_product'),
    path("update_see_all_productt/<int:id>/", views.update_see_all_product, name="update_see_all_product"),
    path("delete_see_all_product/<int:id>/", views.delete_see_all_product, name="delete_see_all_product"),
    path('userprofile', views.userprofile, name='userprofile'),
    path('add_slider', views.add_slider, name='add_slider'),
    path('delete-slider/<int:id>/', views.delete_slider, name='delete_slider'),
    path('register_servicecenter/', views.register_servicecenter, name='register_servicecenter'),
    path('add_advertisement/', views.add_advertisement, name='add_advertisement'),
    path('add_advertisement_1/', views.add_advertisement_1, name='add_advertisement_1'),
    path('advertisement/update/<int:ad_id>/',views.update_advertisement,name='update_advertisement'),
    path('servicecenter_list', views.servicecenter_list, name='servicecenter_list'),
    path('delete_servicecenter/delete/<int:id>/', views.delete_servicecenter, name='delete_servicecenter'),
    path('update_servicecenter/update/<int:id>/', views.update_servicecenter, name='update_servicecenter'),
    path("delete_company_order/delete/<int:order_id>/",views.delete_company_order,name="delete_company_order"),
    path("manage_policy/", views.manage_policy, name="manage_policy"),
    path("dashboard/", CompanyDashboardAPI.as_view()),
    

    























]
