# Generated by Django 5.1.3 on 2024-11-19 14:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0004_alter_clientprofilemodel_status_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Achievements',
            new_name='CounselorAchievements',
        ),
        migrations.AlterModelTable(
            name='counselorachievements',
            table='counselor_achievements',
        ),
    ]
