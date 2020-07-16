# Generated by Django 2.2.12 on 2020-07-15 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VisitorIPAddressModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.GenericIPAddressField(verbose_name='IP Adresi')),
            ],
        ),
        migrations.AlterModelOptions(
            name='alert',
            options={'verbose_name': 'Uyarı', 'verbose_name_plural': 'Uyarılar'},
        ),
        migrations.AlterModelOptions(
            name='choice',
            options={'verbose_name': 'Seçenekler', 'verbose_name_plural': 'Seçenekler'},
        ),
        migrations.AlterModelOptions(
            name='poll',
            options={'ordering': ['-date'], 'verbose_name': 'Anket', 'verbose_name_plural': 'Anketler'},
        ),
        migrations.AddField(
            model_name='choice',
            name='visitor_voters',
            field=models.ManyToManyField(blank=True, to='polls.VisitorIPAddressModel'),
        ),
    ]
