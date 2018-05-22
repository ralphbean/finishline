A script for generating reports from JIRA::

    $ cp Makefile.factory Makefile.yourproject
    $ <edit your makefile to tweak values>
    $ make -f Makefile.yourproject uploadsprint


You can also store command line options in a configuration file::

    $ python finishline.py -c myconfig.ini


https://www.youtube.com/watch?v=jK5n7HY4nfA

Getting Started
_______________

The easiest way to get started using Finishline is to use :code:`make`, a general
build automation tool that performs a series of steps defined in a :code:`Makefile`.
The :code:`make` tool is readily available on all platforms, but steps for installing
it are out of scope for this README.

A key function of Finishline is generating Google Slides presentations that
contain status information about a JIRA project. Before you get started, you
should create a slide deck to be used for this purpose. After creating the
deck, make a note of the deck's identifier, which can be found in the Google
Slides URL (it should be in the form
https://docs.google.com/presentation/d/$SLIDES_ID). This ID will be referred
to later as :code:`$(SLIDES_ID)`.

To start using Finishline for your JIRA project, first copy :code:`Makefile.sample`
to :code:`Makefile.$(YOURPROJECT)` (note that :code:`$(YOURPROJECT)` should be the name of
your JIRA project). There are a few small changes that you'll need to make
in your new :code:`Makefile.$(YOURPROJECT)`:

- Replace all instances of :code:`$(YOURPROJECT)` with the name of your JIRA project

- Replace all instances of :code:`$(SLIDES_ID)` with your slide deck ID

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
