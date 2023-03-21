==================
Contribution Guide
==================

Contributions are highly welcomed and appreciated. Every little help counts,
so do not hesitate! You can make a high impact on ``openclimate`` just by using it and
reporting `issues <https://github.com/Open-Earth-Foundation/OpenClimate-pyclient/issues>`__.

The following sections cover some general guidelines
regarding development in ``openclimate`` for maintainers and contributors.

Nothing here is set in stone and can't be changed.
Feel free to suggest improvements or changes in the workflow.


.. contents:: Contribution links
   :depth: 2



.. _submitfeedback:

Feature requests and feedback
-----------------------------

We are eager to hear about your requests for new features and any suggestions about the
API, infrastructure, and so on. Feel free to submit these as
`issues <https://github.com/Open-Earth-Foundation/OpenClimate-pyclient/issues/new>`__
with the label "feature request."

Please make sure to explain in detail how the feature should work and keep the scope as
narrow as possible. This will make it easier to implement in small PRs.


.. _reportbugs:

Report bugs
-----------

Report bugs for ``openclimate`` in the `issue tracker <https://github.com/Open-Earth-Foundation/OpenClimate-pyclient/issues>`_
with the label "bug".

If you can write a demonstration test that currently fails but should pass
that is a very useful commit to make as well, even if you cannot fix the bug itself.


.. _fixbugs:

Fix bugs
--------

Look through the `GitHub issues for bugs <https://github.com/Open-Earth-Foundation/OpenClimate-pyclient/labels/bugs>`_.

Talk to developers to find out how you can fix specific bugs.



Preparing Pull Requests
-----------------------

#. Fork the
   `OpenClimate-pyclient GitHub repository <https://github.com/Open-Earth-Foundation/OpenClimate-pyclient>`__.
   It's fine to use ``OpenClimate-pyclient`` as your fork repository name because it will live
   under your username.

#. Clone your fork locally using `git <https://git-scm.com/>`_, connect your repository
   to the upstream (main project), and create a branch::

    $ git clone git@github.com:YOUR_GITHUB_USERNAME/OpenClimate-pyclient.git
    $ cd OpenClimate-pyclient
    $ git remote add upstream git@github.com:Open-Earth-Foundation/OpenClimate-pyclient.git

    # now, to fix a bug or add feature create your own branch off "master":

    $ git checkout -b your-bugfix-feature-branch-name master

   If you need some help with Git, follow this quick start
   guide: https://git.wiki.kernel.org/index.php/QuickStart

#. Set up a [conda](environment) with all necessary dependencies::

    $ conda env create -f ci/environment-py3.8.yml

#. Activate your environment::

   $ conda activate test_env_openclimate

#. Install the openclimate package::

   $ pip install -e . --no-deps

#. Before you modify anything, ensure that the setup works by executing all tests::

   $ pytest

   You want to see an output indicating no failures, like this::

   $ ========================== n passed, j warnings in 17.07s ===========================

#. Finally, submit a pull request through the GitHub website using this data::

    head-fork: YOUR_GITHUB_USERNAME/
    compare: your-branch-name

    base-fork: Open-Earth-Foundation/OpenClimate-pyclient
    base: master

   The merged pull request will undergo the same testing that your local branch
   had to pass when pushing.