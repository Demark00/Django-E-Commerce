from django.urls import path
from app import views
from django.contrib.auth import views as auth_views
from .forms import LoginForm, MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm

urlpatterns = [
    path('', views.ProductView.as_view(), name="home"),
    path('chat/', views.ProductView.as_view(), name="home"),
    path('product-detail/<int:id>/', views.product_detail, name='product-detail'),
    path('search-products/', views.search, name="search"),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('remove/<int:id>/', views.remove_cart_item,
         name='remove_cart_item'),

    path('cart/', views.show_cart, name="showcart"),
    path('pluscart/', views.plus_cart),
    path('minuscart/', views.minus_cart),
    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('mobile/', views.mobile, name='mobile'),
    path('mobile/<slug:data>', views.mobile, name='mobiledata'),
    path('laptop/', views.laptop, name='laptop'),
    path('laptop/<slug:data>', views.laptop, name='laptopdata'),
    path('topwear/', views.topwear, name="topwear"),
    path('topwear/<slug:data>', views.topwear, name="topweardata"),
    path('bottomwear/', views.bottomwear, name="bottomwear"),
    path('bottomwear/<slug:data>', views.bottomwear, name="bottomweardata"),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html',
         authentication_form=LoginForm), name="login"),

    path('logout/', auth_views.LogoutView.as_view(next_page="login"), name="logout"),
    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name="app/changepassword.html",
         form_class=MyPasswordChangeForm), name="changepassword"),
    path('passwordchangedone/', auth_views.PasswordChangeDoneView.as_view(
        template_name="app/passwordchangedone.html"), name="password_change_done"),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='app/password_reset.html',
         form_class=MyPasswordResetForm), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='app/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(
        template_name='app/password_reset_confirm.html', form_class=MySetPasswordForm), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='app/password_reset_complete.html'), name='password_reset_complete'),
    path('registration/', views.customerregistration,
         name='customerregistration'),
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.payment_done, name="paymentdone"),
]
