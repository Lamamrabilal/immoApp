# Generated by Django 4.2 on 2023-04-20 12:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('immo_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FraisAgence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frais', models.IntegerField(default='8')),
                ('agence', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='immo_app.contratlocataire')),
            ],
        ),
    ]
