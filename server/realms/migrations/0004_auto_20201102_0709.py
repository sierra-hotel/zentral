# Generated by Django 2.2.15 on 2020-11-02 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realms', '0003_auto_20200305_2104'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='realm',
            options={'ordering': ('name', '-created_at')},
        ),
        migrations.AddField(
            model_name='realmauthenticationsession',
            name='expires_at',
            field=models.DateTimeField(null=True),
        ),
    ]
