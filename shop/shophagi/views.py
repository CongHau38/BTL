from django.contrib import contenttypes
from django.shortcuts import render
from rest_framework import viewsets, permissions, generics, parsers, status
from .models import(
    Category, Brank, Product, User, Comment, Like)
from .serializers import(
    CategorySerializer, BrankSerializer, ProductSerializer,
    ProductDetailSerializer, UserSerializer, CommentSerializer,
    AuthorizedProductDetailSerializer,)
from .paginators import ProductPaginator
from .perms import CommentOwner
from rest_framework.decorators import action
from rest_framework.views import Response
# Create your views here.


class CategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class BrankViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView):
    queryset = Brank.objects.all()
    serializer_class = BrankSerializer
    # list (GET) --> ds
    #..(POST) --> them
    #detail --> chi tiet 1
    #.. (PUT) --> cap nhat
    #.. (DELETE) --> xoa

    def filter_queryset(self, queryset):
        cate_id = self.request.query_params.get('category_id')
        if cate_id:
            queryset = queryset.filter(category_id=cate_id)
        return queryset

    @action(methods=['get'], detail=True, url_path='products')
    def products(self, request, pk):
        c = self.get_object()
        products = c.product.filter(active=True)

        kw = request.query_params.get('kw')
        if kw:
            products = products.filter(name__icontains=kw)

        return Response(ProductSerializer(products, many=True).data)


class ProductViewSet(viewsets.ViewSet, generics.RetrieveAPIView):
    queryset = Product.objects.filter(active=True)
    serializer_class = ProductDetailSerializer
    pagination_class = ProductPaginator

    def get_serializer_class(self):
        if self.request.user.is_authenticated:
            return AuthorizedProductDetailSerializer
        return self.serializer_class

    def get_permissions(self):
        if self.action in ['comments', 'like']:
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=['post'], detail=True, url_path='comments')
    def comments(self, request, pk):
        c = Comment(content=request.data['content'], product=self.get_object(), user=request.user)
        c.Save()
        return Response(CommentSerializer(c, context={'request': request}).data, status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=True, url_path='like')
    def like(self, request, pk):
        lesson = self.get_object()
        l, created = Like.objects.get_or_create(lesson=lesson, user=request.user)
        if not created:
            l.liked = not l.liked
        l.save()

        return Response(status=status.HTTP_200_OK)


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView, generics.UpdateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    parser_classes = [parsers.MultiPartParser, ]

    def get_permissions(self):
        if self.action in ['current_user', 'update', 'partial_update']:
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=['get', 'put'], detail=False, url_path='current-user')
    def current_user(self, request):
        u = request.user
        if request.method.__eq__('PUT'):
            for k, v in request.data.items():
                if k.__eq__('password'):
                    u.set_password(k)
                else:
                    setattr(u, k, v)
            u.save()
        return Response(UserSerializer(u, context={'request': request}).data)


class CommentViewSet(viewsets.ViewSet, generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = Comment.objects.filter(active=True)
    serializer_class = CommentSerializer
    permission_classes = [CommentOwner, ]
