# LiMoNS
 LInux MOnitoring NodeS
# HOW Use
 How the script works:

The script operation modes are controlled through parameters.


[Duration] parameter
'-d' or '--duration' is the main parameter that sets the mode of the script.
if specified as 00:00 - the script runs until it is interrupted by an external command
if it is specified as HH: MM - the script runs HH hours and MM minutes (there will be not a large error at the level of seconds) and will stop working
if specified as XX, the script will run XX cycles of information retrieval and stop working

Example:
./limons.py -e 00:00
or
./limons.py --duration 00:00

Examples of using:
./limons.py -d 00:00 - script runs until forced stop
./limons.py -d 01:00 - the script runs for 1 hour (+/- a few seconds) and stops working
./limons.py -d 50 - the script will remove the system indicators 50 times and stop working



[Pause] parameter
'-p', '--pause' - the main parameter, sets the period for removing the indicators. It is set in milliseconds. The default is 1000ms. or 1 sec., i.e. monitored values ​​will be taken every 1000 msec.

Examples of using
./limons.py -p 3000
or
./limons.py --pause 1500



[Display] parameter
'-od', '--display'
Important parameter - enables or disables the display of all captured indicators on the screen (default: false)
Examples of using
./limons.py -od true
or
./limons.py --display true



[Analytics] parameter
'-oa', '--analytics'
Important parameter - enables or disables the recording of all captured indicators to a csv file for further analysis (default: false)
Examples of using
./limons.py -oa true
or
./limons.py --analytics true
Additional Information:
csv file contains:
- column headings (corresponding to the name of the measured indicators)
- rows with data for each column
-record separator ";"
- decimal separator ","
If Docker is not found in the system - columns with container data are not displayed



[Log] parameter
'-l', '--log',
Enables or disables error logging (default: true)
Examples of using
Examples of using
./limons.py -l true
or
./limons.py --log true?


[Version] parameter
'-v', '--version',
Displays the current version of LeMoNS, some system characteristics, and exits
Examples of using
./limons.py -v ?
or
./limons.py --version ?
Return code (0)



[Debug] parameter
'-e' or '--debug' - the parameter indicates that the script is running in debug mode.
Examples of using
./limons.py -e true
or
./limons.py --debug true



Attention: if both display and analytics parameters are set to false - the script will stop working, return code (1000)
