# Generated by Django 5.1.3 on 2025-01-20 23:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0007_alter_riwayatklasifikasi_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datananas',
            name='gambar',
            field=models.ImageField(blank=True, null=True, upload_to='data_nanas2/'),
        ),
    ]
