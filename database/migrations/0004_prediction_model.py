# Generated by Django 2.2.16 on 2021-04-10 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0003_fixture_model_match_no'),
    ]

    operations = [
        migrations.CreateModel(
            name='prediction_model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.TextField(default='n/a')),
                ('winner', models.TextField(default='n/a')),
                ('date_time', models.TextField(default='123')),
            ],
        ),
    ]
