# Generated by Django <your_version> on <current_date>

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0005_merge'),
    ]

    operations = [
        # Remove 'brix' field from 'DataNanas' model
        migrations.RemoveField(
            model_name='datananas',
            name='brix',
        ),
        # Remove 'brix' field from 'RiwayatKlasifikasi' model
        migrations.RemoveField(
            model_name='riwayatklasifikasi',
            name='brix',
        ),
    ]
