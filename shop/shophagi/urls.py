from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('category', views.CategoryViewSet)
router.register('brank', views.BrankViewSet)
router.register('product', views.ProductViewSet)
router.register('user', views.UserViewSet)
router.register('comment', views.CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]