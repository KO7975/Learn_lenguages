# Generated by Django 4.1.2 on 2023-02-24 09:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0003_alter_material_material_file_userprofile'),
    ]

    operations = [
        # migrations.RemoveField(
        #     model_name='userprofile',
        #     name='courses',
        # ),
        # migrations.AddField(
        #     model_name='userprofile',
        #     name='courses',
        #     field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='materials.course'),
        # ),
    ]
