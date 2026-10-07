from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("centres", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="diagnostictest",
            name="category",
            field=models.CharField(
                choices=[
                    ("RADIOLOGY", "Radiology"),
                    ("PATHOLOGY", "Pathology"),
                    ("NUCLEAR", "Nuclear Medicine"),
                ],
                default="PATHOLOGY",
                max_length=20,
            ),
        ),
    ]
