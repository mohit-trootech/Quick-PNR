# Generated by Django 5.1.2 on 2024-11-08 06:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("quickpnr", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="emailtemplate",
            name="email_type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("verify_email", "Verify Email"),
                    ("registered", "Registered Successfully"),
                    ("pnr_details", "PNR Details"),
                ],
                max_length=50,
                null=True,
            ),
        ),
    ]
