from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView
import authentication.views
import feed.views

auth_patterns = [path('logout/', authentication.views.logout_user, name='logout'),
                 path('signup/', authentication.views.signup_page, name='signup'),
                 path('login/', LoginView.as_view(
                    template_name='authentication/login.html',
                    redirect_authenticated_user=True),
                    name='login')]

urlpatterns = [
    path('', feed.views.feed_home_page, name='home'),
    path('auth/', include(auth_patterns)),
    path('ticket/', feed.views.create_ticket, name='create_ticket')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
