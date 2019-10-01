
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from users import views as user_views


admin.site.site_header = "Events Admin"
admin.site.site_title = "Events Admin Portal"
admin.site.index_title = "Welcome To Events Administration Backend"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("app.urls")),
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.display_profile, name='profile'),
    path('profile/<slug:slug>/', user_views.DisplayProfile.as_view(), name='profile-detail'),
    path('edit_profile/', user_views.profile, name='edit_profile'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('activate/<slug:uidb64>/<slug:token>)/', user_views.activate_link, name='activate'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='users/password_reset.html'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='users/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='users/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='users/password_reset_complete.html'
         ),
         name='password_reset_complete'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



