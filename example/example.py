#!/usr/bin/env python3
"""dictiORM usage example

   ReadME and latest sources:
   https://github.com/bmpenuelas/dictiORM
"""

import dictiorm



# Connect to your database
database_credentials = {'url': url, 'port': port, 'database_name': database_name,
                        'user': user, 'password': password}
collection_name = 'user_info'
collection = dictiorm.Connection(**database_credentials)[collection_name]




#%% Example 1
#   Simplest use case

unique_identifier = {'username': 'user0'}  # Select the feature(s) that make your document unique

user_info = dictiorm.Document(collection, unique_identifier)  # Create the magic dictiORM dictionary


print('Is dictionary? ' + str( isinstance(user_info, dict)) )  # You can use a dictiORM object with
                                                               # functions that expect dicts

user_info['age'] = 25  # Assign new or existing fields as you would with a dictionary, changes are
                       # saved to the database
print(user_info['age'])  # Read a field from the dictionary, the value is read from the database




#%% Example 2
#   Extended use case

unique_identifier = {'username': 'user1'}  # Select the feature(s) that make your document unique
initial_values = {'status': 'registered'}  # Fill the doc with additional initial fields
validators = { 'username': lambda x: type(x)==str,  # If you want to perform validation, you are
               'status': lambda x: type(x)==str}    # completely free to define the data validation
                                                    # functions for as many fields as you want and
                                                    # only in the instances that you want
only_validated_fields = True  # Choose variable document structure like MongoDB and dicts,
                              # or fixed structure, for example for user input
always_access_db = True  # You decide if every local modification is mirrored in the DB or synced manually


user_info = dictiorm.Document(collection, unique_identifier, initial_values, validators, only_validated_fields, always_access_db)


print(user_info)  # No problem, the dict only contains validated fields

try:
    user_info['age'] = 26  # 'only_validated_fields' is set, and the fields with validators are
except ValueError as err:  # 'username' and 'status'. Since 'age' is not one of them, validation
    print(err)             # fails and the 'age' field is never created

print(user_info)  # 'age' was not set


user_info.delete()  # Remove the document from the database (removal of the object in memory is
                    # performed automatically by Python's garbage collection)
