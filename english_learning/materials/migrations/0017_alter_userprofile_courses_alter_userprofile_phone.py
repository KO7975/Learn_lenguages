# Generated by Django 4.1.2 on 2023-05-31 11:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0016_alter_commens_options_alter_commens_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='courses',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='materials.course'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='phone',
            field=models.CharField(blank=True, max_length=13, null=True),
        ),
    ]
