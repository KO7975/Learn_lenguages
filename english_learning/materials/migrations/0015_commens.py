# Generated by Django 4.1.2 on 2023-03-14 08:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('materials', '0014_material_text_material_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='Commens',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(blank=True, null=True)),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('time_appdated', models.DateTimeField(auto_now=True)),
                ('is_published', models.BooleanField(default=True)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
