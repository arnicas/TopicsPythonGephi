
You can go a la carte - just follow one part or the other.  The primary code is done in python (I'll make some scripts you can run from the command line if you don't want to do the notebook stuff) and the visual part is in Gephi. You should also have text editing ability on your machine.


Installing Python:
-------

Download miniconda for Python 2.7 from here:
[http://conda.pydata.org/miniconda.html][1]

To install it on a Mac, you need to open a terminal window and find it in your downloads file. Then type:

>sh Miniconda-3.6.0-MacOSX-x86_64.sh

Accept the defaults.  Open a new terminal window afterwards.

Then from the command line in the new window, make a directory for the class:

    >conda create -n topic_workshop ipython-notebook nltk pip
    [accept the defaults]
    >source activate topic_workshop
    >pip install pattern

You should see a prompt that shows the name of your new virtual environment (venv):

>(topic_workshop) morestuffhere$

Check it all worked by starting the notebook server:

>(topic_workshop)$ ipython notebook

You should see the notebook server start up and open a web page with a list of directories.  (You can shut down the notebook server by typing Control-C in the window where you started it.)

Installing Gephi (application for graph layout and export):
------------------------------------------------


Download here: [https://gephi.github.io/][2]

**Note:** On the Mac, you may have an issue running it if you don't have Java 6 installed.  You can install that from here: [http://support.apple.com/kb/DL1572][3]

After you do that, if you want to keep using Java 7 on your machine for other things, go to *System Preferences>Java* and update back to Java 7.  You'll still be able to use Java 6 via Gephi, which looks for it specifically.

If you have any more issues with this, try this:

To check if you have 1.6 installed, at a command prompt:

> /usr/libexec/java_home -v 1.6

This should report a path something like this:

  >/System/Library/Java/JavaVirtualMachines/1.6.0.jdk/Contents/Home

To configure Gephi, edit the file: **/Applications/Gephi.app/Contents/Resources/gephi/etc/gephi.conf** and add **jdkhome="[the path you got above]"**


Plugins to install for Gephi:
-----------------------------

When you start Gephi up, just pick **New Project**, and then go to the top menu for **Tools > Plugins**. 

Click on "Available Plugins" and search for **Sigma Exporter**.  
I also suggest getting the **Circular Layout**.  (Add as many as you want.)

Install them, and restart if necessary, the go back in and make sure they are Active - you can find this switch under "Installed".

*Written with [StackEdit](https://stackedit.io/).*

  [1]: http://conda.pydata.org/miniconda.html
  [2]: https://gephi.github.io/
  [3]: http://support.apple.com/kb/DL1572
