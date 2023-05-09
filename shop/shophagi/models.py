from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField


#makemigrations
#migrate

#Phân quyền người dùng
class Decentralization(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name

# vai trò người bán
class Roles(models.Model):
    name = models.CharField(max_length=50, unique=True)
    decent = models.ForeignKey(Decentralization, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

#người dùng
class User(AbstractUser):
    avatar = models.ImageField(upload_to='users/%Y/%m/', null=True)
    decent = models.ForeignKey(Decentralization, on_delete=models.CASCADE, default="3")

#dùng chung
class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True


#Danh mục sản phẩm
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

#Danh mục chi tiết
class Brank(models.Model):
    name = models.CharField(max_length=80, unique=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="brank")

    def __str__(self):
        return self.name

#Sản phẩm
class Product(BaseModel):
    name = models.CharField(max_length=100)
    rating = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=0)
    quantity = models.IntegerField()
    description = models.TextField(null=True, blank=True)
    images = models.ImageField(upload_to='product/%Y/%m/', null=True)
    brank = models.ForeignKey(Brank, on_delete=models.RESTRICT, related_name="product")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="user")

    def __str__(self):
        return self.name

class ActionBase(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True

#bình luận
class Comment(ActionBase):
    content = models.CharField(max_length=255)
    rating = models.IntegerField()
    def __str__(self):
        return self.content

#phản hồi bình luận
class FeedbackComment(ActionBase):
    content = models.CharField(max_length=255)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    def __str__(self):
        return self.content

# thích
class Like(ActionBase):
    liked = models.BooleanField(default=True)
    class Meta:
        unique_together = ('product', 'user')

#Hóa đơn
class Bill(BaseModel):
    gross = models.IntegerField()
    grossbill = models.DecimalField(max_digits=65, decimal_places=0)
    payments = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.RESTRICT)

#Chi tiết hóa đơn
class Invoicedetails(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.RESTRICT)
    product = models.ForeignKey(Product, on_delete=models.RESTRICT)
    price_product = models.DecimalField(max_digits=10, decimal_places=0)
    quantity_product = models.IntegerField()
