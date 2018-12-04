from abc import ABCMeta, abstractmethod
import os
import pickle

__author__ = "Peter Campbell"
__copyright__ = "Copyright 2018,BCPR301 Class Assignment 3"
__credits__ = []
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Peter Campbell"
__email__ = "peter@intrepid-adventure.com"
__status__ = "Development"

class OutputMaker(object):

    def __init__(self, output_type):
        self.output_type = output_type

    def make_output(self, modules, output_file = None):
        return self.output_type.generate_output(modules, output_file)


class AbstractOutputType(metaclass=ABCMeta):

    @abstractmethod
    def generate_output(self, module, output_file):
        pass


class CSVOutput(AbstractOutputType):

    def generate_output(self, modules, output_file='output.csv'):
        # Writes module as received from model or from self.open_file
        # to specified csv file.
        output = ''
        for (name, module) in modules.items():
            output += 'module,{}\n'.format(name)
            for c in module:
                output += 'class,{}'.format(c.name)
                if len(c.attributes) > 0:
                    output += '\nattributes'
                for attr in c.attributes:
                    output += ',{}'.format(attr.name)
                if len(c.functions) > 0:
                    output += '\nmethods'
                for func in c.functions:
                    output += ',{}'.format(func.name)
                if c.super_classes is not None:
                    if len(c.super_classes) > 0:
                        output += '\nsuper_classes'
                        for super_class in c.super_classes:
                            output += ',{}'.format(super_class)
                output += '\n'
        try:
            with open(output_file, "wt") as f:
                f.write(output)
            return True
        except IOError:
            print("Cannot write csv file. Try again another day")
            return False
        except PermissionError:
            print('You do not have appropriate permissions on '
                  'this system to save the file')
            return False
        except:
            print('The system encountered a problem here. '
                  'Please turn off your computer,')
            print('jump up and down three times, flap your arms '
                  'and quack like a duck and then try again.')
            return False


class UMLOutput(AbstractOutputType):

    def generate_output(self, modules, output_file = None):
        self.hide_attributes = False
        self.hide_methods = False
        full_path = os.path.realpath(__file__)
        path, filename = os.path.split(full_path)
        path = path.replace("\\", "/")

        # create tmp folder if doesn't exist
        if not os.path.exists(path + '/tmp'):
            os.makedirs(path + '/tmp')

        try:
            with open(path + '/tmp/class.dot', 'w') as out:
                # Output as UML class diagram using DOT (graphviz)
                def line(s):
                    return out.write(s + "\n")

                def class_name_to_dot(name):
                    return name

                # creates row in table with method name
                def write_row(out, method):
                    out.write(method + "\l")

                # styles class table and items for output
                out.write(
                    """
                    digraph G {
                        rankdir=BT
                        node [
                            fontname = "Sans Not-Rotated 8"
                            fontsize = 8
                            shape = "record"
                        ]
                        edge [
                            fontname = "Sans Not-Rotated 8"
                            fontsize = 8
                        ]
                    """
                )
                for (name, module) in modules.items():
                    if len(module) > 1:
                        line("subgraph {")

                    for c in module:
                        line(class_name_to_dot(c.name) + " [")

                        # Class Title
                        out.write("label = \"{" + c.name)

                        out.write("|")

                        # Attributes Start
                        #if not self.hide_attributes:
                        for attr in c.attributes:
                            write_row(out,  attr.name)
                        # Attributes End
                        out.write("|")
                        # Functions Start
                        # if not self.hide_methods:
                        for func in c.functions:
                            write_row(out, func.name + "(" + func.get_parameters() +")")

                        # Functions End

                        out.write("}\"\n")

                        line("]")

                    if len(module) > 1:
                        line("}")

                out.write("""
                    edge [
                        arrowhead = "empty"
                    ]
                """)

                # draws lines between class boxes
                for module in modules.values():
                    for c in module:
                        if c.super_classes != None:
                            for parent in c.super_classes:
                                line(class_name_to_dot(c.name) + " -> " +
                                    class_name_to_dot(parent.__name__))

                line("}")

                return True
        except OSError:
            print("tmp folder failed to exist, if it has not automatically "
                  "been created in project directory then please create")
            return False
        except TypeError:
            print("A type error has occurred. Please try this operation later")
            return False

class PickleOutput(AbstractOutputType):

    def generate_output(self, modules, output_file='output.csv'):
        try:
            with open('data.pickle', 'wb') as f:
                pickle.dump(modules, f)
            return True
        except:
            return False

