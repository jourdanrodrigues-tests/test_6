# Generated by Django 2.0.5 on 2018-09-17 15:47

import datetime
from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChocolatePreference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('milk', models.PositiveSmallIntegerField(choices=[(1, 'Hate'), (2, 'Dislike'), (3, 'Neutral'), (4, 'Like'), (5, 'Love')], verbose_name='milk')),
                ('dark', models.PositiveSmallIntegerField(choices=[(1, 'Hate'), (2, 'Dislike'), (3, 'Neutral'), (4, 'Like'), (5, 'Love')], verbose_name='dark')),
                ('white', models.PositiveSmallIntegerField(choices=[(1, 'Hate'), (2, 'Dislike'), (3, 'Neutral'), (4, 'Like'), (5, 'Love')], verbose_name='white')),
            ],
        ),
        migrations.CreateModel(
            name='ChocolateRecommendation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recommendation', django.contrib.postgres.fields.jsonb.JSONField(editable=False, verbose_name='recommendation')),
                ('date', models.DateTimeField(default=datetime.datetime.now, editable=False, verbose_name='date')),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('billing_day', models.PositiveSmallIntegerField(verbose_name='billing day')),
                ('card_token', models.CharField(max_length=200)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerBillEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date.today, editable=False, verbose_name='date')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bill_events', to='app.Customer')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chocolate_selection', models.CharField(max_length=200, verbose_name='chocolate selection')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='app.Customer')),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('length', models.PositiveSmallIntegerField(choices=[(1, 'Monthly'), (2, '6 months')])),
                ('customer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.Customer')),
            ],
        ),
        migrations.CreateModel(
            name='SubscriptionValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField(editable=False, verbose_name='value')),
                ('date', models.DateField(auto_now=True, verbose_name='date')),
                ('user_responsible', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions_added', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='chocolaterecommendation',
            name='customer',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='chocolate_recommendations', to='app.Customer'),
        ),
        migrations.AddField(
            model_name='chocolatepreference',
            name='customer',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='chocolate_preference', to='app.Customer'),
        ),
    ]
