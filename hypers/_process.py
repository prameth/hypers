"""
Stores data in a custom class and generates attributes for other modules
"""
import numpy as np
from typing import Tuple, Union

from hypers._preprocessing import _data_preprocessing, _data_scale, _data_whiten
from hypers._learning import _data_cluster, _vca, _ucls, _data_decomposition, _data_scree
from hypers._tools import _data_smoothen, _data_mean, _data_checks, _data_access
from hypers._tools import PreprocessType, ClusterType, DecomposeType
from hypers._view import hsiPlot


class Dataset:
    def __init__(self, data: np.ndarray,
                 scale: bool = True) -> None:
        self.data = data
        self.scale = scale

        # Data properties
        self.shape = None
        self.ndim = None
        self.n_features = None
        self.n_samples = None
        self.smoothing = 'savitzky_golay'

        # Hyperspectral image/spectrum
        self.image = None
        self.spectrum = None
        self.mean_image = None
        self.mean_spectrum = None

        # sklearn
        self.mdl_preprocess = None
        self.mdl_decompose = None
        self.mdl_cluster = None
        self.mdl_mixture = None

        self.update()

    def __getitem__(self, key: tuple) -> np.ndarray:
        return self.data[key]

    def __setitem__(self, key: tuple, value: Union[int, float, np.ndarray]) -> None:
        self.data[key] = value
        self.update()

    def __truediv__(self, var: Union[int, float, np.ndarray]) -> 'Dataset':
        if type(var) in (int, float):
            for _val in np.ndenumerate(self.data):
                self.data[_val[0]] /= var

        elif type(var) == np.ndarray and var.ndim == 1 and var.shape[0] == self.shape[-1]:
            for _val in np.ndindex(self.shape[:-1]):
                self.data[_val] /= var

        else:
            raise TypeError('Can only divide by an integer, float or spectral array')

        self.update()
        return self

    def __mul__(self, var: Union[int, float, np.ndarray]) -> 'Dataset':
        if type(var) in (int, float):
            for _val in np.ndenumerate(self.data):
                self.data[_val[0]] *= var

        elif type(var) == np.ndarray and var.ndim == 1 and var.shape[0] == self.shape[-1]:
            for _val in np.ndindex(self.shape[:-1]):
                self.data[_val] *= var

        else:
            raise TypeError('Can only multiply by an integer, float or spectral array')

        self.update()
        return self

    def __add__(self, var: Union[int, float, np.ndarray]) -> 'Dataset':
        if type(var) in (int, float):
            for _val in np.ndenumerate(self.data):
                self.data[_val[0]] += var

        elif type(var) == np.ndarray and var.ndim == 1 and var.shape[0] == self.shape[-1]:
            for _val in np.ndindex(self.shape[:-1]):
                self.data[_val] += var

        else:
            raise TypeError('Can only add with an integer, float or spectral array')

        self.update()
        return self

    def __sub__(self, var: Union[int, float, np.ndarray]) -> 'Dataset':
        if type(var) in (int, float):
            for _val in np.ndenumerate(self.data):
                self.data[_val[0]] -= var

        elif type(var) == np.ndarray and var.ndim == 1 and var.shape[0] == self.shape[-1]:
            for _val in np.ndindex(self.shape[:-1]):
                self.data[_val] -= var

        else:
            raise TypeError('Can only subtract by an integer, float or spectral array')

        self.update()
        return self

    def update(self) -> None:
        _data_checks(self)
        if self.scale:
            _data_scale(self)
        _data_mean(self)
        _data_access(self)

    def view(self) -> None:
        hsiPlot(self)

    def smoothen(self, **kwargs) -> None:
        _data_smoothen(self, **kwargs)
        self.update()

    def flatten(self) -> np.ndarray:
        return np.reshape(self.data, (np.prod(self.shape[:-1]), self.shape[-1]))

    def scree(self, plot: bool = False,
              return_arrs: bool = True) -> np.ndarray:
        return _data_scree(self, plot=plot, return_arrs=return_arrs)

    def preprocess(self, mdl: PreprocessType) -> None:

        _data_preprocessing(self, mdl)

    def decompose(self, mdl: DecomposeType,
                  plot: bool = False,
                  return_arrs: bool = True) -> Tuple[np.ndarray, np.ndarray]:

        return _data_decomposition(self, mdl, return_arrs=return_arrs, plot=plot)

    def cluster(self, mdl: ClusterType,
                decomposed: bool = False,
                pca_comps: int = 4,
                plot: bool = False,
                return_arrs: bool = True) -> Tuple[np.ndarray, np.ndarray]:

        return _data_cluster(self, mdl, decomposed=decomposed, pca_comps=pca_comps, plot=plot, return_arrs=return_arrs)

