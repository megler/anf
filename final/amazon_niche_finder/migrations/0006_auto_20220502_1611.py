# Generated by Django 3.2 on 2022-05-02 20:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('amazon_niche_finder', '0005_auto_20220502_1405'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bestsellers',
            name='level',
        ),
        migrations.RemoveField(
            model_name='bestsellers',
            name='lft',
        ),
        migrations.RemoveField(
            model_name='bestsellers',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='bestsellers',
            name='rght',
        ),
        migrations.RemoveField(
            model_name='bestsellers',
            name='tree_id',
        ),
    ]