# Generated by Django 2.0.5 on 2018-11-06 23:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('username', models.CharField(blank=True, max_length=255)),
                ('password', models.CharField(blank=True, max_length=255)),
                ('api_key', models.CharField(blank=True, max_length=255, null=True)),
                ('api_secret', models.CharField(blank=True, max_length=255, null=True)),
                ('is_active', models.BooleanField(default=True, help_text='Is active account on exchange')),
                ('exchange', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.Exchange')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
