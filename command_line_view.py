#!/usr/bin/python
# -*- coding: utf-8 -*-
import interactive_shell

__author__ = 'Peter Campbell'
__copyright__ = 'Copyright 2018,BCPR301 Class Assignment 3'
__credits__ = []
__license__ = 'GPL'
__version__ = '1.0.1'
__maintainer__ = 'Peter Campbell'
__email__ = 'peter@intrepid-adventure.com'
__status__ = 'Development'


class CommandLine(object):

    def __init__(self):
        pass

    def set_controller(self, controller):
        self.command = controller

        # print(f"Controller is set: {controller}")

    def get_command(self, args):
        pass

    def analyse_input(self, args):
        self.comm = None  # command given by user
        self.input_file = None

        # print(f'args {args}')
        # print(f'length: {len(args)}')

        if len(args) == 1:
            print ('For help using the command line write: command_interpreter.py -help')
            interactive_shell.InteractiveShell(self)
        else:
            self.output_file = 'output.csv'
            self.check_command_line(args)
            self.run_command()

    def check_command_line(self, args):
        '''
        command_line [command] -i [input] -o [output]
        '''

        # print(args)

        self.comm = args[1]

        # print('command', self.comm)

        index = 0
        for arg in args:
            if arg == '-i':
                self.input_file = args[index + 1]
            elif arg == '-o':
                self.output_file = args[index + 1]
            index += 1

    def run_command(self):
        """
        Commands:
        help, file-uml, to-csv, csv-uml, pickle, pickle-uml, validate
        """

        if self.comm == '-help' or self.comm == 'help' or self.comm \
            == '-h':
            self.help()
        elif self.comm == 'file-uml':

        # elif self.input_file is None:
        #    print("No input file specified")
        #    exit()

            self.create_uml()
        elif self.comm == 'to-csv':
            params = self.input_file + ' ' + self.output_file
            self.create_csv(params)
        elif self.comm == 'csv-uml':
            self.load_csv_for_uml(self.input_file)
        elif self.comm == 'pickle':
            self.pickle_module(self.input_file)
        elif self.comm == 'pickle-uml':
            self.pickle_to_uml()
        elif self.comm == 'validate':
            self.validate_code(self.input_file)

    def help(self, filename='help.txt'):
        try:
            with open(filename) as helpfile:
                for line in helpfile:
                    print(line.replace('\n', ''))
            return True
        except FileNotFoundError:
            print('Requested helpfile could not be found')
            return False
        except:
            print('Could not find any help.')
            return False

    def create_uml(self):
        if self.command.create_class_diagram(self.input_file) is False:
            print('Could not generate UML diagram')
        else:
            print('UML diagram successfully created')

    def create_csv(self, params):
        infiles = []
        args = params.split(' ')
        if len(args) >= 1:
            infiles.append(args[0])
            outfile = 'output.csv'
        if len(args) >= 2:
            outfile = args[1]
        if infiles[0].endswith('.py'):
            if self.command.create_csv(infiles, outfile) is True:
                print('{} successfully created saved as {}'.format(infiles,
                        outfile))
                return True
            else:
                return False
        else:
            return False

    def load_csv_for_uml(self, file='output.csv'):
        if self.command.load_csv_for_uml(file) is True:
            print('UML class diagram successfully created from {}'.format(file))
        else:
            print('UML class diagram could not be created from {}'.format(file))

    def validate_code(self, filenames):
        print('Validating code ...')
        files = []
        if type(filenames) == str:
            files.append(filenames)
        elif type(filenames) == list:
            files = filenames
        valid_files = self.command.validate_code(files)
        if valid_files is not False:
            print('The following files have been validated: {}'.format(valid_files))
            return True
        else:
            print('Unable to validate files: {}'.format(files))

    def pickle_module(self, filename):
        if self.command.pickle_modules(filename) is True:
            print('{} successfully pickled'.format(filename))
            return True
        else:
            print('Unable to pickle {}'.format(filename))
            return False

    def pickle_to_uml(self):
        if self.command.pickle_to_uml() is True:
            print('UML successfully created from pickle')
        else:
            print('Was unable to create UML from pickle, have you pickled anything lately?')
