# Generated by Django 3.2.9 on 2021-12-14 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fsm_admin', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hlvien',
            name='vaitro',
            field=models.CharField(default='HLV Trưởng', max_length=20),
            preserve_default=False,
        ),
    ]