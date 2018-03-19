# -*- coding: utf-8 -*-
"""dictiORM usage example

   ReadME and latest sources:
   https://github.com/bmpenuelas/dictiORM
"""


import dictiorm

from   ct_backend.common       import mongo_connector


user_data = mongo_connector.UserData() # Use your own connector
collection = user_data.db['user_info'] # to the desired DB collection.




# Simplest use case
unique_identifier = {'username': 'user0'}
user_info = dictiorm.Document(collection, unique_identifier)


print(isinstance(user_info, dict))  # You can use a dictiORM object with functions that expect dicts.

user_info['age'] = 26  # Assign new or existing fields as you would with a dictionary.

print(user_info['age'])  # Changes are automatically validated and saved in the DB.






# Extended use case

unique_identifier = {'username': 'user0'}
initial_values = {'doc_type': 'basic_user_info', 'status': 'registered'} # Fill the doc with additional fields.
validators = { 'username': lambda x: type(x)==str,
               'status': lambda x: type(x)==str
             }  # If you want to perform validation you are completely free to define the data validation
                # functions for as many fields as you want and only in the instances that you want.
only_validated_fields = True   # Variable document structure like MongoDB and dicts, or fixed structure,
                               # for example for user input.
always_access_db = True  # You decide if every local modification is mirrored in the DB or synced manually.


user_info = dictiorm.Document(collection, unique_identifier, initial_values, validators, only_validated_fields, always_access_db)


print(isinstance(user_info, dict))

print(user_info)
