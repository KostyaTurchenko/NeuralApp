# Generated by Django 3.2.10 on 2022-01-14 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_alter_config_accuracy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='config',
            name='accuracy',
            field=models.CharField(max_length=100),
        ),
    ]