# Generated by Django 4.0.1 on 2022-02-15 10:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shops', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shop',
            options={'ordering': ['-name'], 'verbose_name': 'shop', 'verbose_name_plural': 'shops list'},
        ),
    ]
