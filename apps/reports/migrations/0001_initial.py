import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("centres", "0002_diagnostictest_category"),
    ]

    operations = [
        migrations.CreateModel(
            name="Report",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("findings", models.TextField()),
                ("report_date", models.DateField()),
                ("status", models.CharField(choices=[("DRAFT", "Draft"), ("FINAL", "Final")], default="FINAL", max_length=10)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("patient", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="reports", to=settings.AUTH_USER_MODEL)),
                ("test", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="reports", to="centres.diagnostictest")),
            ],
            options={"ordering": ["-report_date", "-id"]},
        ),
    ]
