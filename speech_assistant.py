#! /usr/bin/python3

import sys
import subprocess
import os
import platform    # for getting os name
import csv
import re
import colorama  # for colored text
import time
import signal

colorama.init()

osName = platform.system()   # OS name


def defaultSettings() :
    """
    Returns a dictionary of default settings
    """
    # if the file doesn't exist, that means either it is the first time running the script or settings file has been deleted
    # create a settings file
    if not os.path.exists("settings.csv") :
        string = "skipOptions : false\ndefaultOption : 1\nAudioFile transcript fileName : AudioFileName + _transcribed.txt\nopen_Output_In_TextEditor_After : 100\n"
        string += "exitTerminalAfterResult : false\nexitAfter (sec) : 10"
        # writing the settings.csv
        with open("settings.csv", "w") as file :
            file.write(string)

        # manually returning the settings dictionary
        return {"skipOptions" : "false", "defaultOption" : "1", "AudioFile transcript fileName" : "AudioFileName + _transcribed.txt", 
        "open_Output_In_TextEditor_After" : 100, "exitTerminalAfterResult" : "false", "exitAfter (sec)" : "10"}


    with open("settings.csv", "r") as file :
        settings = {i.strip() : j.strip() for i, j in list(csv.reader(file, delimiter=":"))}  #making a settings dictionary

    return settings


def clearScreen() :
    """
    Clears the terminal 
    """
    if osName == "Windows" :
        os.system("cls")
    else :
        os.system("clear")


def homeScreen() :
    """
    Displays stuff on home screen
    """
    clearScreen()   # clear the screen first

    # if the skip options setting is turned to True, this will not be displayed
    if settings["skipOptions"].lower() == "false" :
        terminalWidth = os.get_terminal_size().columns    #getting the width of the terminal window
        print(colorama.Fore.GREEN + "SPEECH ASSISTANT".center(terminalWidth) + "\n" + "~"*terminalWidth + "\n")     # title 
        print(colorama.Style.RESET_ALL)
        print("Two options are available here. ")
        print("1. Use Microphone to convert speech to text. Start speaking after a lag of 0.2 sec. Text is copied to the clipboard. Paste it anywhere you want.")
        print("2. Transcribe an audio file. Saves the transcript to a file with name of the format -> AudioFileName + '_transcribed.txt' in the same folder")

        print("\nTIP: Navigate to the settings.csv file to tinker with the default settings. Like skipping this tiring read altogether. Play with them.")


def clipboardPaste(string) :
    """
    This function pastes the string provided to the clipboard. Works for all the OS.
    """

    if osName == "Windows" :
        os.system("echo " + string + " | CLIP")   #running clip command for windows

    elif osName == "Linux" :
        try :               # if xclip is already installed
            os.system("xclip -selection -clipboard " + string)    

        except :            # if xclip is not installed
            print("Xclip needs to be installed first. Need sudo privileges.")  
            os.system("sudo apt install xclip")
            os.system("xclip -selection -clipboard " + string)

    else :
        subprocess.run("pbcopy", universal_newlines=True, input=string)


