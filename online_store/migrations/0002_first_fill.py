# Generated by Django 3.1.3 on 2020-11-14 11:40
import datetime
import random
from django.db import migrations
from django.contrib.auth.hashers import make_password


def fill(apps, schema_editor):
    """ Первичное заполнение БД
    """

    def random_date():
        start_date = datetime.date(2020, 11, 1)
        end_date = datetime.date(2020, 12, 1)

        time_between_dates = end_date - start_date
        days_between_dates = time_between_dates.days
        random_number_of_days = random.randrange(days_between_dates)
        random_date = start_date + datetime.timedelta(days=random_number_of_days)

        return random_date

    GoodUnits = apps.get_model('online_store', 'GoodUnits')
    for name in ('шт', 'кг', 'коробка'):
        GoodUnits.objects.create(name=name)

    # ---
    Good = apps.get_model('online_store', 'Good')
    good_units = GoodUnits.objects.all()
    for idx in range(1, 20):
        Good.objects.create(name=f'Товар {idx}', unit=random.choice(good_units))

    # ---
    Shop = apps.get_model('online_store', 'Shop')
    for idx in range(1, 4):
        Shop.objects.create(name=f'Магазин {idx}')

    # ---
    DocType = apps.get_model('online_store', 'DocType')
    for name in ('Приходная накладная', 'Расходная накладная'):
        DocType.objects.create(name=name)

    # ---
    # todo: добавить группы!

    User = apps.get_model('auth', 'User')

    User.objects.create(
        username='admin',
        password=make_password('litebox1234'),
        is_superuser=True,
        is_staff=True
    )

    for idx in range(1, 10):
        User.objects.create(
            username=f'User{idx}',
            first_name=f'П_ользователь {idx}',
            password=make_password('1234')
        )

    # ---
    Doc = apps.get_model('online_store', 'Doc')
    DocGoods = apps.get_model('online_store', 'DocGoods')

    shops = Shop.objects.all()
    types = DocType.objects.all()
    owners = User.objects.filter(is_superuser=False)
    goods = Good.objects.all()

    for idx in range(1, 10):
        doc = Doc.objects.create(
            shop=random.choice(shops),
            date=random_date(),
            type=random.choice(types),
            owner=random.choice(owners)
        )

        for item in range(1, random.randint(3, 15)):
            DocGoods.objects.create(
                doc=doc,
                good=random.choice(goods),
                quantity=random.randint(1, 100)
            )


class Migration(migrations.Migration):
    dependencies = [
        ('online_store', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(fill)
    ]
