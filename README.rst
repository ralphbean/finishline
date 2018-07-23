Finishline
==========

A script for generating reports from JIRA

https://www.youtube.com/watch?v=jK5n7HY4nfA

.. contents:: Contents

Getting Started
===============

Creating your config file
_________________________

First copy :code:`example.conf` to :code:`YOURPROJECT.conf`. Supply the
appropriate values for any REQUIRED options as well as any optional fields
that you wish to use.

Config file format
~~~~~~~~~~~~~~~~~~

The config file uses the `INI format`_. All required options for Finishline
are within an [options] section. In the :code:`example.conf` file, commented
lines indicate which options are required. Optional values are commented
out. In the case of optional values, the defaults are configured in
:code:`defaults.py`.

Config scenarios
~~~~~~~~~~~~~~~~

The config file supports specifying any arbitrary number of "scenarios". These
are intended to be used when you regularly run Finishline with different
values for the same config option. A common example is using different output
templates depending on how you wish to report status. Scenarios provide a
mechanism for storing all of these different values for a given config
option in the same config file.

To create a scenario, simply add a new section to your config file. The name
of the section will be the name of the scenario. Add any config options
specific to the scenario to the new section. Values specified here override
the values specified in the [options] section. To run Finishline using a
scenario, pass the -s/--scenario argument to Finishline, specifying the
name of the scenario you wish to use.

Creating your Makefile
______________________

It is recommended to use the :code:`make`, to automate running Finishline.
:code:`Make` is a general purpose build automation tool that performs a series
of steps defined in a :code:`Makefile`. The :code:`make` tool is readily
available on all platforms, but steps for installing it are out of scope for
this README.

A key function of Finishline is generating Google Slides presentations that
contain status information about a JIRA project. Before you get started, you
should create a slide deck to be used for this purpose. After creating the
deck, make a note of the deck's identifier, which can be found in the Google
Slides URL (it should be in the form
https://docs.google.com/presentation/d/$SLIDES_ID). This ID will be referred
to later as :code:`$(SLIDES_ID)`.

To start using Finishline for your JIRA project, first copy
:code:`Makefile.sample` to :code:`Makefile.$(YOURPROJECT)` (note that
:code:`$(YOURPROJECT)` should be the name of your JIRA project). This sample
:code:`Makefile` has been preconfigured with a couple of targets that will
allow you to create status slides as well as create an email status report.

There are a few small changes that you'll need to make
in your new :code:`Makefile.$(YOURPROJECT)`:

- Replace all instances of :code:`$(YOUR_CONFIG_FILE)` with the name of the
  config file you created earlier.

- Replace all instances of :code:`$(YOUR_SLIDES_TITLE)` with a title that you
  wish to be used to name your status slide deck.

- Replace all instances of :code:`$(SLIDES_ID)` with your slide deck ID

Running Finishline
__________________

To test Finishline on your project, run the following command from the root of
the Finishline git repo:

::

  make -f Makefile.$(YOURPROJECT) buildstatus

Upon running this command, Finishline will query JIRA for all issues that are
in progress or recently completed. It will attempt to determine the parent
epic for each of these issues, can calculate a progress percentage for that
epic by calculating the percentage of story points or issues within that epic
that are complete. Finishline assumes that your project uses the OKR process.
As such, it expects issues to be grouped in an epic representing a KR, and
that all KR epics are in turn sub tasks of another epic representing an
Objective. When finishline runs, it will attempt to determine the parent
Objective for all issues and group content as such. If no parent Objective
can be found, KRs will be grouped under a general "Miscellaneous" heading.

When the above command is run, the status report content will be written
to a file :code:`foo.md`. Check this file to make sure its content is what you
expect. If it is, run the following command to generate the status slide
deck:

::

  make -f Makefile.$(YOURPROJECT) uploadstatus

When the command is complete, your slide deck will automatically open
in a browser window.

Another supported reporting format is plain text (e.g. for sending email
status reports). In this mode, the report is saved to a text file, the
contents of which can be copied into whatever location you wish. To
generate this text report, run the following command:

::

  make -f Makefile.$(YOURPROJECT) buildemail

This will save the report to a file titled :code:`report-$(DATE).md`. (This
file name is set in :code:`Makefile.$(YOURPROJECT)` on the last line of the
:code:`buildemail` Make target.)

Finishline supports other arguments and features. We're working on adding
documentation for all of this functionality. For now, feel free to reach
out in a GitHub issue if you have any questions.

Old Argument Format
===================

Finishline has been refactored to use config files instead of command line
arguments. If you wish to use the old command line argument functionality,
you may use the version of the code at the :code:`old-argument-format` git
tag. Note that new code changes will not be backported to this tag.

.. _INI Format: https://en.wikipedia.org/wiki/INI_file
