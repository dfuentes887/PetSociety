# Generated by Django 3.1.2 on 2021-07-24 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20210722_1912'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='slug',
            field=models.SlugField(default='producto'),
            preserve_default=False,
        ),
    ]