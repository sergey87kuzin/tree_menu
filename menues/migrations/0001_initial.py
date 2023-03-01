# Generated by Django 4.1.7 on 2023-03-01 08:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('slug', models.SlugField(primary_key=True, serialize=False, unique=True, verbose_name='URL')),
                ('name', models.CharField(max_length=50, verbose_name='название')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='menues.menu', verbose_name='родитель')),
            ],
            options={
                'verbose_name': 'Пункт меню',
                'verbose_name_plural': 'Пункты меню',
            },
        ),
    ]
