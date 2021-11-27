from django.contrib import admin
from django.urls import path,include
from django.contrib.auth.views import (LoginView,
                                       LogoutView,
                                       PasswordResetView,
                                       PasswordResetDoneView,
                                       PasswordResetConfirmView,
                                       PasswordResetCompleteView)
#from users import views as users_views
from users.views import register,profile
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    #path('register/', users_views.register,name='register'),
    #path('profile/', users_views.profile,name='profile'),
    path('register/', register,name='register'),
    path('profile/', profile,name='profile'),
    path('login/', LoginView.as_view(template_name='users/login.html'),name='login'),
    path('logout/', LogoutView.as_view(template_name='users/logout.html'),name='logout'),
    path('password-reset/',PasswordResetView.as_view(
             template_name='users/password_reset.html'
         ),
         name='password_reset'),
    path('password-reset/done/',
         PasswordResetDoneView.as_view(
             template_name='users/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(
             template_name='users/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         PasswordResetCompleteView.as_view(
             template_name='users/password_reset_complete.html'
         ),
         name='password_reset_complete'),
    path('', include('blog.urls')),
]

# debug setting for production purpose
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    