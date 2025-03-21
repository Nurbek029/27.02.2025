from django.urls import path
from . import views


urlpatterns = [
    path('', views.index_view, name='index'),

    path('product/<int:product_id>/', views.product_detail_view, name='product_detail'),
    path('product/create/', views.product_create_view, name='product_create'),
    path('product/update/<int:product_id>/', views.product_update_view, name='product_update'),

    path('rating/create/<int:product_id>/', views.rating_create_view, name='rating_create'),
    path('rating-answer/create/<int:rating_id>/', views.rating_answer_create_view, name='rating_answer_create'),

    path('profile/', views.user_profile_view, name='user_profile'),
    path('payment_requests/', views.payment_request_list_view, name='payment_requests'),
    path('payment_request/<int:payment_request_id>/update/', views.payment_request_update_status,
         name='payment_request_update_status'),
    path('payments/', views.payment_list_view, name='payments'),

    path('product/<int:product_id>/payment/create/', views.product_payment_create_view,
         name='product_payment_create'),

    path('catalog/', views.product_list_view, name='catalog')
]