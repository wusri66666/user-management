# Generated by Django 2.1 on 2020-07-16 03:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0007_remove_firstmenupermission_menu_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='firstmenupermission',
            name='menu_name',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='一级菜单名'),
        ),
    ]