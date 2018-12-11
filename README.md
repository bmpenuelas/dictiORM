It's a dict... It's an ORM... It's dictiORM! :airplane:
=======================================================

A tiny MongoDB ORM that takes zero time to setup because docs:page_with_curl: become simple dicts **{}**
--------------------------------------------------------------------------------------------------------

Read and write the documents in your database like if you were using normal dictionary variables in Python.

<br>

- All the database accesses are abstracted for you. **If you know how to use a Python dictionary, that's all you need to read and write a MongoDB database.**
```python
>>> user_info = collection.Document({'username': 'user0'})
...
>>> user_info['age'] = 26  # Write a new field, or change its value
...
>>> print(user_info['status']) # Read a field in the DB even if you dit not explicitly declare it
```

<br>

- You **do not need to predefine models**, in compliance with with MongoDB philosophy of variable document structure. Use it even with functions that expect a dict!
```python
>>> isinstance(user_info, dict)
True
```

<br>

- And you still have access to document cache/update, find/count, all the methods of a dict variable and **validation**
```python
>>> validation_funcs = { 'username': lambda x: type(x)==str, 'status': lambda x: x in ('on', 'off') }
>>> user_info = collection.Document({'username': 'user0'}, validators=validation_funcs)
...
>>> user_info.pop('status')  # 'status' was popped, since it is a required field, validation will fail
ValueError: Validation failed. Not all the required fields are present. Missing: {'status'}
```

<br>
<br>
<br>

:inbox_tray: Install from PyPI: `pip install dictiorm`

<br>
<br>
<br>

:raising_hand: How is it used?
------------------------------


Simply put: **like you use a normal dictionary in Python**. You just need:
  * The field or fields and values used to select the specific document that you want.
  <br>Example: `unique_identifier = {'customer_type': 'premium', username': 'user0'}`

  * A connection to your database and the desired collection. This is made easy with:
  <br>`connection = dictiorm.Connection(**database_credentials)`
  <br>`collection = connection.Collection('collection_name')`


That's all you need to create a dictiORM object! It will behave like a **dictionary**, and data will be automagically mirrored in a database **document**!

`user_info = collection.Document(unique_identifier)`

<br>
<br>

Now you can perform all the operations you are used to:

`user_info['gender'] ` Read a field that was stored in the database.

`user_info['age'] = 27` Change the value of an existing field or create a new one.

`user_info.pop('age', None)` Remove a field and get it's value.

`list(user_info)` Convert into a list.

`user_info.keys()` Get the name of all the fields.

...**and everything you can do with a regular dictionary!**
Check out [the examples](/example) for more.

<br>
<br>
<br>


:bulb: Additional functionalities
---------------------------------

<br>

:ballot_box_with_check: `validators` **This is an really useful feature!** You can define a function that evaluates whether if the value of a field  fulfills some requirements. If at any moment an invalid value was to be assigned, it would not pass the validation and that modification would never happen. Not in the local object, neither in the database.

<br>

Example: `validators = { 'username': lambda x: type(x) == str, 'amount': lambda x: x < 1000 }`

<br>

  You can set validators for any number of fields that you want, and let the other fields be changed freely, or...

* `only_validated_fields` you can set this to `True` and this dictionary will only be allowed to contain the fields that you have set validators for, and only with values that pass your validation criteria.

<br>
<br>

:arrows_clockwise: `always_access_db` By default, every modification is mirrored in the database. You can disable this and do it manually whenever you want using:
  - some_doc.update_memory() to read the database and apply changes to your local object.
  - some_doc.update_database() to upload local modifications to the database.

<br>
<br>

:zero: `initial_values` Fill the doc with additional fields the moment you create it if those fields don't have a value already.
<br>Example: `initial_values = {'status': 'registered'}`

<br>
<br>

:x: `some_doc.delete()` Remove the document from the database. Removal of the object in memory is performed automatically by Python's garbage collection. (Also available as `Group.delete_all()`)

<br>
<br>

:paperclip: `Group` You can get the all the documents that match some filter inside a collection with a single command.
<br>Example: `collection.Group({'status': 'active'})` to get all the documents with status active.
