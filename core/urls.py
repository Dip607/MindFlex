from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import home, signup_view, login_view, edit_profile_view, matches
from .views import custom_logout_view
from .views import chat_view
from .views import all_users_view
from .views import profile_detail_view
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', custom_logout_view, name='logout'),
    path('users/', all_users_view, name='all-users'),
    path('chat/<int:user_id>/', chat_view, name='chat'),
    path('edit-profile/', edit_profile_view, name='edit-profile'),
    path('matches/', matches, name='matches'),
    
    path('profile/<int:user_id>/', profile_detail_view, name='profile-detail'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)