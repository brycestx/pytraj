from __future__ import print_function
import unittest
import pytraj as pt
from pytraj.utils import eq, aa_eq
from pytraj.decorators import no_test, test_if_having, test_if_path_exists
import pytraj.common_actions as pyca

class Test(unittest.TestCase):
    def test_0(self):
        traj = pt.iterload("./data/md1_prod.Tc5b.x", "./data/Tc5b.top")
        dslist = traj.calc_multidihedral("psi", dtype='dataset')
        self.assertRaises(KeyError, lambda : dslist.append(dslist[0]))

if __name__ == "__main__":
    unittest.main()