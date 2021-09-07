from django.urls import path

from bot import views

urlpatterns = [
    path('', views.TestView.as_view(), name='home'),
    path('customers-table', views.CustomerView.as_view()),
    path('item-table', views.ItemView.as_view()),
    path('credit-card', views.CreditCardCreateView.as_view(), name='create_card'),
    path('card-update', views.CreditCardUpdateView.as_view(), name='update_card'),
    path('card-delete', views.CreditCardDeleteView.as_view(), name='delete_card'),
    path('card-info', views.CreditCardReadView.as_view(), name='card_info'),
    path('signup', views.SignUpView.as_view(), name='signup'),
    path('login', views.UserLoginView.as_view(), name='login'),
    path('logout', views.UserLogoutView.as_view(), name='logout'),
    path('buy/<int:pk>', views.BuyItemView.as_view(), name='buy_item'),
    path('order-history', views.OrderHistoryView.as_view(), name='order_history'),
    path('rating/<int:pk>', views.ItemRatingView.as_view(), name='item_rating'),
]
