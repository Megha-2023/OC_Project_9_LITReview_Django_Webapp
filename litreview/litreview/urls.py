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
                 path('ticket/<str:post_review>/', blog.views.create_ticket,
                      name='create_ticket'),
                 path('post_review/<int:tid>', blog.views.post_review_to_ticket,
                      name='post_review_to_ticket'),
                 path('follow_users/', blog.views.follow_users, name='follow_users'),
                 path('my_posts/', blog.views.own_posts, name='own_posts'),
                 path('my_posts/edit_/<str:type_of_model>/<int:tid>/', blog.views.edit_,
                      name='edit_'),
                 path('my_posts/ask_delete/<str:type_of_model>/<int:tid>/',
                      blog.views.ask_delete_confirm,
                      name='delete_confirm'),
                 path('my_posts/delete_/<str:type_of_model>/<int:tid>/', blog.views.delete_,
                      name='delete_'),
                 path('unfollow_user/<str:user_name>/', blog.views.unfollow_user,
                      name='unfollow_user')]


urlpatterns = [
    path('', blog.views.home_page, name='home'),
    path('auth/', include(auth_patterns)),
    path('blog/', include(blog_patterns))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
