=====================
Unsupervised learning
=====================

The `hparray` object has built in methods that allows you to perform several unsupervised learning
techniques on the stored data. The techniques are split into the following categories:

- Dimensionality reduction
- Clustering
- Mixture models
- Abundance mapping

These are all available as methods on the `hparray` object.

.. code-block:: python

    import numpy as np
    import hypers as hp

    test_data = np.random.rand(10, 10, 1000)
    X = hp.array(test_data)

    # To access PCA from the dimensionality reduction techniques
    ims, spcs = X.decompose.pca.calculate(n_components=10)

    # To access k-means from the clustering techniques
    lbls, spcs = X.cluster.kmeans.calculate(n_clusters=4)

    # To access Gaussian mixture models
    lbls, spcs = X.mixture.gaussian_mixture.calculate(n_components=10)

    # To access unconstrained least-squares for abundance mapping
    spectra = np.random.rand(1000, 2)
    amap = X.abundance.ucls.calculate(spectra)


