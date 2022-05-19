# Generated by Django 3.2 on 2022-05-02 17:00

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('amazon_niche_finder', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bestsellers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cat_id', models.IntegerField()),
                ('cat_name', models.CharField(default='', max_length=100)),
                ('cat_parent_id', models.IntegerField()),
                ('cat_link', models.URLField(null=True)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('best_parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='amazon_niche_finder.bestsellers')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
