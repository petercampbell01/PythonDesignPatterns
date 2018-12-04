import unittest
import controller


__author__ = "Peter Campbell"
__copyright__ = "Copyright 2018,BCPR301 Class Assignment 3"
__credits__ = []
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Peter Campbell"
__email__ = "peter@intrepid-adventure.com"
__status__ = "Development"


class MainTests(unittest.TestCase):


    def test_01_controller_runparser(self):
        cont = controller.Controller()
        expected = dict
        actual = type(cont.run_parser(['plants.py']))
        self.assertEqual(expected, actual)

    def test_02_controller_runparser(self):
        cont = controller.Controller()
        expected = dict
        actual = type(cont.run_parser(['plants.py', 'linkedlist.py']))
        self.assertEqual(expected, actual)

    def test_03_controller_create_uml(self):
        cont = controller.Controller()
        expected = True
        actual = cont.create_class_diagram(['plants.py'])
        self.assertEqual(expected, actual)

    def test_04_controller_create_uml(self):
        cont = controller.Controller()
        expected = True
        actual = cont.create_class_diagram(['plants.py', 'linkedlist.py'])
        self.assertEqual(expected, actual)

    def test_05_controller_create_uml(self):
        # Pass non python file to generate an image.
        # Result should lead to empty image being generated.
        # Return should be True
        cont = controller.Controller()
        expected = True
        actual = cont.load_csv_for_uml(['plants.csv'])
        self.assertEqual(expected, actual)

    def test_06_controller_create_csv(self):
        cont = controller.Controller()
        filename = 'plants.py'
        expected = True
        actual = cont.create_csv(filename, 'test_output_plants.csv')
        self.assertEqual(expected, actual)

    def test_07_controller_create_csv(self):
        cont = controller.Controller()
        filename = 'doesnotexist.py'
        expected = False
        actual = cont.create_csv(filename, 'test_output_plants.csv')
        self.assertEqual(expected, actual)

    def test_08_controller_load_csv_for_uml(self):
        cont = controller.Controller()
        expected = False
        actual = cont.load_csv_for_uml('plants.py')
        self.assertEqual(expected, actual)

    def test_09_controller_load_csv_for_uml(self):
        cont = controller.Controller()
        expected = True
        actual = cont.load_csv_for_uml('plants.csv')
        self.assertEqual(expected, actual)

    def test_10_controller_validate_code(self):
        cont = controller.Controller()
        expected = 1
        actual = len(cont.validate_code(['linkedlist.py']))
        self.assertEqual(expected, actual)

    def test_11_controller_validate_code(self):
        cont = controller.Controller()
        expected = 2
        actual = len(cont.validate_code(['linkedlist.py', 'plants.py']))
        self.assertEqual(expected, actual)

    def test_12_controller_validate_code(self):
        cont = controller.Controller()
        expected = 1
        actual = len(cont.validate_code(['linkedlist.py', 'plants.foo']))
        self.assertEqual(expected, actual)

    def test_13_controller_pickle(self):
        cont = controller.Controller()
        expected = True
        actual = cont.pickle_modules()
        self.assertEqual(expected, actual)

    def test_14_controller_pickle(self):
        cont = controller.Controller()
        expected = True
        actual = cont.pickle_modules('linkedlist.py')
        self.assertEqual(expected, actual)

    def test_15_controller_pickle(self):
        cont = controller.Controller()
        expected = True
        actual = cont.pickle_modules('linkedlist.py')
        self.assertEqual(expected, actual)

    def test_16_controller_load_pickle(self):
        cont = controller.Controller()
        expected = dict
        actual = type(cont.load_pickle())
        self.assertEqual(expected, actual)

    def test_17_controller_module_to_uml(self):
        cont = controller.Controller()
        expected = False
        try:
            actual = cont.module_to_uml()
        except:
            actual = False
        self.assertEqual(expected, actual)

    def test_18_controller_pickle_to_uml(self):
        cont = controller.Controller()
        expected = True
        actual = cont.pickle_to_uml()
        self.assertEqual(expected, actual)

    def test_19_controller_module_to_uml(self):
        cont = controller.Controller()
        expected = True
        actual = cont.module_to_uml(cont.run_parser(['linkedlist.py']))
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main(verbosity=2)
