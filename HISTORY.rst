=======
History
=======

0.2.1 (2019-08-14)
------------------

* Minor patch release to fix the tagging.

0.2.0 (2019-08-14)
------------------

* Removed `xmler` dependency, simplified, and re-implemented the logic using `xmltodict`.
* Added more tests, including for the CLI and increased tests coverage over 96%.
* Added Python 3.8 to supported versions.
* Removed Python 3.4 from supported versions.

  NOTE: This was supposed to be 0.1.4, but instead of `bumprevision patch` I ran
  `bumprevision minor`, and since the PR is yet be pass TravisCI, I'll do a follow-up
  patch release.

0.1.3 (2019-02-20)
------------------

* Fixed an issue with garbage data appearing from previous transformations (with deepcopy()).

0.1.2 (2019-02-07)
------------------

* Working JSON transformation with multiple input files.

0.1.0 (2018-10-30)
------------------

* First release on PyPI.
