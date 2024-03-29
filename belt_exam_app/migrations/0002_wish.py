# Generated by Django 3.2 on 2021-04-29 07:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('belt_exam_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('is_granted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('likes', models.ManyToManyField(related_name='wishes_liked', to='belt_exam_app.User')),
                ('wished_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishes', to='belt_exam_app.user')),
            ],
        ),
    ]
