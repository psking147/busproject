# Generated by Django 3.1.3 on 2021-05-28 01:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sbclc', '0008_line_stop_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='stop',
            name='pair',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]
