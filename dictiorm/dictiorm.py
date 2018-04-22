# -*- coding: utf-8 -*-
"""dictiORM

   A tiny MongoDB ORM that takes zero time to setup because all objects are dictionaries.


   ReadME and latest sources:
   https://github.com/bmpenuelas/dictiORM
"""

import pymongo
from   pymongo.collection import ReturnDocument
from   bson.objectid      import ObjectId

from   itertools import chain




###############################################################################
# Make it compatible with both Python 2.x and 3.x
###############################################################################

try:              # Python 2
    str_base = basestring
    items = 'iteritems'
except NameError: # Python 3
    str_base = str, bytes, bytearray
    items = 'items'

_RaiseKeyError = object()




###############################################################################
# Generic helper functions
###############################################################################

def id_to_str(document):
    if document and '_id' in document:
        document['_id'] = str(document['_id'])
    return document



def combine(recent_data, past_data):
    result = past_data
    for key in recent_data:
        result[key] = recent_data[key]
    return result


###############################################################################
# DictiORM classes
###############################################################################

class Document(dict):

    __slots__ = ('collection_connection',
                 'unique_identifier',
                 'validators',
                 'only_validated_fields',
                 'always_access_db'
                )



    # -------------------------------------------------------------------------
    # Overrides of dict
    # -------------------------------------------------------------------------

    @staticmethod
    def _process_args(mapping=(), **kwargs):
        if hasattr(mapping, items):
            mapping = getattr(mapping, items)()
        return {key: value for key, value in chain(mapping, getattr(kwargs, items)())}



    def __init__(self, collection_connection, unique_identifier, initial_values={}, validators={}, only_validated_fields=False, always_access_db=True, mapping=()):
        self.collection_connection = collection_connection
        self.unique_identifier = unique_identifier
        self.validators = validators
        self.only_validated_fields = only_validated_fields
        self.always_access_db = always_access_db

        self.validators['_id'] = lambda x: type(x)==str


        initial_values = combine(unique_identifier, initial_values)
        valid, valid_fields, invalid_fields = self.validate(initial_values)

        if invalid_fields:
            raise ValueError('Init validation failed. Conflicting fields: ' + str(invalid_fields))

        super(Document, self).__init__(self._process_args(mapping, **valid_fields))


        database_data = self.find_first(self.unique_identifier)
        if database_data:
            super(Document, self).__setitem__('_id', database_data['_id'])
            self.unique_identifier = {'_id': dict(self)['_id']}
            if dict(self) != database_data:
                updated_data = combine(dict(self), database_data)
                for key in updated_data:
                    super(Document, self).__setitem__(key, updated_data[key])
                self.update_database()
        else:
            super(Document, self).__setitem__('_id', self.insert_document(dict(self)))
            self.unique_identifier = {'_id': dict(self)['_id']}



    def __getitem__(self, key):
        self.update_memory()
        return super(Document, self).__getitem__(key)



    def __setitem__(self, key, value):
        self.update_memory()

        valid, valid_fields, invalid_fields = self.validate({key: value})
        if valid:
            super(Document, self).__setitem__(key, value)
        else:
            raise ValueError('Validation failed. Cannot set: ' + str(invalid_fields))

        return self.update_database()



    def __delitem__(self, key):
        self.update_memory()
        super(Document, self).__delitem__(key)
        return self.update_database()



    def get(self, key, default=None):
        self.update_memory()
        return super(Document, self).get(key, default)



    def setdefault(self, key, default=None):
        self.update_memory()

        valid, valid_fields, invalid_fields = self.validate({key: default})
        if valid:
            super(Document, self).setdefault(key, default)
        else:
            raise ValueError('Validation failed. Provided key/default is not valid: ' + str(invalid_fields))
            
        return self.update_database()



    def pop(self, key, v=_RaiseKeyError):
        self.update_memory()
        if v is _RaiseKeyError:
            result = super(Document, self).pop(key)
        else:
            result = super(Document, self).pop(key, v)
        self.update_database()
        return result



    def update(self, mapping=(), **kwargs):
        new_dict = self._process_args(mapping, **kwargs)
        self.update_memory()

        valid, valid_fields, invalid_fields = self.validate(new_dict)
        super(Document, self).update(valid_fields)
        self.update_database()
        if invalid_fields:
            raise ValueError('New elements validation failed. Conflicting fields: ' + str(invalid_fields))



    def __contains__(self, key):
        self.update_memory()
        return super(Document, self).__contains__(key)



    def copy(self):
        raise SyntaxError('Cannot use copy, DB config parameters are needed.')
        # return type(self)(self)



    @classmethod
    def fromkeys(cls, keys, v=None):
        raise SyntaxError('Cannot use fromkeys, DB config parameters are needed.')
        # return super(Document, cls).fromkeys((key for key in keys), v)



    def __repr__(self):
        self.update_memory()
        return '{0}({1})'.format(type(self).__name__, super(Document, self).__repr__())




    # -------------------------------------------------------------------------
    # Typical accesses
    # -------------------------------------------------------------------------

    def insert_document(self, document):
        if '_id' in document:
            document['_id'] = ObjectId(document['_id'])
        return str(self.collection_connection.insert_one(document).inserted_id)



    def find_first(self, filter={}, _id=None):
        if '_id' in filter:
            result = self.collection_connection.find_one({'_id':ObjectId(filter['_id'])})
            return id_to_str(result)
        elif _id:
            result = self.collection_connection.find_one({'_id':ObjectId(_id)})
            return id_to_str(result)
        else:
            result = self.collection_connection.find_one(filter)
            return id_to_str(result)



    def update_first(self, update, filter={}, _id=None):
        update.pop('_id', None)

        if '_id' in filter:
            result = self.collection_connection.find_one_and_replace({'_id': ObjectId(filter['_id'])}, update, upsert=True, return_document=ReturnDocument.AFTER)
        elif _id:
            result = self.collection_connection.find_one_and_replace({'_id': ObjectId(_id)}, update, upsert=True, return_document=ReturnDocument.AFTER)
        else:
            if not filter:
                raise ValueError('Failed to update, _id or filter needed to update document.')
            result = self.collection_connection.find_one_and_replace(filter, update, upsert=True, return_document=ReturnDocument.AFTER)
        return id_to_str(result)




    # -------------------------------------------------------------------------
    # Class methods
    # -------------------------------------------------------------------------

    def update_memory(self):
        if self.always_access_db == True:
            database_data = self.find_first(self.unique_identifier)
            if database_data:
                for db_key in database_data:
                    super(Document, self).__setitem__(db_key, database_data[db_key])



    def update_database(self):
        if self.always_access_db == True:
            required_fields = self.validators.keys()
            if all(field in dict(self) for field in required_fields):
                self.update_first(dict(self), self.unique_identifier)
            else:
                missing_fields = set(required_fields) - set( dict(self) )
                raise ValueError('Validation failed. Not all the required fields are present. Missing: ' + str(missing_fields))



    def validate(self, data={}):
        if not data:
            data = dict(self)

        valid_fields = {}
        invalid_fields = {}
        valid = True

        for key in data:
            if key in self.validators:
                if self.validators[key]( data[key] ):
                    valid_fields[key] = data[key]
                else:
                    invalid_fields[key] = data[key]
                    valid = False

            elif self.only_validated_fields == True:
                invalid_fields[key] = data[key]
                valid = False

            else:
                valid_fields[key] = data[key]

        return valid, valid_fields, invalid_fields

    def delete(self):
        del_filter = self.unique_identifier

        if '_id' in del_filter:
            del_filter = {'_id': ObjectId(del_filter['_id'])}

        result = self.collection_connection.delete_one( del_filter );

        if result.deleted_count != 1:
            raise ValueError('Deleted %d items, not one.' % result.deleted_count)
