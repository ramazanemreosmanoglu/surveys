# Generated by Django 2.2.12 on 2020-07-16 10:57

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_auto_20200715_1932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='voters',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
