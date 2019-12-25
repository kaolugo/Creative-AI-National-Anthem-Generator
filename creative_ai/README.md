# Creative AI Project

Project Proposal (Updated README)
- Thronson
- Kaoru Murai; kaolugo
- Aelita Klausmeier; aelita

Python Libraries Used:
*pysynth
*random
*numpy (in order to run pysynth_b)
*pydub 
    !!!This is an external library that you MUST install for the program to work. !!!
    This library contains functions that mix wave files much better than the mixfiles library
    Documentation: http://pydub.com/
    Installation Instructions:
    1.) Make sure you are in the Creative_AI_3040_Repository directory in terminal
    2.) Enter "pip install pydub" to install this library

Application:
We used the music generation part of our learning model to generate "new" national anthems based on the national anthems that already exist. We used midi files for over 140 national anthems to train our model.

Heuristics Used:
1.) New material to train learning model --- we scraped over 140 midi files from the internet (https://www.midiworld.com/search/5/?q=national%20anthems) to generate "new"  national anthems.
2.) pySynth: we utilized different versions of pySynth (most notably pySynth_C and pySynth_P) to generate appropriate sounds for appropriate parts
3.) Mixing wav files: we mixed different musical parts together (such as melody and rhythm) to create a more fullbodied piece. We used the external library, pydub for this portion.
4.) Same key: we made sure the melody generate stayed in and is in a particular key
5.) Ending Note/Phrase: we made a function to make the ending of the generate song pleasant by making sure it always ended on the root note of the musical key.
6.) Harmony: we made a function to create a background track that harmonizes with the main meolody

Showmanship:
We will be demonstrating our work at the project showcase by generating random "new" national anthems, and playing it along with a randomly generated make-believe national flag.


NOTE: In order to test out and see what our reach does, make sure to choose option 2 in the menu (generate a new national anthem). If you choose option 1, it will generate an error.


**Creative AI** is about using artificial intelligence to automatically generate lyrics and music using datasets of your choice.

Welcome to the Creative AI Project! If you have questions, please check here:

- <a href="https://youtu.be/Z46LvHwgygs?list=PL2BYDiR6uDOJzYCJ7QuuQz-hWvQeYN5Nx" target="_blank">Link to generated lyrics demo</a>

- <a href="https://youtu.be/RrHrRqZ3pUM?list=PL2BYDiR6uDOJzYCJ7QuuQz-hWvQeYN5Nx" target="_blank">Link to generated music demo</a>

- <a href="https://github.com/eecs183/creative-ai/wiki" target="_blank">Link to specification</a>

Here are a few notes to get you started:

* Don't touch the __init__.py files. These are necessary to your project.

* Things will be easier if you read the spec first and follow the given function order.

* Make sure you have ```pip``` installed so you can download pysynth.

* Remember to update this file to describe your finished Final Project.

Good luck on the project!
