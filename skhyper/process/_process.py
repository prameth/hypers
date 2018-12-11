"""
Stores data in a custom class and generates attributes for other modules
"""
import warnings
import numpy as np

from skhyper.process._preprocessing import _data_preprocessing
from skhyper.tools._smoothen import _data_smoothen
from skhyper.learning._cluster import _data_cluster
from skhyper.learning._decomposition import _data_decomposition, _data_scree
from skhyper.view import hsiPlot


class Process:
    """
    Process object to store the hyperspectral array.

    Parameters
    ----------
    X : array, dimensions (3 or 4)
        The hyperspectral data. It should be 3- or 4-dimensional in the form:
            X_3d = [x, y, spectrum] or
            X_4d = [x, y, z, spectrum]

    scale : bool
        Scales the spectra to either between {0, 1} or {-1, 1} depending on presence of negative values.

    normalize : bool
        Normalizes each spectra by subtracting the mean spectrum of the hyperspectral dataset.

    Attributes
    ----------
    shape : array
        Returns the shape of the hyperspectral array

    n_dimension : int
        Returns the number of dimensions of the hyperspectral array (3 or 4)

    n_features : int
        Returns the number of spectral points (features)

    n_samples : int
        Returns the total number of pixels in the hyperspectral array

    image : array, shape(x, y, (z))
        Returns the image averaged over the selected spectral range

    spectrum : array, shape(n_features)
        Returns the spectrum averaged over the selected pixels

    mean_image : array, shape(x, y, (z))
        Returns the image averaged over the entire spectral range

    mean_spectrum : array, shape(n_features)
        Returns the spectrum averaged over all the pixels


    Examples
    --------
    >>> import numpy as np
    >>> from skhyper.process import Process
    >>>
    >>> test_data = np.random.rand(100, 100, 10, 1024)
    >>> X = Process(test_data, scale=True)
    >>>
    >>> X.ndim
    4
    >>>
    >>> X.n_features
    1024
    >>>
    >>> X.n_samples
    100000
    """
    def __init__(self, X):
        # TODO Store in numpy memmap
        self.data = X

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

        self.update()

    def __getitem__(self, item):
        return self.data[item]

    def update(self):
        """ Update properties of the hyperspectral array

        This should be called whenever `X.data` is directly modified to update the attributes
        of the `X` object.

        """
        # Perform data operations
        self._data_checks()
        self._data_mean()
        self._data_access()

    def _data_checks(self):
        if type(self.data) != np.ndarray:
            raise TypeError('Data must be a numpy array')

        self.shape = self.data.shape
        self.ndim = len(self.shape)

        if self.ndim != 3 and self.ndim != 4:
            raise TypeError('Data must be 3- or 4- dimensional.')

        if self.ndim == 3:
            self.n_samples = self.shape[0] * self.shape[1]
            self.n_features = self.shape[2]

            if not self.n_samples > self.n_features:
                # raise TypeError('The number of samples must be greater than the number of features')
                warnings.warn('n_samples (number of pixels) should be greater than n_features (spectral points)')

        elif self.ndim == 4:
            self.n_samples = self.shape[0] * self.shape[1] * self.shape[2]
            self.n_features = self.shape[3]

            if not self.n_samples > self.n_features:
                raise TypeError('The number of samples must be greater than the number of features')

    def _data_flatten(self):
        if self.ndim == 3:
            return np.reshape(self.data, (self.shape[0] * self.shape[1], self.shape[2]))

        elif self.ndim == 4:
            return np.reshape(self.data, (self.shape[0] * self.shape[1] * self.shape[2], self.shape[3]))

    def _data_mean(self):
        if self.ndim == 3:
            self.mean_image = np.squeeze(np.mean(self.data, 2))
            self.mean_spectrum = np.squeeze(np.mean(np.mean(self.data, 1), 0))

        elif self.ndim == 4:
            self.mean_image = np.squeeze(np.mean(self.data, 3))
            self.mean_spectrum = np.squeeze(np.mean(np.mean(np.mean(self.data, 2), 1), 0))

    def _data_access(self):
        self.image = _AccessImage(self.data, self.shape, self.ndim)
        self.spectrum = _AccessSpectrum(self.data, self.shape, self.ndim)

    def view(self):
        """ Hyperspectral viewer

        Opens a hyperspectral viewer with the hyperspectral array loaded (pyqt GUI)
        """
        hsiPlot(self)

    def smoothen(self, **kwargs):
        _data_smoothen(self, **kwargs)
        self.update()

    def flatten(self):
        """Flatten the hyperspectral data

        Flattens the hyperspectral data from 3d/4d to 2d by unravelling the pixel order.

        Returns
        -------
        X_flattened : array, shape (x*y*(z), n_features)
            A flattened version of the hyperspectral array

        """
        return self._data_flatten()

    def scree(self):
        return _data_scree(self)

    def preprocess(self, mdl):
        _data_preprocessing(self, mdl)

    def decompose(self, mdl):        
        return _data_decomposition(self, mdl)

    def cluster(self, mdl, decomposed=False, pca_comps=4):
        return _data_cluster(self, mdl, decomposed, pca_comps)

class _AccessImage:
    def __init__(self, X, shape, n_dimension):
        self.data = X
        self.shape = shape
        self.n_dimension = n_dimension

    def __getitem__(self, item):
        if self.n_dimension == 3:
            return np.squeeze(np.mean(self.data[item], 2))

        elif self.n_dimension == 4:
            return np.squeeze(np.mean(self.data[item], 3))


class _AccessSpectrum:
    def __init__(self, X, shape, n_dimension):
        self.data = X
        self.shape = shape
        self.n_dimension = n_dimension

    def __getitem__(self, item):
        if self.n_dimension == 3:
            return np.squeeze(np.mean(np.mean(self.data[item], 1), 0))

        elif self.n_dimension == 4:
            return np.squeeze(np.mean(np.mean(np.mean(self.data[item], 2), 1), 0))
