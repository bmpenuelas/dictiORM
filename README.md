It's a dict... It's an ORM... It's dictiORM!
==============================================

A tiny MongoDB ORM that takes zero time to setup because docs become simple dicts.
----------------------------------------------------------------------------------

- Use your database documents **like a simple dictionary variable**. Even in functions that expect a dict!
```python
>>> user_info = dictiorm.Document(collection, {'username': 'user0'})
>>> isinstance(user_info, dict)
True
```

- You **do not have to predefine models**, in compliance with with MongoDB philosophy of variable document structure.
```python
>>> user_info['age'] = 26  # Create a new field, it is automatically added to the DB.
...
>>> print(user_info['status']) # Access a field that exists in the DB even if you dit not explicitly declare it.
```

- And you still have access to document cache/update, find/count, and **validation**.
```python
>>> validation_funcs = { 'username': lambda x: type(x)==str, 'status': lambda x: type(x)==str }
>>> user_info = dictiorm.Document(collection, {'username': 'user0'}, validators=validation_funcs)
...
>>> user_info.pop('status')  # 'status' was popped. As it is a required field, it will fail validation.
ValueError: Validation failed. Not all the required fields are present. Missing: {'status'}
```
  
  
  
  
  
How is it used?
---------------

Simply put: like you use a normal dictionary in Python, with some additional features. You just need:
  * `unique_identifier` : The field or fields and values used to select the specific document that you want.
    Example: `unique_identifier = {'customer_type': 'premium', username': 'user0'}`

  * `collection_connection` : The pymongo connector that points to the database.collection that stores that document.
    Example: `collection = user_data.db['user_info']`


That's all you need to create a dictiORM object! It will behave like a **dictionary**, and data will be automagically mirrored with a database **document**!

`user_info = dictiorm.Document(collection, unique_identifier)`
  
  
  
  
Now you can perform all the operations you are used to:

`user_info['gender'] ` Read a field that was stored in the database.

`user_info['age'] = 26` Change the value of an existing field or create a new one.

`user_info.pop('age', None)` Remove a field and get it's value.

`list(user_info)` Convert into a list.

`user_info.keys()` Get the name of all the fields.

**... 
and everything you can do with a regular dictionary!**


Even pass it to a function that expects a dict:

```python
  ...
  new_user_info = function_that_works_with_dictionaries( user_info )
  ...
```
  
  
  
  
  
  
Additional functionalities
--------------------------

* `initial_values` Fill the doc with additional fields the moment you create it.

  Example: `initial_values = {'status': 'registered'}`
  
  
  
* `validators` **This is an extremely useful feature!** You can define a function that evaluates if the value of a field  fulfills some requirements. If at any moment an invalid value were to be assigned, it would not pass the validation and that modificatioin would never happen. Not in the local object, neither in the database.
  Example: `validators = { 'username': lambda x: type(x) == str, 'amount': lambda x: x < 1000 }`
  
  
  
  You can set validators for any number of fields that you want, and let the other fields be changed freely, or...

* `only_validated_fields` you can set this to `True`. This way this dictionary will only be allowed to contain the fields that you have set validators for, and only with values that pass your validation criteria.
  
  
  
* `always_access_db` By default, every modification is mirrored in the database. You can disable this and do it manually whenever you want using:
  - yourDoc.update_memory() to read the database and apply changes to your local object.
  - yourDoc.update_database() to upload local modifications to the database.
  
  
  
* `yourDoc.delete()` Remove the document from the database. Removal of the object in memory is performed automatically by Python's garbage collection.
  
  
  
  
v0.1 - Pretty functional proof of concept release. More features to come! Questions, comments and contributions always welcome  : )
  