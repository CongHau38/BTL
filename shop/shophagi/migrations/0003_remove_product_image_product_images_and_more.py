# Generated by Django 4.2 on 2023-05-07 05:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shophagi', '0002_remove_product_image_product_images_product_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='decent',
            field=models.ForeignKey(default='3', on_delete=django.db.models.deletion.CASCADE, to='shophagi.decentralization'),
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('liked', models.BooleanField(default=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shophagi.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('product', 'user')},
            },
        ),
    ]
