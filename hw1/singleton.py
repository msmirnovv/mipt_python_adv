import ctypes

# Singleton через перегрузку __new__
class SingletonWithNew:
    _entity = None

    def __new__(cls):
        if cls._entity is None:
            cls._entity = super().__new__(cls)
        return cls._entity

# Singleton через ctypes
class SingletonWithCtypes:
    _entity_address = ctypes.c_void_p(0)

    def __new__(cls):
        if not cls._entity_address.value:
            instance = super().__new__(cls)
            cls._entity_address = ctypes.c_void_p(id(instance))
            return instance
        else:
            return ctypes.cast(cls._entity_address.value, ctypes.py_object).value

# Singleton через декоратор
def singleton_decorator(cls):
    entities = {}

    def get_instance(*args, **kwargs):
        if cls not in entities:
            entities[cls] = cls(*args, **kwargs)
        return entities[cls]

    return get_instance

@singleton_decorator
class SingletonWithDecorator:
    def __init__(self):
        pass

if __name__ == "__main__":
    # 1. SingletonNew:
    #    + Максимально легковесная реализация
    #    - Невозможно адаптировать для других классов
    #    - Потенциальные race condition'ы в многопоточке
    # Test Singleton with __new__
    singleton_with_new1 = SingletonWithNew()
    singleton_with_new2 = SingletonWithNew()
    print("Test SingletonWithNew:", ("passed" if singleton_with_new1 is singleton_with_new2 else "failed"))

    # 2. SingletonDecorated:
    #    + Универсальное решение для любых классов
    #    + Легко модифицировать поведение через декоратор
    #    - Оригинальный класс становится недоступен напрямую
    # Test Singleton with ctypes
    singleton_with_ctypes1 = SingletonWithCtypes()
    singleton_with_ctypes2 = SingletonWithCtypes()
    print("Test SingletonWithCtypes:", ("passed" if singleton_with_ctypes1 is singleton_with_ctypes2 else "failed"))

    # Test Singleton with decorator
    # 3. SingletonCtypes:
    #    + Прямой доступ к памяти для точного управления экземпляром
    #    + Обход ограничений Python за счет C-совместимого интерфейса
    #    - Сниженная читаемость кода и сложность отладки
    #    - Возможные проблемы безопасности и переносимости
    singleton_with_decorator1 = SingletonWithDecorator()
    singleton_with_decorator2 = SingletonWithDecorator()
    print("Test SingletonWithDecorator:", ("passed" if singleton_with_decorator1 is singleton_with_decorator2 else "failed"))
