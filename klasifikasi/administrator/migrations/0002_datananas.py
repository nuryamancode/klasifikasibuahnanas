# Generated by Django 5.1.3 on 2024-12-06 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataNanas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sample', models.IntegerField()),
                ('red', models.IntegerField()),
                ('green', models.IntegerField()),
                ('blue', models.IntegerField()),
                ('brix', models.FloatField()),
                ('label', models.CharField(max_length=1)),
            ],
        ),
    ]
