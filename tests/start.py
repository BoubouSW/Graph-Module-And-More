import unittest
import sys
import os

root = os.path.normpath(os.path.join(__file__, "./../.."))
sys.path.append(root)

from tests.open_digraph_test import *
from tests.matrice_test import *

if __name__ == "__main__":
    unittest.main()
