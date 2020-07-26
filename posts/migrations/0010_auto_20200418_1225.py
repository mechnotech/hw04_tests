# Generated by Django 2.2.9 on 2020-04-18 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0009_auto_20200417_1132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='title',
            field=models.CharField(help_text='Название группы (не более 200 символов)', max_length=200, unique=True, verbose_name='Название группы'),
        ),
    ]
