# -*- coding: utf-8 -*-
"""dictiORM usage example

   ReadME and latest sources:
   https://github.com/bmpenuelas/dictiORM
"""


import dictiorm

from   backend_lib.common       import mongo_connector


user_data = mongo_connector.UserData() # Use your own connector
collection = user_data.db['user_info'] # to the desired DB collection.




#%% Example 1
#   Simplest use case
unique_identifier = {'username': 'user0'}
user_info = dictiorm.Document(collection, unique_identifier)


print(isinstance(user_info, dict))  # You can use a dictiORM object with functions that expect dicts.

user_info['age'] = 26  # Assign new or existing fields as you would with a dictionary.

print(user_info['age'])  # Changes are automatically validated and saved in the DB.






#%% Example 2
#   Extended use case

unique_identifier = {'username': 'user1'}
initial_values = {'status': 'registered'} # Fill the doc with additional fields.
validators = { 'username': lambda x: type(x)==str,
               'status': lambda x: type(x)==str
             }  # If you want to perform validation you are completely free to define the data validation
                # functions for as many fields as you want and only in the instances that you want.
only_validated_fields = True   # Variable document structure like MongoDB and dicts, or fixed structure,
                               # for example for user input.
always_access_db = True  # You decide if every local modification is mirrored in the DB or synced manually.


user_info = dictiorm.Document(collection, unique_identifier, initial_values, validators, only_validated_fields, always_access_db)


print(user_info) # No problem, only contains validated fields.

user_info['age'] = 26 # 'only_validated_fields' is set, so validation fails and the 'age' field is never created.
print(user_info) # 'age' was not set.


user_info.delete() # Remove the document from the database. Removal of the object in memory is performed automatically by Python's garbage collection.
