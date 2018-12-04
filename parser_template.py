from abc import ABCMeta, abstractmethod
import inspect
import sys
import os
import csv
import model


__author__ = "Peter Campbell"
__copyright__ = "Copyright 2018,BCPR301 Class Assignment 3"
__credits__ = []
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Peter Campbell"
__email__ = "peter@intrepid-adventure.com"
__status__ = "Development"


class ParserTemplate(metaclass=ABCMeta):

    def __init__(self, file_name):
        self.modules = dict()
        if type(file_name) is not list:
            file_name = [file_name]
        self.file_name = file_name

    def parser_algorithm(self):
        if self.check_files_exists() is False:
            return False
        if self.process_files(self.file_name) is False:
            return False
        return self.get_modules()

    def check_files_exists(self):
        for file in self.file_name:
            if os.path.isfile(file) is False:
                return False
        return True

    @abstractmethod
    def process_files(self):
        pass

    @abstractmethod
    def process_module(self, module):
        pass

    @abstractmethod
    def process_function(self):
        pass

    @abstractmethod
    def process_attribute(self):
        pass

    def get_modules(self):
        return self.modules


class PythonModuleParser(ParserTemplate):

    filter_out_attributes = ["__doc__", "__module__",
                             "__dict__", "__weakref__"]

    def process_files(self, file_names):
        """
        Loop through a list of files, and process each file as an individual
        Author: Braeden

        >>> fp.process_files(["plants.py"])
        1
        >>> fp.process_files(["plants.py", "plants2.py"])
        2
        """
        for file in file_names:
            self.process_file(file)
        return len(self.modules)

    def process_file(self, file_name):
        # Import specified file_name and store as module
        path, file = os.path.split(file_name)
        module_name = file.replace("./", "").replace(".py", "")\
            .replace("/", ".")

        # change path for import to directory of file
        sys.path.append(path)

        try:
            __import__(module_name, locals(), globals())
            self.process_module(sys.modules[module_name])
        except ImportError:
            print("A file with this name could not be found, "
                  "please try again.")
        except OSError:
            print("The provided python file contains invalid syntax,"
                  " please fix the provided code before running")

    def process_module(self, module):
        # Find any classes that exists within this module
        for (name, something) in inspect.getmembers(module):
            if inspect.isclass(something):
                self.process_class(something)

    def process_class(self, some_class):
        # Process the found class, and store in global modules
        # Find any functions with-in the class
        name = some_class.__name__

        module_name = some_class.__module__

        # create module for current file in global modules list
        if module_name not in self.modules:
            self.modules[module_name] = list()

        super_classes = []
        super_classes_names = []

        # Only creates class_nodes that have unique name,
        # stops duplicate class_nodes
        # Strips any random objects, only leaves proper class names
        for class_object in some_class.__bases__:
            if class_object.__name__ != 'object':
                if class_object.__name__ not in super_classes_names:
                    super_classes.append(class_object)
                    super_classes_names.append(class_object.__name__)

        # create class node and append to current module
        class_node = model.ClassNode(name, super_classes)
        self.modules[module_name].append(class_node)

        # create list of functions in class
        for (name, something) in inspect.getmembers(some_class):
            if inspect.ismethod(something) or inspect.isfunction(something):
                # get the class from the functions element
                function_class = something.__qualname__.split('.')[0]

                # only add function if the current class is the same as the
                # selected functions class
                if some_class.__name__ == function_class:
                    # create list of attributes in class with constructor
                    if something.__name__ == "__init__":
                        attributes = something.__code__.co_names

                        for attribute in attributes:
                            self.process_attribute(attribute, class_node,
                                                   self.get_visibility_of_string
                                                   (attribute))

                    self.process_function(something, class_node,
                                          self.get_visibility_of_string
                                          (something.__name__))

    def process_function(self, some_function, class_node, visibility):
        # Functions are added to the class node with just their title
        class_node.add_function(some_function.__name__,
                                inspect.getfullargspec(some_function)[0],
                                visibility)

    def process_attribute(self, attribute_name, class_node, visibility):
        # Attributes are added to the class node with just their name
        # filter out __module__, __doc__
        if attribute_name not in self.filter_out_attributes:
            class_node.add_attribute(attribute_name, visibility)

    def get_visibility_of_string(self, string):
        # get visibility of function (public = +, protected = #, private = -)
        visibility = "+"
        if string[:2] == "__":
            visibility = "-"
        elif string[0] == "_":
            visibility = "#"
        return visibility


class CSVParser(ParserTemplate):

    def process_files(self, input_files):
        for file_name in input_files:
            return self.process_file(file_name)

    def process_file(self, file_name = 'input.csv'):
        # Opens csv file and loads each line of the file into list
        # Then process_module for parsing
        result = []
        try:
            with open(file_name) as File:
                reader = csv.reader(File)
                for row in reader:
                    result.append(row)
            return self.process_module(result)
        except FileNotFoundError:
            print('File cannot be found. Please check path and '
                  'file name or check that file exists')
            return False
        except:
            print('An error has occurred. Could not load '
                  'information from csv file.')
            return False

    def process_module(self, module_list):

        module_name = ''
        newClass = None
        for aline in module_list:
            if aline[0] == 'module':
                module_name = aline[1]
                self.modules[module_name] = list()
            elif aline[0] == 'class':
                if newClass is None:
                    newClass = model.ClassNode(aline[1].strip())
                else:
                    self.modules[module_name].append(newClass)
                    newClass = model.ClassNode(aline[1].strip())
            elif aline[0] == 'attributes':
                loop_counter = 1
                while loop_counter < len(aline):
                    newClass.add_attribute(aline[loop_counter].strip(), False)
                    loop_counter += 1
            elif aline[0] == 'methods':
                loop_counter = 1
                while loop_counter < len(aline):
                    newClass.add_function(aline[loop_counter].strip(),
                                          'params', False)
                    loop_counter += 1
            elif aline[0] == 'super_classes':
                pass
        self.modules[module_name].append(newClass)
        return self.modules

    def process_function(self):
        pass

    def process_attribute(self):
        pass
