# Generated by Django 3.1 on 2020-12-25 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('podo_app', '0005_add_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='likeproduct',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
