# Generated by Django 4.1.6 on 2023-02-12 13:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gui', '0003_movielist_movie_movie_list'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='movie_list',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='gui.movielist'),
        ),
    ]
