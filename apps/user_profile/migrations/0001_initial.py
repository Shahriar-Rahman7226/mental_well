# Generated by Django 5.0.6 on 2024-10-20 17:37

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SpecializationModel',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, help_text="Unique id for a model's object", primary_key=True, serialize=False, unique=True)),
                ('is_active', models.BooleanField(db_index=True, default=True, help_text="Is the model's object active")),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, help_text="Creation date of the model's object")),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, help_text="Updating date of the model's object")),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'specialization',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ClientProfileModel',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, help_text="Unique id for a model's object", primary_key=True, serialize=False, unique=True)),
                ('is_active', models.BooleanField(db_index=True, default=True, help_text="Is the model's object active")),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, help_text="Creation date of the model's object")),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, help_text="Updating date of the model's object")),
                ('description', models.TextField(blank=True, null=True)),
                ('goals', models.TextField(blank=True, null=True)),
                ('emergency_contact', models.CharField(blank=True, max_length=20, null=True, unique=True)),
                ('status', models.CharField(blank=True, choices=[('PENDING', 'pending'), ('APPROVED', 'approved')], default='PENDING', max_length=100, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='client_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'client_profile',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='CounselorProfileModel',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, help_text="Unique id for a model's object", primary_key=True, serialize=False, unique=True)),
                ('is_active', models.BooleanField(db_index=True, default=True, help_text="Is the model's object active")),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, help_text="Creation date of the model's object")),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, help_text="Updating date of the model's object")),
                ('certificate', models.FileField(blank=True, null=True, upload_to='')),
                ('identity_document', models.FileField(blank=True, null=True, upload_to='')),
                ('description', models.TextField(blank=True, null=True)),
                ('license_number', models.CharField(blank=True, max_length=100, null=True)),
                ('website', models.URLField(blank=True, null=True)),
                ('linked_in', models.URLField(blank=True, null=True)),
                ('status', models.CharField(blank=True, choices=[('PENDING', 'pending'), ('APPROVED', 'approved')], default='PENDING', max_length=100, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='counselor_profile', to=settings.AUTH_USER_MODEL)),
                ('specializations', models.ManyToManyField(related_name='counselor_specialization', to='user_profile.specializationmodel')),
            ],
            options={
                'db_table': 'counselor_profile',
                'ordering': ['-created_at'],
            },
        ),
    ]
