# Generated by Django 3.1.1 on 2020-09-20 20:20

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('release_date', models.CharField(blank=True, max_length=15, null=True)),
                ('description', models.TextField()),
                ('tmdb_id', models.IntegerField()),
                ('favorited_by', models.ManyToManyField(blank=True, related_name='favorites', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
