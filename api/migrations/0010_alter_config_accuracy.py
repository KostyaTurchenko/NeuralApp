# Generated by Django 3.2.10 on 2022-01-14 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_alter_config_accuracy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='config',
            name='accuracy',
            field=models.CharField(default='off', max_length=100),
        ),
    ]
