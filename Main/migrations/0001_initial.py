# Generated by Django 3.2 on 2022-07-14 23:31

import autoslug.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('description', models.TextField(verbose_name='Description')),
                ('slug', autoslug.fields.AutoSlugField(always_update=True, editable=False, max_length=100, populate_from='__str__', unique=True, verbose_name='Slug')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CPE',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('reference', models.TextField(unique=True, verbose_name='Reference')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Extension',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Vulnerability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('description', models.TextField(verbose_name='Description')),
                ('score', models.FloatField(verbose_name='Score')),
                ('severity', models.CharField(max_length=100, verbose_name='Severity')),
                ('link', models.URLField(verbose_name='Link')),
                ('slug', autoslug.fields.AutoSlugField(always_update=True, editable=False, max_length=100, populate_from='__str__', unique=True, verbose_name='Slug')),
                ('cpe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='Main.cpe', verbose_name='CPE')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Software',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('description', models.TextField(verbose_name='Description')),
                ('version', models.CharField(max_length=100, verbose_name='Version')),
                ('slug', autoslug.fields.AutoSlugField(always_update=True, editable=False, max_length=100, populate_from='__str__', unique=True, verbose_name='Slug')),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='Main.asset', verbose_name='Asset')),
                ('cpe', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Main.cpe', verbose_name='CPE')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('description', models.TextField(verbose_name='Description')),
                ('slug', autoslug.fields.AutoSlugField(always_update=True, editable=False, max_length=100, populate_from='__str__', unique=True, verbose_name='Slug')),
                ('assets', models.ManyToManyField(blank=True, related_name='_Main_group_assets_+', to='Main.Asset', verbose_name='Assets')),
                ('extension', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='Main.extension', verbose_name='Extension')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='extension',
            name='groups',
            field=models.ManyToManyField(blank=True, related_name='_Main_extension_groups_+', to='Main.Group', verbose_name='Group(s)'),
        ),
        migrations.AddField(
            model_name='extension',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cpe',
            name='vulnerabilities',
            field=models.ManyToManyField(blank=True, related_name='_Main_cpe_vulnerabilities_+', to='Main.Vulnerability', verbose_name='Vulnerabilities'),
        ),
        migrations.AddField(
            model_name='asset',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='Main.group', verbose_name='Group'),
        ),
        migrations.AddField(
            model_name='asset',
            name='softwares',
            field=models.ManyToManyField(blank=True, related_name='_Main_asset_softwares_+', to='Main.Software', verbose_name='Softwares'),
        ),
    ]
