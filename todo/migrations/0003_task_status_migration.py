from django.db import migrations, models


def migrate_complete_to_status(apps, schema_editor):
    Task = apps.get_model('todo', 'Task')
    for task in Task.objects.all():
        if task.complete:
            task.status = 'done'
        else:
            task.status = 'todo'
        task.save()


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0002_profile'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={},
        ),
        migrations.AddField(
            model_name='task',
            name='status',
            field=models.CharField(
                choices=[('todo', 'À faire'), ('in_progress', 'En cours'), ('done', 'Terminé')],
                default='todo',
                max_length=20,
            ),
        ),
        migrations.RunPython(migrate_complete_to_status, reverse_code=migrations.RunPython.noop),
        migrations.RemoveField(
            model_name='task',
            name='complete',
        ),
    ]
