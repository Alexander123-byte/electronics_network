"""
Скрипт для быстрого наполнения базы данных тестовыми данными.
Запуск: python scripts/populate_db.py
"""
import os
import sys
import django

# Добавляем путь к корневой директории проекта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Устанавливаем настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Инициализируем Django
django.setup()

from django.core.management import call_command
from django.contrib.auth import get_user_model
from network.models import NetworkNode, Contact, Product


def main():
    print("🚀 Начинаем наполнение базы данных...")
    
    # Очищаем базу
    print("🧹 Очищаем базу данных...")
    call_command('flush', '--noinput')

    # Генерируем тестовые данные
    print("📦 Генерируем тестовые данные...")
    call_command('generate_test_data')
    
    # Проверяем, что данные созданы
    contacts_count = Contact.objects.count()
    products_count = Product.objects.count()
    nodes_count = NetworkNode.objects.count()
    
    print("\n✅ База данных успешно наполнена!")
    print(f"   Создано контактов: {contacts_count}")
    print(f"   Создано продуктов: {products_count}")
    print(f"   Создано звеньев сети: {nodes_count}")
    
    # Проверяем задолженность ИП
    print("\n💰 ПРОВЕРКА ЗАДОЛЖЕННОСТИ ИП:")
    entrepreneurs = NetworkNode.objects.filter(level=2)
    total_ip_debt = 0
    for ip in entrepreneurs:
        print(f"   {ip.name}: {ip.debt} ₽")
        total_ip_debt += ip.debt
    print(f"   ВСЕГО ИП: {total_ip_debt} ₽")
    
    print("\n📝 Данные для входа в админку:")
    print("   Логин: admin")
    print("   Пароль: rewty76")
    print("\n🌐 Админ-панель: http://localhost:8000/admin/")
    print("🌐 API: http://localhost:8000/api/")
    print("📚 Документация: http://localhost:8000/swagger/")


if __name__ == '__main__':
    main()
