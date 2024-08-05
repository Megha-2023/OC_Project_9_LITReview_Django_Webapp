from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView
import authentication.views
import blog.views

auth_patterns = [path('logout/', authentication.views.logout_user, name='logout'),
                 path('signup/', authentication.views.signup_page, name='signup'),
                 path('login/', LoginView.as_view(
                    template_name='authentication/login.html',
                    redirect_authenticated_user=True),
                    name='login')]

blog_patterns = [path('ticket/', blog.views.create_ticket, name='create_ticket'),
                 path('review/', blog.views.create_review, name='create_review')]


urlpatterns = [
    path('', blog.views.home_page, name='home'),
    path('auth/', include(auth_patterns)),
    path('blog/', include(blog_patterns))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
