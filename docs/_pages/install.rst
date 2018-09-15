Installation of chuda
=================================

.. toctree::
    :hidden:

This part of the documentation covers the installation of chuda.
The first step to using any software package is getting it properly installed.

$ pipenv install chuda
----------------------

To install chuda, simply run this simple command in your terminal of choice:

.. code-block:: bash

    $ pipenv install chuda

If you don’t have pipenv installed, head over to the `Pipenv website <https://docs.pipenv.org/>`_ for
installation instructions. Or, if you prefer to just use pip and don’t have it installed,
this Python installation guide can guide you through the process.

Get the Source Code
-------------------

chuda is developed on GitHub, where the code is always available.

You can either clone the public repository:

.. code-block:: bash

    $ git clone git://github.com/Varkal/chuda.git

Or, download the tarball:

.. code-block:: bash

    $ curl -OL https://github.com/Varkal/chuda/tarball/master
    # optionally, zipball is also available (for Windows users).

Once you have a copy of the source, you can embed it in your own Python package, or install it into your
site-packages easily:

.. code-block:: bash

    $ cd chuda
    $ pip install .
