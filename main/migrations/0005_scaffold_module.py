# Generated by Django 2.2 on 2019-04-08 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_scaffold'),
    ]

    operations = [
        migrations.AddField(
            model_name='scaffold',
            name='module',
            field=models.CharField(choices=[('WC', 'Web Coding'), ('CE', 'Computer Essentials'), ('IS', 'Information Systems'), ('PR', 'Programming'), ('SI', 'Social Issues')], default='PR', max_length=2),
            preserve_default=False,
        ),
    ]
