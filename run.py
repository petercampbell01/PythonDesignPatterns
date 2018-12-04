import command_line_view as CLV
import sys
import controller


__author__ = "Peter Campbell"
__copyright__ = "Copyright 2018,BCPR301 Class Assignment 3"
__credits__ = []
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Peter Campbell"
__email__ = "peter@intrepid-adventure.com"
__status__ = "Development"

if __name__ == '__main__':
    viewer = CLV.CommandLine()
    controller = controller.Controller()
    controller.set_view(viewer)
    viewer.set_controller(controller)
    controller.do_stuff(sys.argv)