# Generated by Django 5.1.2 on 2024-11-08 06:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pnr", "0004_alter_passengerdetail_pnr_details"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pnrdetail",
            name="boarding_point",
            field=models.CharField(
                blank=True, max_length=8, null=True, verbose_name="boarding point"
            ),
        ),
    ]
