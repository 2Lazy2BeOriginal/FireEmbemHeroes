# Troubleshooting 

## Infinite loop midgame 

	While the program is running, there may be moments where it repeats "took screenshot..." in a loop

If you get an infinite loop that repeats

	took screenshot becausefinding game over
	took screenshot becausefinding stage clear
 
but autoplay isn't enabled... Then simply manually "select autoplay" and the bot will run normally.

If you are in the game over screen also get an infinite loop. 
Go through the game over screen and the autoplay and the game will pick up from where it started. (MAKE SURE IT DOES NOT SAY GAMEOVER DETECTED)

If you are in the level select screen: 

  1. end the program (click the red box on top right) and change the variables on the top of the code.
  2. re enter the book, chapter and level.
  3. on your device, scroll all the way back to "Book 1" and return on screen (program assumes you are at home screen)

**Note:** The program does an infinite loop until it detects a "stage clear" just be careful since it automatically assumes that if it finds a skip button than the level must've completed.

Be aware that it goes from
    finding game over
    finding stage clear
    finding skip button
    finding ...
and the program takes 8 seconds to finish one loop. As in you should click "fight" when it says finding ...
and hit skip once it pops up to make sure you don't run into problems

## When the commands don't work

Sometimes the commands do not work, you may have to do some debugging on your end to let the program know where to tap, and what colour it should seek.
Below is a list of commands it will run and all have a prefix of "took screenshot being finding"


    Green button:
        -"the halfway point" on the x axis and a green button
        -go to the find_green() function and change the values inside
        
    skip button:
        -the top right corner and pick the dark red value.
        -go to the find_skip() function and change the values inside
        
    game over screen:
        -the halfway point of the height. and the dark red value on the G
        -go to the did_game_over() and change there
        
    stage clear screen:
        -tha halfway point of the width and move down and pick the dark yellow point. DO NOT PICK WHITE
        AS IT OCCURS MANY TIMES IN THE PROGRAM
        -go to the did_stage_clear() and change there
        
To find out what colours to use simply go to a image color selecting website (such as https://imagecolorpicker.com/en) and then
upload the "screen.png" file (will be located inside the project file) and use the color picker and click on the pixel you 
want to find the colour value of 

    -When you upload the image and select a point on screen. There will be a section that says
    RGB(r value, g value, b value)
    
    -Then depending on the problem you want to adjust the numbers inside the
    is_valid_color() functions to + or - 20 the original number.

    Ex:
    -it said RGB(100,125,150) then change it to is_valid_color(x,80,120,115,145,130,170)
     Do not touch the letter that is at the first comma. It will throw an error

    Note: 20 is an arbitrary number but it gives enough variance while also being specific enough
    Note: for the game over, you want to give it 5 cycles before troubleshooting due to the logo changing colours.


## Failure at the tutorial
If you encounter an error in the tutorial part. Just finish the tutorial and then set Completed_levels to 3
and return to the main hub and click run again.
If you encounter any issues, don't be afraid to dm 2Lazy2BeOriginal#4095 on discord for troubleshooting
