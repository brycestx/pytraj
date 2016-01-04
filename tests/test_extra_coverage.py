#!/usr/bin/env python

from __future__ import print_function
import sys
import unittest
import numpy as np
import subprocess
import pytraj as pt
from pytraj.utils import eq, aa_eq
from pytraj.version import version


class TestExtraCoverage(unittest.TestCase):

    def setUp(self):
        self.traj = pt.iterload("./data/tz2.nc", "./data/tz2.parm7")

    def test_extra_coverage(self):
        '''all kind of tests that do not belong to anywhere else
        '''
        traj = pt.iterload("./data/tz2.nc", "./data/tz2.parm7")

        # show_versions
        pt.show_versions()
        pt._verbose()
        pt._verbose(False)
        print(version)

        # info
        pt.info()
        pt.info('parallel')
        pt.misc.parallel_info('pmap')
        pt.misc.parallel_info('openmp')
        pt.misc.parallel_info(None)

        eq([2, 3], [2, 3])
        # raise if comparing NaN
        self.assertRaises(ValueError, lambda: aa_eq(np.nan, np.nan))

        dslist = pt.multidihedral(traj)
        string_ = str(dslist[0])

    def testget_common_objects(self):
        from pytraj.get_common_objects import get_reference_from_traj
        # raises
        # raise if try to index traj()
        self.assertRaises(TypeError, lambda: get_reference_from_traj(self.traj(), 3))
        self.assertRaises(TypeError, lambda: get_reference_from_traj(self.traj(), None))

    def test_all_actions(self):
        from pytraj import all_actions
        self.assertRaises(ValueError, lambda: all_actions._assert_mutable(self.traj))


if __name__ == "__main__":
    unittest.main()