from re import template
from django.urls import path,include
from app import views
from django.contrib.auth import views as auth_views
from .forms import LoginForm,MyPasswordChangeForm,MyPasswordResetForm,MySetPasswordForm

urlpatterns = [
    path('',views.ProductView.as_view(),name="home"),
    path('product-detail/<int:pk>',views.ProductDetailView.as_view(),name='product-detail'),
    path('cart/',views.show_cart,name='cart'),
    path('add_to_cart/',views.add_to_cart,name="add_to_cart"),
    path('removecart/',views.removecart,name="removecart"),
    path('pluscart/',views.plus_cart),
    path('minuscart/',views.minus_cart),
    path('checkout/',views.checkout,name="checkout"),
    path('done/',views.done,name="done"),
    path('orders/',views.orders,name="orders"),

    path('registration/',views.CustomerRegistrationView.as_view(),name="customerRegistration"),

    path('login/',auth_views.LoginView.as_view(template_name='app/login.html',authentication_form=LoginForm),name="login"),

    path('logout/',auth_views.LogoutView.as_view(next_page='home'),name="logout"),

    path('changepassword/',auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html',form_class=MyPasswordChangeForm,success_url='/passwordchangedone/'),name='change-password'),
    path('passwordchangedone/',auth_views.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'),name='passwordchangedone'),

    path('reset_password/',auth_views.PasswordResetView.as_view(template_name='app/password_reset.html',form_class=MyPasswordResetForm),name="reset-password"),

    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'),name="password-reset-done"),

    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html',form_class=MySetPasswordForm),name="password_reset_confirm"),

    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'),name="password_reset_complete"),

    path('profile/',views.ProfileView.as_view(),name="profile"),
    path('address/',views.address,name="address"),
    path('sign_up/',views.sign_up,name="sign_up"),
]