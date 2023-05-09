from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Category, Brank, Product, User, Comment


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class ImageSerializer(ModelSerializer):
    image = SerializerMethodField(source='image')

    def get_image(self, obj):
        if obj.image:
            request = self.context.get('request')
            return request.build_absolute_uri('/static/%s' % obj.image.name) if request else ''

class BrankSerializer(ModelSerializer):
    class Meta:
        model = Brank
        fields = ['id', 'name', 'category']

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'images', 'rating', 'price']

class ProductDetailSerializer(ProductSerializer):
    images = SerializerMethodField(source='images')

    def get_image(self, obj):
        if obj.images:
            request = self.context.get('request')
            return request.build_absolute_uri('/static/%s' % obj.images.name) if request else ''

    def create(self, validated_data):
        data = validated_data.copy()

        p = Product(**data)
        p.save()

        return p
    class Meta:
        model = ProductSerializer.Meta.model
        fields = ProductSerializer.Meta.fields + ['description', 'user']

class AuthorizedProductDetailSerializer(ProductDetailSerializer):
    like = SerializerMethodField

    def get_like(self, product):
        request = self.context.get('request')
        if request:
            return product.like_set.filter(user=request.user, like=True).exists()

    class Meta:
        model = ProductSerializer.Meta.model
        fields = ProductSerializer.Meta.fields + ['like']

class UserSerializer(ModelSerializer):
    avatar = SerializerMethodField(source='avatar')

    def get_image(self, obj):
        if obj.avatar:
            request = self.context.get('request')
            return request.build_absolute_uri('/static/%s' % obj.avatar.name) if request else ''

    def create(self, validated_data):
        data = validated_data.copy()

        u = User(**data)
        u.set_password(u.password)
        u.save()

        return u
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'password', 'email', 'avatar', 'decent_id']
        extra_kwargs = {
            'avatar': {'write_only': True},
            'password': {'write_only': True}
        }

class CommentSerializer(ModelSerializer):
    user = UserSerializer
    class Meta:
        model = Comment
        fields = ['id', 'rating', 'content', 'created_date', 'user']