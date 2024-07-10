from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView
import authentication.views
import feed.views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', LoginView.as_view(
        template_name='authentication/login.html',
        redirect_authenticated_user=True),
        name='login'),
    path('logout/', authentication.views.logout_user, name='logout'),
    path('home/', feed.views.feed_home_page, name='home'),
]
