#!/usr/bin/env python3
"""dictiORM usage example

   ReadME and latest sources:
   https://github.com/bmpenuelas/dictiORM
"""

import dictiorm



# Connect to your database
database_credentials = {'url': url, 'port': port, 'database_name': database_name,
                        'user': user, 'password': password}
collection_name = 'users_info'
collection = dictiorm.Connection(**database_credentials)[collection_name]




#%% Example 1
#   Simplest use case

unique_identifier = {'username': 'user0'}  # Select the feature(s) that make your document unique

user0_info = dictiorm.Document(collection, unique_identifier)  # Create the magic dictiORM dictionary


print('Is dictionary? ' + str( isinstance(user0_info, dict)) )  # You can use a dictiORM object with
                                                                # functions that expect dicts

user0_info['age'] = 25  # Assign new or existing fields as you would with a dictionary, changes are
                        # saved to the database
print(user0_info['age'])  # Read a field from the dictionary, the value is read from the database




#%% Example 2
#   Extended use case using validators

unique_identifier = {'username': 'user1'}  # Select the feature(s) that make your document unique
initial_values = {'age': 18}  # Fill the doc with additional initial fields
validators = { 'username': lambda x: type(x)==str,  # If you want to perform validation, you are
               'age': lambda x: x>0}                # completely free to define the data validation
                                                    # functions for as many fields as you want and
                                                    # only in the instances that you want
only_validated_fields = True  # Choose variable document structure like MongoDB and dicts,
                              # or fixed structure, for example for user input
always_access_db = True  # You decide if every local modification is mirrored in the DB or synced manually


user1_info = dictiorm.Document(collection, unique_identifier, initial_values, validators, only_validated_fields, always_access_db)


try:
    user1_info['age'] = -1  # The validator says that 'age' must be > 0, so this will fail
except ValueError as err:   # and the value -1 will never be assigned
    print(err)

print(user1_info)  # 'age' was not changed, it remains at it's initial value (18)

try:
    user1_info['country'] = 'Freedonia'  # 'only_validated_fields' is set, and the fields with
except ValueError as err:                # validators are 'username', 'status' and 'age'. Since
    print(err)                           # 'country' is not one of them, validation fails

print(user1_info)  # The field 'country' was not created


user1_info.delete()  # Remove the document from the database (removal of the object in memory is
                     # performed automatically by Python's garbage collection)
