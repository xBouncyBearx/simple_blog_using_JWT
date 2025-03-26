from django.contrib import admin
from django.urls import path
from users.views import RegisterView, CustomTokenObtainPairView, CustomTokenRefreshView
from blog.views import home_view, blog_view, PostListCreateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('blog/', blog_view, name='blog'),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('api/posts/', PostListCreateView.as_view(), name='post-list-create'),
]
