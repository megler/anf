# Generated by Django 3.2 on 2022-05-02 18:05

from django.db import migrations
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('amazon_niche_finder', '0004_auto_20220502_1359'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bestsellers',
            name='best_parent',
        ),
        migrations.AddField(
            model_name='bestsellers',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='amazon_niche_finder.bestsellers'),
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]
