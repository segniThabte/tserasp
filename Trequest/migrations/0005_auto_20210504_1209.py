# Generated by Django 3.0.3 on 2021-05-04 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Trequest', '0004_auto_20210504_1203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='first_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='last_name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
