from django.urls import path
from leboauth import views
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from .views import CustomPasswordResetView, CustomPasswordResetDoneView, CustomPasswordResetCompleteView, password_reset_link_sent

urlpatterns = [
    path('signup/',views.signup,name='signup'),
    path('login/',views.handlelogin,name='handlelogin'),
    path('logout/',views.handlelogout,name='handlelogout'),
    path('activate/<uidb64>/<token>',views.ActivateAccountView.as_view(),name='activate'),
    path('password-reset/',CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset-done/', PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done.html'),
    path('password-reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset/complete/', PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('password-reset-link-sent/', password_reset_link_sent, name='password_reset_link_sent.html'),
    path('password-reset/sent/', password_reset_link_sent, name='password_reset_link_sent.html'),
    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
]