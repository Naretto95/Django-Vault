# Generated by Django 3.2 on 2022-06-04 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0003_auto_20220604_2113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cpe',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='Name'),
        ),
    ]