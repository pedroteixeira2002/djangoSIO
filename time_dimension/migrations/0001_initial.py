# Generated by Django 5.0.6 on 2024-05-25 09:24

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TimeDimension',
            fields=[
                ('date', models.DateField()),
                ('sk_year_month', models.CharField(max_length=150, primary_key=True, serialize=False, unique=True)),
            ],
        ),
    ]
