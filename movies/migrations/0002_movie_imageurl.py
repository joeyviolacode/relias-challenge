# Generated by Django 3.1.1 on 2020-09-21 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='imageURL',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
