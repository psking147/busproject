# Generated by Django 3.1.3 on 2021-05-18 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sbclc', '0005_remove_line_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='line',
            name='stop',
            field=models.PositiveIntegerField(),
        ),
    ]
