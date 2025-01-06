# About

Want to earn MyNintendo Platnium points without personally playing the game yourself? This program is for you! This script will follow a set sequence of steps by checking what colour a particular pixel is. Since the colours are repeated many times throughout the game and the UI does not change positions frequently. 

For any troubleshooting please message 2Lazy2BeOriginal#4095 :) 

## Setting up the Android
1. Go to your android phone and enter settings, then scroll all the way down to **About Phone** and search for anything mentioning **build model**
2. Click the build model a few times until it says to **enable developer mode** click yes
3. Head back to settings and look for a section called **Developer mode** inside there will be an option for **USB debugging**. enable it.
4. Plug the phone to your laptop/monitor. via USB, (usb C do not work for some reason)

## Setting up the laptop
1. Click the [link](https://developer.android.com/studio/releases/platform-tools) and download the appropiate OS (Mine is Windows)
2. Once clicked, extract the folder and then go to into **platform-tools** folder and open the terminal
   - on Windows, right click, and scroll all the way down to  **terminal**
   - on Mac, you will have to manually enter the path.
   	- Open the **LaunchPad** and in the search bar type **terminal**.
   	- Then (assuming it is on the downloads folder) type `cd Downloads/platform-tools`
3. Copy and paste `./adb devices` and your phone should get a notification if you want to connect it or not. Click accept
4. Once clicked, it should display "List of devices" with a random number and "device"
   - To test it out, try `./adb shell input touchscreen swipe 500 500 1000 2000` in the terminal andthe phone should scroll up.

Optional: 
	Scroll down to the download section if this page https://github.com/Genymobile/scrcpy
	Extract the file and open the scrpy file. It should work automatically

## Python part:
If you have python already on your laptop then skip step 1-3
1. install [python](https://www.python.org/downloads/) and [pycharm](https://www.jetbrains.com/pycharm/download/?section=mac) to your laptop
2. Install pycharm on your computer create a new project
3. Copy and paste the contents in `main.py` to `main.py`

If you have **Pycharm installed** then you can easily install the required packages by following these steps

	ignore:
        2. Go to the search bar and type command prompt and open the file, then type
            `pip install pure-python-adb`
            `pip install numpy`
            `pip install mss`
    3. Open pycharm and create a new project, from this project you want to copy and paste, the "main.py"
    contents
	2. tap the search bar on the top right, enter "python packages". click it and
	there will be a search bar and simply type "ppadb-uiautomator". Then there should be a install button
	somewhere.
	3. repeat step 2 for "Pillow" and "numpy"


## Before you start the program
1. Boot into Fire Emblem Heroes and **finish the tutorial** and finish downloading the additional files it will ask.
2. Head into settings and make sure that the options ensure the fastest time. Photos are attached on what the option screen should look like — click the *misc* button, than settings and match the screen
3. Head back to the main menu of the game and go through the daily login-in bonus. 

Assuming all goes to plan, you can click the green arrow on the top right and sit back and relaxing

## Some notes about the console messages

While the program is running, you will notice some text being printed out that says "took screenshot..." and "stage complete" 
The reasoning is that the program will relies on using colours on screen to do a certain action. The program follows a predictable cycle it expects from the game. However when the sequence breaks, it's up to **you** to see where it broke.

On the top of the script, there will be 3 variables **in caps** that indicate which Book,Chapter and level you are on. You want to replace the values to the **next level to be completed**

**YOU MUST RETURN TO BOOK 1** 

## What to do after the inital set up

If you are planning on using the program on a later date (or your laptop/desktop goes to sleep) you must repeat step 2-4 at the "setting up your laptop" section to turn on the automation program. Failure to do so will have the program tell you "no device attached" 

