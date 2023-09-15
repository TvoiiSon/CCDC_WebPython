def add_value_to_dict(my_di, key, value):
    if key in my_di:
        # Если ключ уже существует в словаре, добавляем значение в множество
        my_di[key].add(value)
    else:
        # Если ключа нет, создаем новую запись в словаре с ключом и множеством значений
        my_di[key] = {value}


# Пример использования
my_dict = {}
add_value_to_dict(my_dict, 'key1', 'value1')
add_value_to_dict(my_dict, 'key1', 'value3')
add_value_to_dict(my_dict, 'key2', 'value2')
add_value_to_dict(my_dict, 'key1', 'value1')  # Это значение уже есть и не будет добавлено

print(my_dict)
