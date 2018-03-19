It's a dict... It's an ORM... It's dictiORM!
==============================================

A tiny MongoDB ORM that takes zero time to setup because docs become simple dicts.
----------------------------------------------------------------------------------

- Use your database documents **like a simple dictionary variable**.
```python
>>> user_info = dictiorm.Document(collection, {'username': 'user0'})
>>> isinstance(user_info, dict)
True
```

- You **do not have to predefine models**, in compliance with with MongoDB philosophy of variable document structure.
```python
>>> user_info['age'] = 26  # Create a new field, it is automatically added to the DB
...
>>> print(user_info['status']) # Access a field that exists in the DB even if you dit not explicitly declare it
```

- And you still have access to document cache/update, find/count, and **validation**.
```python
>>> validation_funcs = { 'username': lambda x: type(x)==str, 'status': lambda x: type(x)==str }
>>> user_info = dictiorm.Document(collection, {'username': 'user0'}, validators=validation_funcs)
...
>>> user_info.pop('status')  # 'status' was popped, as it is a required field, it will fail validation
ValueError: Validation failed. Results: {'username': True, 'status': False}
```
