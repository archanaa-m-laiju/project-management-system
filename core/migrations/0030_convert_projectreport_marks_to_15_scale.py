from django.db import migrations


def scale_report_marks_to_15(apps, schema_editor):
    ProjectReport = apps.get_model("core", "ProjectReport")

    for report in ProjectReport.objects.all().iterator():
        changed = False

        # Convert legacy 0-10 scale records into 0-15 scale.
        # Safety guard: if any stored mark is already > 10, skip conversion for that report.
        current_values = [
            report.coordinator1_mark,
            report.coordinator2_mark,
            report.final_mark,
        ]
        non_null_values = [value for value in current_values if value is not None]
        if non_null_values and any(value > 10 for value in non_null_values):
            continue

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


def reverse_scale_report_marks_to_10(apps, schema_editor):
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


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0029_studentevaluation_final_guide_fields"),
    ]

    operations = [
        migrations.RunPython(scale_report_marks_to_15, reverse_scale_report_marks_to_10),
    ]
