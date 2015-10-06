"""perform nucleic acid analysis
"""
from __future__ import absolute_import
import numpy as np
from ._base_result_class import BaseAnalysisResult
from .externals.six import string_types
from ._get_common_objects import _get_topology, _get_data_from_dtype, _get_resrange
from ._get_common_objects import _get_reference_from_traj, _get_fiterator
from pytraj.externals.six import iteritems

def _group(self, key):
    # adapted from `toolz` package.
    # see license in $PYTRAJHOME/licenses/externals/toolz.txt
    import collections
    if not callable(key):
        key = getter(key)
    #d = collections.defaultdict(lambda: self.__class__().append)
    d = collections.defaultdict(lambda: [].append)
    for item in self:
        d[key(item)](item)
    rv = {}
    for k, v in iteritems(d):
        rv[k] = v.__self__
    return rv


def nastruct(traj=None,
             ref=0,
             resrange=None,
             resmap=None,
             hbcut=3.5,
             frame_indices=None,
             pucker_method='altona',
             top=None):
    """compute nucleic acid parameters. (adapted from cpptraj doc)

    Parameters
    ----------
    traj : Trajectory-like
    ref : {Frame, int}, default 0 (first frame)
    resrange : None, str or array-like of integers
    resmap : residue map, example: 'AF2:A'
    hbcut : float, default=3.5 Angstrong
        Distance cutoff for determining basepair hbond
    pucker_method : str, {'altona', 'cremer'}, default 'altona'
        'altona' : Use method of Altona & Sundaralingam to calculate sugar pucker
        'cremer' : Use method of Cremer and Pople to calculate sugar pucker'
    frame_indices : array-like, default None (all frames)

    Returns
    -------
    out : nupars object. One can assess different values (major groove width, xdips values
    ...) by accessing its attribute. See example below.

    Examples
    --------
    >>> import pytraj as pt
    >>> import numpy as np
    >>> data = pt.nastruct(traj)
    >>> data.keys()[:5]
    ['buckle', 'minor', 'major', 'xdisp', 'stagger']
    >>> # get minor groove width values for each pairs for each snapshot
    >>> # data.minor is a tuple, first value is a list of basepairs, seconda value is
    >>> # numpy array, shape=(n_frames, n_pairs)

    >>> data.minor
    (['1G16C', '2G15C', '3G14C', '4C13G', '5G12C', '6C11G', '7C10G', '8C9G'], 
     array([[ 13.32927036,  13.403409  ,  13.57159901, ...,  13.26655865,
             13.43054485,  13.4557209 ],
           [ 13.32002068,  13.45918751,  13.63253593, ...,  13.27066231,
             13.42743683,  13.53450871],
           [ 13.34087658,  13.53778553,  13.57062435, ...,  13.29017353,
             13.38542843,  13.46101475]]))

    >>> data.twist
    (['1G16C-2G15C', '2G15C-3G14C', '3G14C-4C13G', '4C13G-5G12C', '5G12C-6C11G', '6C11G-7C10G', '7C10G-8C9G'], 
    array([[ 34.77773666,  33.98158646,  30.18647003, ...,  35.14608765,
             33.9628334 ,  33.13056946],
           [ 33.39176178,  32.68476105,  28.36385536, ...,  36.59774399,
             30.20827484,  26.48732948],
           [ 36.20665359,  32.58955002,  27.47707367, ...,  33.42843246,
             30.90047073,  33.73724365]]))
    """
    from pytraj.datasets.DatasetList import DatasetList as CpptrajDatasetList
    from .actions.CpptrajActions import Action_NAstruct
    from pytraj.array import DataArray

    _resrange = _get_resrange(resrange)

    fi = _get_fiterator(traj, frame_indices)
    _ref = _get_reference_from_traj(traj, ref)
    _top = _get_topology(traj, top)
    _resmap = "resmap " + resmap if resmap is not None else ""
    _hbcut = "hbcut " + str(hbcut) if hbcut is not None else ""
    _pucker_method = pucker_method

    command = " ".join((_resrange, _resmap, _hbcut, _pucker_method))

    act = Action_NAstruct()
    dslist = CpptrajDatasetList()

    act(command, [_ref, fi], dslist=dslist, top=_top)

    dslist_py = []
    for d in dslist:
        dslist_py.append(DataArray(d))
        dslist_py[-1].values = dslist_py[-1].values[1:]
    return nupars(_group(dslist_py, lambda x : x.aspect))


class nupars(object):
    '''class holding data for nucleic acid.
    '''
  
    def __init__(self, adict):
        self._dict = adict

    def __str__(self):
        return '<nupars, keys = %s>' % str(self.keys())

    def __repr__(self):
        return str(self)

    def __getitem__(self, key):
        '''self['minor'], ...
        '''
        return self.__getattr__(key)

    def __getattr__(self, aspect):
        '''self.minor, ...
        '''
        # data is a list of DataArray
        data = self._dict[aspect]
        arr = np.empty((len(data), len(data[0])), dtype='f8')

        keylist = []
        for idx, arr0 in enumerate(data):
            keylist.append(arr0.key)
            arr[idx] = arr0.values
        return keylist, arr.T

    def keys(self):
        return list(self._dict)

    def __dir__(self):
        '''for autocompletion in ipython
        '''
        return self.keys() + ['_summary',]

    def _summary(self, ops, keys=None, indices=None):
        '''
        Parameters
        op : numpy method
        keys: optional
        indices : optional

        Examples
        --------
        self._summary(np.mean, indices=range(2, 8))
        '''
        _keys = keys if keys is not None else self.keys()

        sumlist = []
        ops = [ops, ] if not isinstance(ops, (list, tuple)) else ops

        for op in ops: 
            sumdict = {}
            for k in _keys:
                values = self[k][1]
                if indices is None:
                    sumdict[k] = op(values, axis=1)
                else:
                    sumdict[k] = op(values[indices], axis=1)
            sumlist.append(sumdict)
        if len(ops) == 1:
            return sumlist[0]
        else:
            return sumlist

    def _explain(self):
        '''copied from cpptraj doc
        '''
        return '''
        [shear] Base pair shear.
        [stretch] Base pair stretch.
        [stagger] Base pair stagger.
        [buckle] Base pair buckle.
        [prop] Base pair propeller.
        [open] Base pair opening.
        [hb] Number of hydrogen bonds between bases in base pair.
        [pucker] Base sugar pucker.
        [major] Rough estimate of major groove width, calculated between P atoms of each
        base.
        [minor] Rough estimate of minor groove width, calculated between O4 atoms of
        each base.
        [shift] Base pair step shift.
        [slide] Base pair step slide.
        [rise] Base pair step rise.
        [title] Base pair step tilt.
        [roll] Base pair step roll.
        [twist] Base pair step twist.
        [xdisp] Helical X displacement.
        [ydisp] Helical Y displacement.
        [hrise] Helical rise.
        [incl] Helical inclination.
        [tip] Helical tip.
        [htwist] Helical twist.
        '''

    def __setstate__(self, state):
        self._dict = state

    def __getstate__(self):
        return self._dict