
import unittest
from time import time
from pytraj.base import *
from pytraj import allactions
from pytraj import io as mdio
from pytraj import adict

class TestActionList(unittest.TestCase):
    def test_run_0(self):
        # load traj
        traj = mdio.load("./data/md1_prod.Tc5b.x", "./data/Tc5b.top")
        dslist = DataSetList()
        dflist = DataFileList()
    
        # creat ActionList to hold actions
        alist = ActionList()
        # add two actions: Action_Dihedral and Action_Distance
        alist.add_action(adict['distance'], ":2@CA :10@CA out ./output/_dist.out", 
                         traj.top, dslist, dflist)
        alist.add_action(adict['dihedral'], ":2@CA :3@CA :4@CA :5@CA out ./output/_dih.out", 
                         traj.top, dslist, dflist)

        # using string for action 'dssp'
        alist.add_action('dssp', "out ./output/_dssp_alist.out", 
                         traj.top, dslist, dflist)
        alist.add_action('matrix', "out ./output/_mat_alist.out", 
                         traj.top, dslist, dflist)
        alist.do_actions((traj, traj))
        alist.do_actions((traj[0], traj[1], traj))
        dflist.write_all_datafiles()
        print (dslist.size)
        print (dslist[0][:])
        print (dslist[1][:])
        print (dslist.get_dataset(dtype='integer'))

if __name__ == "__main__":
    unittest.main()
