# Speech-Assistant
A CLI for speech-recognition built in python

An extremely easy to use speech-recognizer built with python. Uses the speech-recognizer library.

## Functionalities
1. Start dictating and the program will transcribe.
2. Provide an audio file and the program will transcribe that.

## Features
* Extremely user-friendly.
* Works on both Windows and Linux. Sorry Mac.
* The transcribed dictation is automatically copied to the clipboard, available for you to paste it anywhere you need.
* The transcription of the audio file is saved as a text file
* Except FFmpeg (for Windows) and PyAudio, all the other necessary packages will be automatically installed. Proper steps and required links are also provided for manual installation of FFmpeg and PyAudio.
* Generates a settings file that can be edited extremely easily to modify certain behaviors of the program
* Can lauch the program in either of the modes i.e. Dictation or AudioFile mode, automatically by tweaking the settings file generated. Choose 1 for Dictation and 2 for AudioFile mode in the defaultOption setting.

## Installation
Either download the zip file of the code or clone the repository using 
```bash
$ git clone https://github.com/Rachit-Singh/Speech-Assistant.git
```

The program includes shebang. So in Linux, just make the script executable and run without calling the interpreter everytime. Better, for quick switch, add the shell command to the keyboard shortcuts.

In Windows, the program can be launched by double clicking the icon. Setting a keyboard-shortcut for any shell command, like in any Linux distro, seems impossible to me. If there exists a way to do this, please inform me as well. 
