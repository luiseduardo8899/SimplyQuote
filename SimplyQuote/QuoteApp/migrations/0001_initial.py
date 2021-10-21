# Generated by Django 3.2.8 on 2021-10-20 21:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_id', models.IntegerField(default=0)),
                ('create_date', models.DateTimeField(verbose_name='date published')),
                ('company_name', models.CharField(max_length=200)),
                ('main_contact', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_code', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200)),
                ('lease_term', models.IntegerField(default=12)),
                ('list_price', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='SalesPerson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('salesid', models.IntegerField(default=0)),
                ('phone_number', models.CharField(default='', max_length=200)),
                ('create_date', models.DateTimeField(verbose_name='date published')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('quote_id', models.IntegerField(default=0, primary_key=True, serialize=False)),
                ('quote_name', models.CharField(max_length=200)),
                ('create_date', models.DateTimeField(verbose_name='date published')),
                ('state', models.IntegerField(choices=[(0, 'created_tag'), (1, 'registered_tag'), (2, 'accepted_tag'), (3, 'rejected_tag'), (4, 'invalidated_tag')], default=0)),
                ('quantity', models.IntegerField()),
                ('taxable', models.IntegerField(choices=[(0, 'nontaxable_tag'), (1, 'taxable_tag'), (2, 'see_tcs_tags')], default=0)),
                ('discount', models.IntegerField(default=0)),
                ('term', models.IntegerField(choices=[(0, 'net15_tag'), (1, 'net30_tag'), (2, 'net45_tag'), (3, 'net60_tag'), (4, 'net90_tag'), (5, 'other_tag')], default=1)),
                ('validity', models.IntegerField(default=30)),
                ('account', models.ManyToManyField(to='QuoteApp.Account')),
                ('product', models.ManyToManyField(to='QuoteApp.Product')),
                ('sales_person', models.ManyToManyField(to='QuoteApp.SalesPerson')),
            ],
            options={
                'ordering': ['create_date'],
            },
        ),
        migrations.CreateModel(
            name='PO',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('po_id', models.IntegerField(default=0)),
                ('po_name', models.CharField(max_length=200)),
                ('state', models.IntegerField(choices=[(0, 'created_tag'), (1, 'registered_tag'), (2, 'accepted_tag'), (3, 'rejected_tag'), (4, 'invalidated_tag')], default=0)),
                ('create_date', models.DateTimeField(verbose_name='date published')),
                ('validity', models.IntegerField(default=30)),
                ('po_url', models.URLField()),
                ('account', models.ManyToManyField(to='QuoteApp.Account')),
                ('quote', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='QuoteApp.quote')),
                ('sales_person', models.ManyToManyField(to='QuoteApp.SalesPerson')),
            ],
        ),
    ]
