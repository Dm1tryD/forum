# Generated by Django 3.1.1 on 2020-09-30 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app_m', '0010_auto_20200930_2127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='comment_text',
            field=models.TextField(),
        ),
    ]
