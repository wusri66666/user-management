# Generated by Django 2.1 on 2020-07-13 07:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0003_auto_20200713_0714'),
    ]

    operations = [
        migrations.AddField(
            model_name='menupermission',
            name='role',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='role_menu', to='system.Role', verbose_name='所属角色id'),
            preserve_default=False,
        ),
    ]
