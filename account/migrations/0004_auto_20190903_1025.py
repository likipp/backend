# Generated by Django 2.2.1 on 2019-09-03 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20190903_0925'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='avatar/default.jpg', upload_to='avatar/%Y%m%d/'),
        ),
    ]
