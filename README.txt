This is a multi-objective evolutionary algorithm which tries to solve the MAXSAT problem while also maximizing the
    number of variables which do not need to be set
This program requires python 2.7 with numpy
If you wish to use the graphing facilities (plot.py) of this program you must also have matplotlib installed

Configuration files for some preset CNF files and EA configurations are placed in /config
These preset configuration files will produce log and solution files in the /output folder

Important files:
	run.py - This is the main entry point to the EA, run with the '-h' flag to see more info
	plot.py - This generates plots from given log and solution files.  Run with '-h' flag to see more info

To run the EA on a specific CNF file:
    python2 run.py -c CNF_FILE
This will create the output files:
    log.txt
    solution.txt
        
To run with a specified configuration file:
    python2 run.py @CONFIG_FILE
Example:
    python2 run.py @config/2.cfg

To get help on all command-line options:
    python2 run.py -h

To generate a plot:
    python2 plot.py -l LOG_FILE

PRESET CONFIGURATION FILES
A number of pre-made configuration files have been placed in /config/
Most of these correspond with the configurations described in the PDF document.
Configuration one:   random:     random.args
Configuration two:   FPS:        fps.args
Configuration three: kTourn:     ktourn.args
Configuration four:  truncation: truncation.args
Configuration five:  comma:      comma.args
Configuration six:   bigsteps:   bigstep.args
Configuration seven: tinysteps:  tinystep.args
Output for these configurations is also placed in /output/ using a similar naming scheme.
Graphs of these configurations are placed in /ouput/ as well.

