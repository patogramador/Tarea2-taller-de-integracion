# Generated by Django 3.2 on 2021-05-03 00:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.CharField(max_length=22, primary_key=True, serialize=False)),
                ('artist_id', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('genre', models.CharField(max_length=100)),
                ('artist', models.CharField(max_length=200)),
                ('tracks', models.CharField(max_length=200)),
                ('self', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Artistas',
            fields=[
                ('id', models.CharField(max_length=22, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('age', models.IntegerField()),
                ('albums', models.CharField(max_length=200)),
                ('tracks', models.CharField(max_length=200)),
                ('self', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Cancion',
            fields=[
                ('id', models.CharField(max_length=22, primary_key=True, serialize=False)),
                ('album_id', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('duration', models.FloatField()),
                ('times_played', models.IntegerField()),
                ('artist', models.CharField(max_length=200)),
                ('album', models.CharField(max_length=200)),
                ('self', models.CharField(max_length=200)),
                ('padre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='musica.album')),
            ],
        ),
        migrations.AddField(
            model_name='album',
            name='padre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='musica.artistas'),
        ),
    ]