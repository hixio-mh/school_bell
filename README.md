# Loudspeaker school bell

## With this piece of software you can:
* Set a schedule for the bell to follow
* Specify school holidays, when the bell shouldn't ring
* Specify the days of week, when education in school is usually done
* Specify exceptions for the second an third points
* Switch a relay through a Raspberry Pi's GPIO pins (more on that below)

## Whith this piece of software you can't (yet):
* Switch a relay with anything else than a Raspberry Pi's GPIO pins

### Installation:
This program doesn't really need any installation,    
BUT:    
At the moment, the script is not fully automatic, which means, that it stops every day at midnight.    
This is needed, because the script checks whether the bell is needed or not on that day, before starting the timer.   
If you don't want to start the script by hand every day (which you probably don't want), you have to schedule it somehow.    
On UNIX based and UNIX like systems you can use [cron](https://en.wikipedia.org/wiki/Cron) ([here is a little manual](https://www.raspberrypi.org/documentation/linux/usage/cron.md)).   
On Windows, you can use the built-in task scheduler.
### Configuration:
You can configure the bell by editing the files in the `data` folder.   
More info on those are written in the `ReadMe.txt` file next to the data files.   
You can copy your own audio files into the `sound` folder (more about that below).
### Set your own bells:
There are two audio files in the `sound` folder.
One of them is called `start.wav`, and the other one is called `end.wav`. The `start.wav` file is being played when the warning bell (two minutes before class) or the starting bell (at the start of class) is "ringing", and `end.wav` is playing at the end of each class.   

The playing of audio is not being handled by python. You have to specify a terminal command, that you want to use, to play the files (On windows, you can go with `"start"` (default), and it will play the files with the default application). You can specify this command by editing the `termcommand` variable in the `init_vars` file.   

#### The player must quit after playing the audio file!!
> TIP: On Linux, you can do it with vlc using this: `cvlc --play-and-exit`

> NOTES: On raspbian, `termcommand` can be set to `"omxplayer -o both"` || The command should be specified without the file's path.    

### Raspberry Pi GPIO output:
If the program can load the `RPi.GPIO` module, it will switch a GPIO pins output to `HIGH` (3.3v) when the bell is ringing. This can be used to turn on an indicator LED, or switch an opto-coupled relay(to turn on an amplifier for example).   
The used GPIO pin is pin `5` by default, but can be specified in the `init_vars` file by editing the `tvpin` variable.
