import django.core.validators
from django.db import migrations, models


def scale_report_marks_to_10(apps, schema_editor):
    ProjectReport = apps.get_model("core", "ProjectReport")

    for report in ProjectReport.objects.all().iterator():
        changed = False

        if report.coordinator1_mark is not None:
            report.coordinator1_mark = round((report.coordinator1_mark / 15) * 10)
            changed = True

        if report.coordinator2_mark is not None:
            report.coordinator2_mark = round((report.coordinator2_mark / 15) * 10)
            changed = True

        if report.final_mark is not None:
            report.final_mark = round((report.final_mark / 15) * 10)
            changed = True

        if changed:
            report.save(update_fields=["coordinator1_mark", "coordinator2_mark", "final_mark"])


def reverse_scale_report_marks_to_15(apps, schema_editor):
    ProjectReport = apps.get_model("core", "ProjectReport")

    for report in ProjectReport.objects.all().iterator():
        changed = False

        if report.coordinator1_mark is not None:
            report.coordinator1_mark = round((report.coordinator1_mark / 10) * 15)
            changed = True

        if report.coordinator2_mark is not None:
            report.coordinator2_mark = round((report.coordinator2_mark / 10) * 15)
            changed = True

        if report.final_mark is not None:
            report.final_mark = round((report.final_mark / 10) * 15)
            changed = True

        if changed:
            report.save(update_fields=["coordinator1_mark", "coordinator2_mark", "final_mark"])


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0030_convert_projectreport_marks_to_15_scale"),
    ]

    operations = [
        migrations.AlterField(
            model_name="projectreport",
            name="coordinator1_mark",
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)]),
        ),
        migrations.AlterField(
            model_name="projectreport",
            name="coordinator2_mark",
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)]),
        ),
        migrations.AlterField(
            model_name="projectreport",
            name="final_mark",
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)]),
        ),
        migrations.RunPython(scale_report_marks_to_10, reverse_scale_report_marks_to_15),
    ]
