# Generated by Django 4.2.6 on 2023-11-21 10:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_like_cnt'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='author',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='app.profile'),
            preserve_default=False,
        ),
    ]