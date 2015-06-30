import unittest
from pytraj.base import *
from pytraj import io as mdio
from pytraj.datasets import *
from pytraj.utils.check_and_assert import assert_almost_equal


class Test(unittest.TestCase):

    def test_0(self):
        traj = mdio.iterload("./data/md1_prod.Tc5b.x", "./data/Tc5b.top")
        ds = DatasetFloat()
        print(ds.dtype)

if __name__ == "__main__":
    unittest.main()
