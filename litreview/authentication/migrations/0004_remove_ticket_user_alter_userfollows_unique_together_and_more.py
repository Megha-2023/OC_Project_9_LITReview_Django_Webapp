# Generated by Django 5.0.6 on 2024-07-30 13:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_ticket_review_userfollows'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='user',
        ),
        migrations.AlterUniqueTogether(
            name='userfollows',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='userfollows',
            name='followed_user',
        ),
        migrations.RemoveField(
            model_name='userfollows',
            name='user',
        ),
        migrations.DeleteModel(
            name='Review',
        ),
        migrations.DeleteModel(
            name='Ticket',
        ),
        migrations.DeleteModel(
            name='UserFollows',
        ),
    ]
