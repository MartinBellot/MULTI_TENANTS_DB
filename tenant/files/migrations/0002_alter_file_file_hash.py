# Generated by Django 4.2.20 on 2025-04-15 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file_hash',
            field=models.CharField(blank=True, help_text='Hash du fichier', max_length=1200, null=True),
        ),
    ]
