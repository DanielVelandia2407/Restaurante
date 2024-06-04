from django.urls import path, include
from .views import ProjectAPIView, TaskAPIView, ProjectViewSet, TaskViewSet, CommentViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='projects')
router.register(r'tasks', TaskViewSet, basename='tasks')
router.register(r'comments', CommentViewSet, basename='comments')


urlpatterns = [
    #path('projects/', ProjectAPIView.as_view()),
    #path('projects/<int:project_id>/tasks/', TaskAPIView.as_view())
]

urlpatterns += router.urls