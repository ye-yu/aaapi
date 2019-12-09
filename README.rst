=====
aaapi
=====


.. image:: https://img.shields.io/pypi/v/aaapi.svg
        :target: https://pypi.python.org/pypi/aaapi

.. image:: https://img.shields.io/travis/ye-yu/aaapi.svg
        :target: https://travis-ci.org/ye-yu/aaapi

.. image:: https://readthedocs.org/projects/aaapi/badge/?version=latest
        :target: https://aaapi.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




Another Audio API - Collection of audio and music processing API with massive amount of dependencies


* Free software: MIT license
* Documentation: https://aaapi.readthedocs.io.


Features
--------

- AudioUtils

  - loading wav files
  - splitting audio based on volumn peaks
  - extracting audio features of MFCC and spectral entropy
  - f0 estimation using CREPE

- MidiUtils

  - converting frequencies to musical notes
  - converting frequencies to musical label
  - converting pandas pd into midi files
  - grouping consecutive notes into one note
  - grouping multiple notes into weighted-averaged note

- MusicUtils

  - identifying the scale of the musical notes


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
