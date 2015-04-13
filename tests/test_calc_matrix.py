from __future__ import print_function
import unittest
from pytraj.base import *
from pytraj import adict
from pytraj import io as mdio
from pytraj.utils.check_and_assert import assert_almost_equal
from pytraj.decorators import no_test, test_if_having
from pytraj.utils.check_and_assert import is_word_in_class_name
from pytraj.utils import has_

class Test(unittest.TestCase):
    def test_0(self):
        from pytraj.common_actions import calc_matrix
        traj = mdio.load("./data/md1_prod.Tc5b.x", "./data/Tc5b.top")
        d0 = calc_matrix("@CA", traj)
        print (d0)
        assert is_word_in_class_name(d0, 'DataSetList') == True
        print (d0.get_legends())

        if has_("pandas"):
            from pytraj.dataframe import to_dataframe
            print (to_dataframe(d0))

if __name__ == "__main__":
    unittest.main()