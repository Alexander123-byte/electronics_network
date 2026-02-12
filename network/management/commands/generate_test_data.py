import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.db import models
from network.models import Contact, Product, NetworkNode


class Command(BaseCommand):
    help = 'Генерирует тестовые данные для сети электроники'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Начинаем генерацию тестовых данных...'))

        # Очищаем существующие данные
        self.stdout.write('Очищаем базу данных...')
        NetworkNode.objects.all().delete()
        Product.objects.all().delete()
        Contact.objects.all().delete()

        # Создаем контакты
        self.stdout.write('Создаем контакты...')
        contacts = self.create_contacts()

        # Создаем продукты
        self.stdout.write('Создаем продукты...')
        products = self.create_products()

        # Создаем заводы (уровень 0)
        self.stdout.write('Создаем заводы...')
        factories = self.create_factories(contacts[:3], products)

        # Создаем розничные сети (уровень 1)
        self.stdout.write('Создаем розничные сети...')
        retailers = self.create_retailers(contacts[3:8], products, factories)

        # Создаем ИП (уровень 2) - поставщики только розничные сети!
        self.stdout.write('Создаем индивидуальных предпринимателей...')
        self.create_entrepreneurs(contacts[8:15], products, retailers)  # Передаем только retailers, не factories!

        self.stdout.write(self.style.SUCCESS('✅ Тестовые данные успешно созданы!'))

        # Выводим статистику
        self.show_statistics()

    def create_contacts(self):
        """Создание контактов"""
        contacts_data = [
            # Заводы
            {'email': 'factory@xiaomi.cn', 'country': 'Китай', 'city': 'Пекин', 'street': 'Улица Технологий',
             'house_number': '1'},
            {'email': 'factory@samsung.kr', 'country': 'Южная Корея', 'city': 'Сеул', 'street': 'Digital Street',
             'house_number': '100'},
            {'email': 'factory@sony.jp', 'country': 'Япония', 'city': 'Токио', 'street': 'Shinjuku',
             'house_number': '5-10-15'},

            # Розничные сети России
            {'email': 'info@mvideo.ru', 'country': 'Россия', 'city': 'Москва', 'street': 'Ленинградское шоссе',
             'house_number': '16'},
            {'email': 'contact@eldorado.ru', 'country': 'Россия', 'city': 'Москва', 'street': 'Улица 1905 года',
             'house_number': '25'},
            {'email': 'info@dns-shop.ru', 'country': 'Россия', 'city': 'Владивосток', 'street': 'Светланская',
             'house_number': '45'},
            {'email': 'info@citilink.ru', 'country': 'Россия', 'city': 'Санкт-Петербург', 'street': 'Невский проспект',
             'house_number': '50'},
            {'email': 'info@technopoint.ru', 'country': 'Россия', 'city': 'Екатеринбург', 'street': 'Ленина',
             'house_number': '25'},

            # Индивидуальные предприниматели
            {'email': 'ip.ivanov@mail.ru', 'country': 'Россия', 'city': 'Новосибирск', 'street': 'Красный проспект',
             'house_number': '120'},
            {'email': 'ip.petrov@yandex.ru', 'country': 'Россия', 'city': 'Казань', 'street': 'Баумана',
             'house_number': '15'},
            {'email': 'ip.sidorov@gmail.com', 'country': 'Россия', 'city': 'Нижний Новгород',
             'street': 'Большая Покровская', 'house_number': '30'},
            {'email': 'ip.smirnov@list.ru', 'country': 'Россия', 'city': 'Самара', 'street': 'Московское шоссе',
             'house_number': '18'},
            {'email': 'ip.kuznetsov@bk.ru', 'country': 'Россия', 'city': 'Ростов-на-Дону', 'street': 'Буденновский',
             'house_number': '55'},
            {'email': 'ip.popov@mail.ru', 'country': 'Россия', 'city': 'Уфа', 'street': 'Октября',
             'house_number': '82'},
            {'email': 'ip.vasiliev@yandex.ru', 'country': 'Россия', 'city': 'Красноярск', 'street': 'Мира',
             'house_number': '45'},

            # Дополнительные контакты
            {'email': 'shop@technodom.kz', 'country': 'Казахстан', 'city': 'Алматы', 'street': 'Абая',
             'house_number': '150'},
            {'email': 'info@technoplus.by', 'country': 'Беларусь', 'city': 'Минск', 'street': 'Независимости',
             'house_number': '85'},
        ]

        contacts = []
        for data in contacts_data:
            contact = Contact.objects.create(**data)
            contacts.append(contact)
            self.stdout.write(f'  Создан контакт: {contact.city}, {contact.street}')

        return contacts

    def create_products(self):
        """Создание продуктов"""
        products_data = [
            # Смартфоны Xiaomi
            {'name': 'Xiaomi 14 Ultra', 'model': '23113RKC6G', 'release_date': '2024-02-22'},
            {'name': 'Xiaomi 14', 'model': '23127PCC0G', 'release_date': '2024-02-22'},
            {'name': 'Redmi Note 13 Pro', 'model': '2312DRAABG', 'release_date': '2024-01-15'},
            {'name': 'Redmi Note 13', 'model': '23129RAA4G', 'release_date': '2024-01-15'},
            {'name': 'POCO X6 Pro', 'model': '2311DRK48G', 'release_date': '2024-01-12'},

            # Смартфоны Samsung
            {'name': 'Samsung Galaxy S24 Ultra', 'model': 'SM-S928B', 'release_date': '2024-01-31'},
            {'name': 'Samsung Galaxy S24+', 'model': 'SM-S926B', 'release_date': '2024-01-31'},
            {'name': 'Samsung Galaxy S24', 'model': 'SM-S921B', 'release_date': '2024-01-31'},
            {'name': 'Samsung Galaxy Z Fold5', 'model': 'SM-F946B', 'release_date': '2023-08-11'},
            {'name': 'Samsung Galaxy Z Flip5', 'model': 'SM-F731B', 'release_date': '2023-08-11'},

            # Смартфоны Sony
            {'name': 'Sony Xperia 1 V', 'model': 'XQ-DQ72', 'release_date': '2023-07-28'},
            {'name': 'Sony Xperia 5 V', 'model': 'XQ-DE72', 'release_date': '2023-09-15'},
            {'name': 'Sony Xperia 10 V', 'model': 'XQ-DC72', 'release_date': '2023-06-15'},

            # Ноутбуки и аксессуары
            {'name': 'Xiaomi Book S 12.4', 'model': '230502FP', 'release_date': '2023-12-01'},
            {'name': 'Samsung Galaxy Book4 Pro', 'model': 'NP960XGL', 'release_date': '2024-01-15'},
            {'name': 'Sony VAIO SX14', 'model': 'VJS141', 'release_date': '2023-10-20'},

            # Дополнительные товары
            {'name': 'Xiaomi Smart Band 8 Pro', 'model': 'M2233B1', 'release_date': '2023-10-26'},
            {'name': 'Samsung Galaxy Watch6', 'model': 'SM-R940', 'release_date': '2023-08-11'},
            {'name': 'Sony WH-1000XM5', 'model': 'WH1000XM5', 'release_date': '2022-05-20'},
            {'name': 'Xiaomi Electric Scooter 4 Pro', 'model': 'DDHBC02MN', 'release_date': '2023-03-15'},
        ]

        products = []
        for data in products_data:
            product = Product.objects.create(**data)
            products.append(product)
            self.stdout.write(f'  Создан продукт: {product.name} ({product.model})')

        return products

    def create_factories(self, contacts, products):
        """Создание заводов (уровень 0)"""
        factories = []
        factory_data = [
            {
                'name': 'Xiaomi Manufacturing Plant',
                'contact': contacts[0],
                'debt': Decimal('0.00'),
            },
            {
                'name': 'Samsung Electronics Factory',
                'contact': contacts[1],
                'debt': Decimal('0.00'),
            },
            {
                'name': 'Sony Production Facility',
                'contact': contacts[2],
                'debt': Decimal('0.00'),
            },
        ]

        for i, data in enumerate(factory_data):
            factory = NetworkNode.objects.create(
                name=data['name'],
                contact=data['contact'],
                debt=data['debt'],
                supplier=None
            )

            if i == 0:  # Xiaomi
                factory.products.set(products[:5] + [products[13], products[16], products[18]])
            elif i == 1:  # Samsung
                factory.products.set(products[5:10] + [products[14], products[17]])
            elif i == 2:  # Sony
                factory.products.set(products[10:13] + [products[15]])

            factories.append(factory)
            self.stdout.write(f'  Создан завод: {factory.name} (уровень {factory.level})')

        return factories

    def create_retailers(self, contacts, products, factories):
        """Создание розничных сетей (уровень 1)"""
        retailers = []
        retailer_data = [
            {
                'name': 'М.Видео',
                'contact': contacts[0],
                'supplier': factories[0],  # Xiaomi
                'debt': Decimal('1500000.50'),
            },
            {
                'name': 'Эльдорадо',
                'contact': contacts[1],
                'supplier': factories[0],  # Xiaomi
                'debt': Decimal('2300000.75'),
            },
            {
                'name': 'DNS',
                'contact': contacts[2],
                'supplier': factories[1],  # Samsung
                'debt': Decimal('3200000.25'),
            },
            {
                'name': 'Ситилинк',
                'contact': contacts[3],
                'supplier': factories[1],  # Samsung
                'debt': Decimal('1800000.00'),
            },
            {
                'name': 'Технопоинт',
                'contact': contacts[4],
                'supplier': factories[2],  # Sony
                'debt': Decimal('950000.30'),
            },
        ]

        for data in retailer_data:
            retailer = NetworkNode.objects.create(
                name=data['name'],
                contact=data['contact'],
                supplier=data['supplier'],
                debt=data['debt']
            )

            supplier_products = data['supplier'].products.all()
            retailer.products.set(supplier_products)

            retailers.append(retailer)
            self.stdout.write(f'  Создана розничная сеть: {retailer.name} (уровень {retailer.level})')

        return retailers

    def create_entrepreneurs(self, contacts, products, retailers):
        """Создание индивидуальных предпринимателей (уровень 2)
        Поставщиками могут быть только розничные сети, не заводы!
        """
        entrepreneurs = []
        entrepreneur_data = [
            {
                'name': 'ИП Иванов А.А.',
                'contact': contacts[0],
                'supplier': retailers[0],  # М.Видео
                'debt': Decimal('250000.45'),
            },
            {
                'name': 'ИП Петров Б.Б.',
                'contact': contacts[1],
                'supplier': retailers[1],  # Эльдорадо
                'debt': Decimal('180000.90'),
            },
            {
                'name': 'ИП Сидоров В.В.',
                'contact': contacts[2],
                'supplier': retailers[2],  # DNS
                'debt': Decimal('320000.15'),
            },
            {
                'name': 'ИП Смирнов Г.Г.',
                'contact': contacts[3],
                'supplier': retailers[3],  # Ситилинк
                'debt': Decimal('150000.00'),
            },
            {
                'name': 'ИП Кузнецов Д.Д.',
                'contact': contacts[4],
                'supplier': retailers[4],  # Технопоинт
                'debt': Decimal('210000.30'),
            },
            {
                'name': 'ИП Попов Е.Е.',
                'contact': contacts[5],
                'supplier': retailers[0],  # М.Видео
                'debt': Decimal('120000.60'),
            },
            {
                'name': 'ИП Васильев Ж.Ж.',
                'contact': contacts[6],
                'supplier': retailers[2],  # DNS
                'debt': Decimal('195000.25'),
            },
        ]

        for data in entrepreneur_data:
            entrepreneur = NetworkNode.objects.create(
                name=data['name'],
                contact=data['contact'],
                supplier=data['supplier'],
                debt=data['debt']
            )

            supplier_products = data['supplier'].products.all()
            # Берем случайные продукты от поставщика
            product_list = list(supplier_products)
            selected_products = random.sample(product_list, min(random.randint(3, 6), len(product_list)))
            entrepreneur.products.set(selected_products)

            entrepreneurs.append(entrepreneur)
            self.stdout.write(f'  Создан ИП: {entrepreneur.name} (уровень {entrepreneur.level})')

        return entrepreneurs

    def show_statistics(self):
        """Вывод статистики по созданным данным"""
        self.stdout.write('\n' + '=' * 50)
        self.stdout.write(self.style.SUCCESS('📊 СТАТИСТИКА ТЕСТОВЫХ ДАННЫХ:'))
        self.stdout.write('=' * 50)

        contacts_count = Contact.objects.count()
        products_count = Product.objects.count()
        nodes_count = NetworkNode.objects.count()
        factories_count = NetworkNode.objects.filter(level=0).count()
        retailers_count = NetworkNode.objects.filter(level=1).count()
        entrepreneurs_count = NetworkNode.objects.filter(level=2).count()

        total_debt = NetworkNode.objects.aggregate(total=models.Sum('debt'))['total']

        self.stdout.write(f'📧 Контакты: {contacts_count}')
        self.stdout.write(f'📦 Продукты: {products_count}')
        self.stdout.write(f'🏢 Всего звеньев сети: {nodes_count}')
        self.stdout.write(f'🏭 Заводы (уровень 0): {factories_count}')
        self.stdout.write(f'🏬 Розничные сети (уровень 1): {retailers_count}')
        self.stdout.write(f'👤 ИП (уровень 2): {entrepreneurs_count}')
        self.stdout.write(f'💰 Общая задолженность: {total_debt if total_debt else 0} ₽')

        self.stdout.write('=' * 50)

        if nodes_count > 0:
            self.stdout.write('\n📋 ДЕТАЛЬНАЯ ИНФОРМАЦИЯ:')

            self.stdout.write('\n🏭 ЗАВОДЫ:')
            for factory in NetworkNode.objects.filter(level=0):
                self.stdout.write(f'  • {factory.name} - {factory.contact.city}')
                self.stdout.write(f'    Продуктов: {factory.products.count()}')

            self.stdout.write('\n🏬 РОЗНИЧНЫЕ СЕТИ:')
            for retailer in NetworkNode.objects.filter(level=1):
                if retailer.supplier:
                    self.stdout.write(f'  • {retailer.name} - {retailer.contact.city}')
                    self.stdout.write(f'    Поставщик: {retailer.supplier.name}')
                    self.stdout.write(f'    Задолженность: {retailer.debt} ₽')

            self.stdout.write('\n👤 ИНДИВИДУАЛЬНЫЕ ПРЕДПРИНИМАТЕЛИ:')
            for entrepreneur in NetworkNode.objects.filter(level=2):
                if entrepreneur.supplier:
                    self.stdout.write(f'  • {entrepreneur.name} - {entrepreneur.contact.city}')
                    self.stdout.write(f'    Поставщик: {entrepreneur.supplier.name}')
                    self.stdout.write(f'    Задолженность: {entrepreneur.debt} ₽')
