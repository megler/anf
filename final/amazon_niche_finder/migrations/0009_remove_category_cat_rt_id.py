# Generated by Django 3.2 on 2022-05-03 01:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('amazon_niche_finder', '0008_auto_20220502_1937'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='cat_rt_id',
        ),
    ]
