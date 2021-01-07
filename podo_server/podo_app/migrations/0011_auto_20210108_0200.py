# Generated by Django 3.1 on 2021-01-07 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('podo_app', '0010_auto_20210107_2216'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatroom',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='status',
            field=models.PositiveIntegerField(default=2),
        ),
    ]
