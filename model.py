#!/usr/bin/python
# -*- coding: utf-8 -*-

##########################################
# Initial helper classes to store information while the parser
# parses the information


class ClassNode:

    """
    Class object containing attributes and functions
    Author: Braeden
    Contributor: Peter

    >>> ClassNode("Class One", []).name
    'Class One'
    >>> class_one = ClassNode("Class One", [])
    >>> class_one.add_attribute("Attribute One")
    >>> class_one.add_attribute("Attribute Two")
    >>> len(class_one.attributes)
    2
    """

    def __init__(self, name, super_classes=None):
        self.name = name
        self.attributes = []
        self.functions = []
        if super_classes is None:
            self.super_classes = []
        else:
            self.super_classes = super_classes

    def add_attribute(self, attribute_name, visibility):
        self.attributes.append(AttributeNode(attribute_name,
                               visibility))

    def add_function(
        self,
        function_name,
        list_of_parameters,
        visibility,
        ):

        self.functions.append(FunctionNode(function_name,
                              list_of_parameters, visibility))

    def add_super_class(self, super_class):
        self.super_classes.append(super_class)

    def get_name(self):
        return self.name


class AttributeNode:

    """
    Attribute object containing attribute name
    Author: Braeden

    >>> AttributeNode("Attribute One").name
    'Attribute One'
    """

    def __init__(self, name, visibility):
        self.name = name
        self.visibility = visibility


class FunctionNode:

    """
    Function object containing function name and parameters
    Author: Braeden

    >>> FunctionNode("Function One", []).get_name()
    'Function One'
    >>> len(FunctionNode("Funct One", ["Par One", "Par Two"]).parameters)
    2
    """

    def __init__(
        self,
        name,
        list_of_parameters,
        visibility,
        ):

        self.name = name
        self.parameters = list_of_parameters
        self.visibility = visibility

    def get_name(self):
        return self.name

    def get_parameters(self):
        return ','.join(self.parameters)


if __name__ == '__main__':
    import doctest
    doctest.testmod(extraglobs={'fp': FileProcessor()})
