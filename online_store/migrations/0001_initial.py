# Generated by Django 3.1.3 on 2020-11-15 20:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Doc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('date', models.DateField(auto_now_add=True, null=True, verbose_name='Дата')),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Владелец')),
            ],
            options={
                'verbose_name': 'Документ',
                'verbose_name_plural': 'Документы',
            },
        ),
        migrations.CreateModel(
            name='DocType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('name', models.CharField(default=None, max_length=255, verbose_name='Наименование')),
            ],
            options={
                'verbose_name': 'Тип документа',
                'verbose_name_plural': 'Типы документов',
            },
        ),
        migrations.CreateModel(
            name='GoodUnits',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('name', models.CharField(default=None, max_length=255, verbose_name='Наименование')),
            ],
            options={
                'verbose_name': 'Единица измерения',
                'verbose_name_plural': 'Единицы измерения',
            },
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('name', models.CharField(default=None, max_length=255, verbose_name='Наименование')),
            ],
            options={
                'verbose_name': 'Магазин',
                'verbose_name_plural': 'Магазины',
            },
        ),
        migrations.CreateModel(
            name='Good',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('name', models.CharField(default=None, max_length=255, verbose_name='Наименование')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='online_store.goodunits', verbose_name='Единаца измерения')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
            },
        ),
        migrations.CreateModel(
            name='DocGoods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('quantity', models.IntegerField(null=True)),
                ('doc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='online_store.doc', verbose_name='Документ')),
                ('good', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='online_store.good', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Товары в документа',
                'verbose_name_plural': 'Товары в документа',
            },
        ),
        migrations.AddField(
            model_name='doc',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='online_store.shop', verbose_name='Магазин'),
        ),
        migrations.AddField(
            model_name='doc',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='online_store.doctype', verbose_name='Тип документа'),
        ),
    ]
