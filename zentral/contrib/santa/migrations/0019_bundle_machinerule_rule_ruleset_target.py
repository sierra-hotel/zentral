# Generated by Django 2.2.17 on 2021-01-19 13:02

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0051_auto_20201202_1025'),
        ('santa', '0018_auto_20210114_0747'),
    ]

    operations = [
        migrations.CreateModel(
            name='RuleSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Target',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('BINARY', 'Binary'), ('BUNDLE', 'Bundle'), ('CERTIFICATE', 'Certificate')], max_length=16)),
                ('sha256', models.CharField(max_length=64)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='target',
            unique_together={('type', 'sha256')},
        ),
        migrations.CreateModel(
            name='Bundle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.TextField()),
                ('executable_rel_path', models.TextField()),
                ('bundle_id', models.TextField()),
                ('name', models.TextField()),
                ('version', models.TextField()),
                ('version_str', models.TextField()),
                ('binary_count', models.PositiveIntegerField()),
                ('uploaded_at', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('binary_targets', models.ManyToManyField(related_name='parent_bundle', to='santa.Target')),
                ('target', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='santa.Target')),
            ],
        ),
        migrations.CreateModel(
            name='Rule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('policy', models.PositiveSmallIntegerField(choices=[(1, 'Allowlist'), (2, 'Blocklist'), (3, 'Silent blocklist'), (5, 'Allowlist compiler')])),
                ('custom_msg', models.TextField(blank=True)),
                ('version', models.PositiveIntegerField(default=1)),
                ('serial_numbers', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), default=list, size=None, blank=True)),
                ('primary_users', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), default=list, size=None, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('configuration', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='santa.Configuration')),
                ('ruleset', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='santa.RuleSet')),
                ('tags', models.ManyToManyField(to='inventory.Tag', blank=True)),
                ('target', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='santa.Target')),
            ],
            options={
                'unique_together': {('configuration', 'target')},
            },
        ),
        migrations.CreateModel(
            name='MachineRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('policy', models.PositiveSmallIntegerField(choices=[(1, 'Allowlist'), (2, 'Blocklist'), (3, 'Silent blocklist'), (5, 'Allowlist compiler'), (4, 'Remove')])),
                ('version', models.PositiveIntegerField()),
                ('cursor', models.CharField(max_length=8, null=True)),
                ('enrolled_machine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='santa.EnrolledMachine')),
                ('target', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='santa.Target')),
            ],
            options={
                'unique_together': {('enrolled_machine', 'target')},
            },
        ),
    ]