# Generated by Django 2.2.1 on 2019-09-03 01:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='static/avatar/default.jpg', upload_to='avatar/<django.db.models.fields.CharField>/%Y%m%d/'),
        ),
    ]