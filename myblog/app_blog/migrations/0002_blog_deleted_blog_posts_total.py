# Generated by Django 4.0.1 on 2022-01-22 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='deleted_blog_posts_total',
            field=models.PositiveIntegerField(default=0, verbose_name='Число удаленных постов'),
        ),
    ]
