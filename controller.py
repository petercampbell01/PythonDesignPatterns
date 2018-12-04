#!/usr/bin/python
# -*- coding: utf-8 -*-
import python_code_validator as validator
import pickle_modules
import output_strategy
import parser_template as parser

__author__ = 'Peter Campbell'
__copyright__ = 'Copyright 2018,BCPR301 Class Assignment 3'
__credits__ = []
__license__ = 'GPL'
__version__ = '1.0.1'
__maintainer__ = 'Peter Campbell'
__email__ = 'peter@intrepid-adventure.com'
__status__ = 'Development'


class Controller(object):

    def set_view(self, view):
        self.view = view

    def do_stuff(self, args):
        self.view.analyse_input(args)

    def run_parser(self, input_file):
        processor = parser.PythonModuleParser(input_file)
        self.extracted_modules = processor.parser_algorithm()
        return self.extracted_modules

    def create_class_diagram(self, filenames):
        if type(filenames) != list:
            filenames = [filenames]
        modules = self.run_parser(filenames)
        if modules is not False:
            uml_output = output_strategy.UMLOutput()
            output_maker = output_strategy.OutputMaker(uml_output)
            return output_maker.make_output(modules)
        return False

    def create_csv(self, in_filename, out_file='class_data.csv'):
        if type(in_filename) != list:
            in_filename = [in_filename]
        modules = self.run_parser(in_filename)
        if modules is not False:
            csv_output = output_strategy.CSVOutput()
            output_maker = output_strategy.OutputMaker(csv_output)
            return output_maker.make_output(modules, out_file)
        else:
            return False

    def load_csv_for_uml(self, input_file='class_data.csv'):
        if type(input_file) is not list:
            input_file = [input_file]
        parse_csv = parser.CSVParser(input_file)
        module = parse_csv.parser_algorithm()

        if module is not False:
            uml_output = output_strategy.UMLOutput()
            output_maker = output_strategy.OutputMaker(uml_output)
            return output_maker.make_output(module)
        else:
            return False

    def validate_code(self, files):
        validate = validator.CodeValidator()
        return validate.validate_files(files)

    def pickle_modules(self, input_file='plants.py'):
        if type(input_file) is not list:
            input_file = [input_file]
        modules = self.run_parser(input_file)
        pickle_output = output_strategy.PickleOutput()
        output_maker = output_strategy.OutputMaker(pickle_output)
        return output_maker.make_output(modules)

    def load_pickle(self):
        pickler = pickle_modules.PickleModules()
        return pickler.load()

    def module_to_uml(self, module):
        uml_output = output_strategy.UMLOutput()
        output_maker = output_strategy.OutputMaker(uml_output)
        return output_maker.make_output(module)

    def pickle_to_uml(self):
        modules = self.load_pickle()
        if modules is not False:
            uml_output = output_strategy.UMLOutput()
            output_maker = output_strategy.OutputMaker(uml_output)
            return output_maker.make_output(modules)
        else:
            return False