def speechMagic() :
    """
    Here speech recognition happens
    """
    r = sr.Recognizer()
    tryAgain = True

    homeScreen()  # calling it for the first time 

    # if the skip Options is turned False, display the prompt
    if settings["skipOptions"] == "false" :
        choice = input("\nYour choice is: ")
    # else put the choice as the default option given in the settings
    # if any random value is entered, it will be set to option 1 i.e. Microphone one.
    else :
        choice = "2" if settings["defaultOption"] == "2" else "1"

    while tryAgain :       # if the speech cannot be comprehended, user can try again
        # using mic for speech recognition
        if choice == "1" :  
            print("\nSpeak as clearly as you can")
            mic = sr.Microphone()
            with mic as source :
                r.adjust_for_ambient_noise(source)  # removing ambient noises from the surrounding
                audio = r.listen(source)

            try :
                text = r.recognize_google(audio)
                print("\nSPEECH TO TEXT ->")                
                print(colorama.Fore.GREEN + text)
                print(colorama.Style.RESET_ALL)
                clipboardPaste(text)   # copying to the clipboard
                print("\nText is copied to clipboard :). Enjoy!\n")

            except sr.RequestError :
                print(colorama.Fore.RED + "API was unreachable :(\n")
                print(colorama.Style.RESET_ALL)
                tryAgain = False   # since API was unreachable, no need to run the loop again
                break

            except sr.UnknownValueError:
                print(colorama.Fore.MAGENTA + "Cannot comprehend. Sorry :(\n") 
                print(colorama.Style.RESET_ALL)

        # if using an audio file
        else :    
            fileName = input("\nFile path: ")

            rightFormat = True

            # if the audioFile name is set to default one provided
            if settings["AudioFile transcript fileName"].lower() == "audiofilename + _transcribed.txt" :
                targetFile = fileName[:fileName.index(".")] + "_transcribed.txt"
            # else set to the provided file name in the settings file
            else :
                targetFile = settings["AudioFile transcript fileName"]

            # if the file format is not .wav, convert it first
            if not re.match(r"\.wav$",fileName)  :
                rightFormat = False
                os.system("mkdir for_file_conversion")  # creating an empty folder in the same directory

                cp = "copy " if osName == "Windows" else "cp "
                os.system(cp + fileName + " for_file_conversion")   # copying the audio file in the new folder
                
                os.system("audioconvert convert for_file_conversion for_file_conversion_new --output-format .wav")  # converting the audio file

                fileName = "for_file_conversion_new\\" if osName == "Windows" else "for_file_conversion_new/" 
                fileName += os.listdir("for_file_conversion_new")[0]  # making the path for the new converted file


            with sr.AudioFile(fileName) as source :
                r.adjust_for_ambient_noise(source)
                audio = r.record(source)

            if not rightFormat :
                # since now the file has been used, time to tidy up. Remove the new created files and folders
                cmd = "rmdir /q /s " if osName == "Windows" else "rm -r "
                os.system(cmd + "for_file_conversion for_file_conversion_new")   

            try :
                text = r.recognize_google(audio)
                print("\nSPEECH TO TEXT ->\n")
                # if the text is too large, open it in the text editor
                if len(text) > settings["open_Output_In_TextEditor_After"] :
                    print("Text size too large. Opening Text editor")
                    time.sleep(0.5)  # wait for half a second
                    if osName == "Windows" :
                        os.system("notepad " + targetFile)
                    else :
                        os.system("gedit " + targetFile)

                else :
                    print(colorama.Fore.GREEN + text)
                    print(colorama.Style.RESET_ALL)
                print("\nTranscript saved at " + targetFile + ". Enjoy! :)")

                with open(targetFile, "w") as file :
                    file.write(text)

            except sr.RequestError :
                print(colorama.Fore.RED + "API was unreachable :(\n")
                print(colorama.Style.RESET_ALL)
                tryAgain = False   # since API was unreachable, no need to run the loop again
                break

        # if the exit Terminal is switched to true
        if settings["exitTerminalAfterResult"] == "true" :
            time.sleep(int(settings["exitAfter (sec)"]))   # go to sleep for specified time
            os.system('taskkill /F /PID ' + str(os.getppid())) if osName == "Windows" else os.system("pidof gnome-terminal | kill -KILL")   # kill the terminal
            sys.exit(0)

        if input("Want to go again?(Y/n) ").lower() == "n" :    # if the user does not want to go again
            tryAgain = False
            clearScreen() # just clear the terminal
            sys.exit(0)
        
        homeScreen()  # bringing the home screen back but with no choice option
        

if __name__ == "__main__" :

    try : 
        import speech_recognition as sr

        try :
            from pydub import AudioSegment
        except ImportError :
            pip = "pip" if osName == "Windows" else "pip3"     # on Windows, it is pip whereas on Linux, it is pip3
            print("pydub library needs to be installed for automatically managing audio file formats.")
            os.system(pip + " install pydub")

            print("FFmpeg needs to be installed for the proper functioning of the pydub.")
            if osName == "Windows" :
                print("Windows doesnot provide any command line method for FFmpeg installation. You have to do that manually :(")
                print("Download FFmpeg zip file from here -> https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z")
                print("For detailed steps of FFmepg installation, visit -> https://www.thewindowsclub.com/how-to-install-ffmpeg-on-windows-10")
                sys.exit(0)

            else :
                print("Run the package installer to install ffmpeg. Eg. on Debian based Linux distro like Ubuntu, run : $ sudo apt install ffmpeg")
                sys.exit(0)

        # checking if the AudioConverter is already installed or not
        cmd = 'pip freeze | findstr "AudioConverter"' if osName == "Windows" else 'pip3 freeze | grep "AudioConverter"'
        if not os.system(cmd) :    # if 0 is returned, that means the command ran successfully
            print("AudioConverter needs to be installed")
            os.system("pip install AudioConverter") if osName == "Windows" else os.system("pip3 install AudioConverter")   # installing

    except ImportError :

        pip = "pip" if osName == "Windows" else "pip3"     # on Windows, it is pip whereas on Linux, it is pip3
        print("speech_recognition library needs to be installed.")
        os.system(pip + " install SpeechRecognition")

        # pyAudio needs to be installed. 
        print("\nPlease install pyAudio yourself. Directly installing pyAudio using pip doesn't seem to work. Apologies :(")
        print("Download .whl file from here -> https://download.lfd.uci.edu/pythonlibs/w4tscw6k/PyAudio-0.2.11-cp39-cp39-win_amd64.whl).")
        print("Then move to the directory where the file is downloaded and run 'pip install PyAudio-0.2.11-cp39-cp39-win_amd64.whl' in the terminal.")

        sys.exit(0)

    settings = defaultSettings()

    speechMagic()

