import numpy as np
import hypers as hp
from typing import Optional
import matplotlib.pyplot as plt


def _data_plotting(X: 'hp.Dataset',
                   kind: str,
                   target: str,
                   figsize: Optional[tuple]):

    if kind not in ('both', 'im', 'spec'):
        raise TypeError('kind must be assigned to both, im or spec')

    if target not in ('data', 'cluster', 'decompose', 'scree'):
        raise TypeError('target must be assigned to data, cluster, decompose or scree')

    if target == 'data':
        pass
