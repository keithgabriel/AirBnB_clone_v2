#!/usr/bin/python3
""" Module for testing file storage"""
import unittest
from models.base_model import BaseModel
from models.state import State
from models import storage
import os


class TestFileStorage(unittest.TestCase):
    """ Class to test the file storage method """

    def setUp(self):
        """ Set up test environment """
        del_list = []
        for key in storage._FileStorage__objects.keys():
            del_list.append(key)
        for key in del_list:
            del storage._FileStorage__objects[key]

    def tearDown(self):
        """ Remove storage file at end of tests """
        try:
            os.remove('file.json')
        except FileNotFoundError:
            pass

    def test_obj_list_empty(self):
        """ __objects is initially empty """
        self.assertEqual(len(storage.all()), 0)

    def test_new(self):
        """ New object is correctly added to __objects """
        obj = BaseModel()
        obj_key = type(obj).__name__ + "." + obj.id
        storage.new(obj)
        self.assertIn(obj_key, storage.all())

    def test_all(self):
        """ __objects is properly returned """
        new_base = BaseModel()
        temp = storage.all()
        self.assertIsInstance(temp, dict)

    def test_all_cls(self):
        """ Test all method but passing in instance """
        new_state = State()
        storage.new(new_state)
        classname: str = new_state.__class__.__name__
        key = f"{classname}.{new_state.id}"
        self.assertIn(key, storage.all(State).keys())

    def test_base_model_instantiation(self):
        """ File is not created on BaseModel save """
        new = BaseModel()
        self.assertFalse(os.path.exists('file.json'))

    def test_empty(self):
        """ Data is saved to file """
        new = BaseModel()
        new.save()
        self.assertNotEqual(os.path.getsize('file.json'), 0)

    def test_save(self):
        """ FileStorage save method """
        new = BaseModel()
        storage.save()
        self.assertTrue(os.path.exists('file.json'))

    def test_reload(self):
        """ Storage file is successfully loaded to __objects """
        new = BaseModel()
        BaseModel.save(new)
        storage.reload()
        self.assertEqual(new.to_dict(),
                         list(storage.all(BaseModel).values())[0].to_dict())

    def test_reload_empty(self):
        """ Load from an empty file """
        with open('file.json', 'w') as f:
            pass
        with self.assertRaises(ValueError):
            storage.reload()

    def test_reload_from_nonexistent(self):
        """ Nothing happens if file does not exist """
        self.assertEqual(storage.reload(), None)

    def test_base_model_save(self):
        """ BaseModel save method calls storage save """
        new = BaseModel()
        new.save()
        self.assertTrue(os.path.exists('file.json'))

    def test_type_path(self):
        """ Confirm __file_path is string """
        self.assertEqual(type(storage._FileStorage__file_path), str)

    def test_type_objects(self):
        """ Confirm __objects is a dict """
        self.assertEqual(type(storage.all()), dict)

    def test_key_format(self):
        """ Key is properly formatted """
        new = BaseModel()
        _id = new.to_dict()['id']
        new.save()
        self.assertIn('BaseModel' + '.' + _id,
                      storage.all())

    def test_storage_var_created(self):
        """ FileStorage object storage created """
        from models.engine.file_storage import FileStorage
        self.assertEqual(type(storage), FileStorage)

    def test_del(self):
        """ Test delete method for FileStorage object """
        accra = State()
        tema = State()
        accra.save(), tema.save()
        self.assertEqual(len(storage.all(State).keys()), 2)
        storage.delete(tema)
        self.assertEqual(len(storage.all(State).keys()), 1)
