# Generated by Django 2.2.6 on 2019-10-28 12:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Başlık')),
                ('url', models.CharField(help_text="Başında / olmadan URL'i yazın.", max_length=200, verbose_name='URL')),
                ('text', models.CharField(max_length=500, verbose_name='Metin')),
                ('is_active', models.BooleanField(default=True, verbose_name='Aktif')),
            ],
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=200, verbose_name='Metin')),
                ('votes', models.PositiveIntegerField(default=0)),
                ('voters', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Seçenekler',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=200, verbose_name='Yorum')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Yorumlar',
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True, verbose_name='Başlık')),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Tarih')),
                ('explanation', models.TextField(blank=True, null=True, verbose_name='Açıklama')),
                ('slug', models.SlugField(editable=False, max_length=130, unique=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('choices', models.ManyToManyField(to='polls.Choice', verbose_name='Seçenekler')),
                ('comments', models.ManyToManyField(blank=True, to='polls.Comment', verbose_name='Yorumlar')),
            ],
            options={
                'verbose_name': 'Anket',
                'ordering': ['-date'],
            },
        ),
    ]
