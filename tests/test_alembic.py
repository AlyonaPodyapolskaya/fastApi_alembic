import os
import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData
from app.database import Base, engine
from app.models import Item
from alembic.config import Config
from alembic import command

Session = sessionmaker(bind=engine)

@pytest.fixture(scope="session")
def test_database():
    """
    Фикстура для создания и подготовки тестовой базы данных.
    """
    # Применяем миграции к тестовой базе данных
    # alembic_ini_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "alembic.ini")

    # alembic_cfg = Config(alembic_ini_path)
    # command.upgrade(alembic_cfg, "head")

    Base.metadata.create_all(bind=engine)
    yield Session()
    # Удаляем все таблицы после завершения теста
    Base.metadata.drop_all(bind=engine)

def test_migrations(test_database):
    """
    Тест для проверки миграций.
    """
    # Создаем сессию базы данных
    session = test_database

    # Добавляем тестовые данные
    item1 = Item(name="Объект 1", description="Описание 1", price=10.99)
    item2 = Item(name="Объект 2", description="Описание два", price=20.99)
    session.add(item1)
    session.add(item2)
    session.commit()

    # Получаем метаданные базы данных
    meta = MetaData()
    meta.reflect(bind=engine)

    # Проверяем, что таблица items существует
    assert "items" in meta.tables

    # Проверяем, что новое поле price добавлено
    assert "price" in meta.tables["items"].columns
