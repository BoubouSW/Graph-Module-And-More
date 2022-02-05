from traceback import print_tb
from modules.open_digraph import *
import unittest
import sys
import os

root = os.path.normpath(os.path.join(__file__, "./../.."))
sys.path.append(root)  # allows us

from tests.open_digraph_test import *
from tests.matrice_test import *

if __name__ == "__main__":  # the following code is called only when
    unittest.main()  # precisely this file is run0, node)
