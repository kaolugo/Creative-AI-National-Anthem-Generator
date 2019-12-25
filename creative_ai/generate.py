#!/usr/bin/env python
import sys
sys.dont_write_bytecode = True # Suppress .pyc files

import random

import pysynth_c as psb
import pysynth_p as psp
#import pysynth_b as psa

import mixfiles

from pydub import AudioSegment #testing out a new way to mix wav files

from creative_ai.utils.menu import Menu
from creative_ai.data.dataLoader import *
from creative_ai.models.musicInfo import *
from creative_ai.models.languageModel import LanguageModel

TEAM = 'Thronson House'
LYRICSDIRS = ['the_beatles']
TESTLYRICSDIRS = ['the_beatles_test']
MUSICDIRS = ['nationalAnthems']
WAVDIR = 'wav/'

MAJOR_SCALES = [['c', 'd', 'e', 'f', 'g', 'a', 'b'], ['d', 'e', 'f#', 'gb', 'g', 'a', 'b', 'c#', 'db'], ['e', 'f#', 'gb', 'g#', 'a', 'b', 'c#', 'db',  'd#', 'eb'], ['f', 'g', 'a', 'bb', 'a#', 'c', 'd', 'e'], ['g', 'a', 'b', 'c', 'd', 'e', 'f#', 'gb'], ['a', 'b', 'c#', 'db', 'd', 'e', 'f#', 'gb', 'g#', 'ab'], ['b', 'c#', 'db', 'd#', 'eb', 'e', 'f#', 'gb', 'g#', 'ab', 'a#', 'bb'], ['db', 'c#', 'eb', 'd#', 'f', 'gb', 'f#', 'ab', 'g#', 'bb', 'a#', 'c'], ['eb', 'd#', 'f', 'g', 'ab', 'g#', 'bb', 'a#', 'c', 'd'], ['f#', 'gb',  'g#', 'ab', 'a#', 'bb', 'b', 'c#', 'db', 'd#', 'eb', 'f'], ['ab', 'g#', 'bb', 'a#', 'c', 'db', 'c#', 'eb', 'd#', 'f', 'g'], ['bb', 'a#', 'c', 'd', 'eb', 'd#', 'f', 'g', 'a']] #list of major scales

ROOT_NOTES = [['c', 'e', 'g'], ['d', 'f#', 'a'], ['e', 'g#', 'b'], ['f', 'a', 'c'], ['g', 'b', 'd'], ['a', 'c#', 'e'], ['b', 'd#', 'f#'], ['db', 'd#', 'gb'], ['eb', 'g', 'bb'], ['f#', 'bb', 'c#'], ['ab', 'c', 'eb'], ['bb', 'd', 'f']] #list of root notes of all major scales

def output_models(val, output_fn = None):
    """
    Requires: nothing
    Modifies: nothing
    Effects:  outputs the dictionary val to the given filename. Used
              in Test mode.

    This function has been done for you.
    """
    from pprint import pprint
    if output_fn == None:
        print("No Filename Given")
        return
    with open('TEST_OUTPUT/' + output_fn, 'wt') as out:
        pprint(val, stream=out)

def sentenceTooLong(desiredLength, currentLength):
    """
    Requires: nothing
    Modifies: nothing
    Effects:  returns a bool indicating whether or not this sentence should
              be ended based on its length.

    This function has been done for you.
    """
    STDEV = 1
    val = random.gauss(currentLength, STDEV)
    return val > desiredLength

def printSongLyrics(verseOne, verseTwo, chorus):
    """
    Requires: verseOne, verseTwo, and chorus are lists of lists of strings
    Modifies: nothing
    Effects:  prints the song.

    This function is done for you.
    """
    verses = [verseOne, chorus, verseTwo, chorus]

    print()
    for verse in verses:
        for line in verse:
            print((' '.join(line)).capitalize())
        print()

def trainLyricModels(lyricDirs, test=False):
    """
    Requires: lyricDirs is a list of directories in data/lyrics/
    Modifies: nothing
    Effects:  loads data from the folders in the lyricDirs list,
              using the pre-written DataLoader class, then creates an
              instance of each of the NGramModel child classes and trains
              them using the text loaded from the data loader. The list
              should be in tri-, then bi-, then unigramModel order.
              Returns the list of trained models.

    This function is done for you.
    """
    model = LanguageModel()

    for ldir in lyricDirs:
        lyrics = prepData(loadLyrics(ldir))
        model.updateTrainedData(lyrics)

    return model

def trainMusicModels(musicDirs):
    """
    Requires: musicDirs is a list of directories in data/midi/
    Modifies: nothing
    Effects:  works exactly as trainLyricsModels, except that
              now the dataLoader calls the DataLoader's loadMusic() function
              and takes a music directory name instead of an artist name.
              Returns a list of trained models in order of tri-, then bi-, then
              unigramModel objects.

    This function is done for you.
    """
    model = LanguageModel()

    for mdir in musicDirs:
        music = prepData(loadMusic(mdir))
        #print(music)
        model.updateTrainedData(music)

    return model

def runLyricsGenerator(models):
    """
    Requires: models is a list of a trained nGramModel child class objects
    Modifies: nothing
    Effects:  generates a verse one, a verse two, and a chorus, then
              calls printSongLyrics to print the song out.
    """
    verseOne = []
    verseTwo = []
    chorus = []

    for _ in range(4):
        verseOne.append(generateTokenSentence(models, 7))
        verseTwo.append(generateTokenSentence(models, 7))
        chorus.append(generateTokenSentence(models, 9))

    printSongLyrics(verseOne, verseTwo, chorus)

def runMusicGenerator(models, songName):
    """
    Requires: models is a list of trained models
    Modifies: nothing
    Effects:  uses models to generate a song and write it to the file
              named songName.wav
    """
    scale = random.randint(0, 11) #generates the scale to be used for this song

    verseOne = []
    verseTwo = []
    chorus = []

    for i in range(4):
        verseOne.extend(generateTokenSentence(models, 7, scale))
        verseTwo.extend(generateTokenSentence(models, 7, scale))
        chorus.extend(generateTokenSentence(models, 9, scale))

    song = []
    song.extend(verseOne)
    song.extend(verseTwo)
    song.extend(chorus)
    song.extend(verseOne)
    song.extend(chorus)

    finalPhrase = genEndPhrase(song, scale) #generates and assigns the ending note of the song to finalNote

    song.extend(finalPhrase)

    beat = []
    beat.extend(generatePercussion(models, 120))

    harmonyList = harmonize(models, scale, 120)

    harmony1Name = 'wav/h1Name.wav'
    harmony2Name = 'wav/h2Name.wav'
    harmony3Name = 'wav/h3Name.wav'

    #whichHarmony = random.randint(0, 2)

    h1 = harmonyList[0]
    h2 = harmonyList[1]
    h3 = harmonyList[2]
    
    
    beatName = 'wav/beatName.wav'
    firstHarmonyIteration = 'wav/firstHarmonyIteration.wav'
    harmony = 'wav/harmony.wav'
    songAndHarmony = 'wav/songAndHarmony.wav'
    

    #bpm chooser - random choice
    bpmProb = random.randint(0, 9)

    bpm1 = 80
    bpm2 = 100
    bpm3 = 115

    if bpmProb in range(0,4):
        selectedBPM = bpm1
    elif bpmProb in range(4, 7):
        selectedBPM = bpm2
    elif bpmProb in range(7, 10):
        selectedBPM = bpm3

    psb.make_wav(song, fn=songName, bpm = selectedBPM)
    psp.make_wav(beat, fn=beatName, bpm = selectedBPM)

    #makes individual note harmony 'songs'
    psb.make_wav(h1, fn=harmony1Name, bpm = selectedBPM)
    psb.make_wav(h2, fn=harmony2Name, bpm = selectedBPM)
    psb.make_wav(h3, fn=harmony3Name, bpm = selectedBPM)

    #mixfiles.mix_files(harmony1Name, harmony2Name, firstHarmonyIteration)
    #mixfiles.mix_files(firstHarmonyIteration, harmony3Name, harmony)

    #mixfiles.mix_files(songName, harmony1Name, songAndHarmony)
    #UNCOMMENT IF PYDUB DON'T WORK
    
    harmonyOnePydub = AudioSegment.from_file(harmony1Name)
    harmonyOnePydub = harmonyOnePydub - 10 #lowers the volume of the harmony track by 5 dBs
    
    harmonyTwoPydub = AudioSegment.from_file(harmony2Name)
    harmonyTwoPydub = harmonyTwoPydub - 10
    
    combined = harmonyOnePydub.overlay(harmonyTwoPydub)
    combined.export(firstHarmonyIteration, format='wav')
    
    
    firstHarmonyIterationPydub = AudioSegment.from_file(firstHarmonyIteration)
    
    harmonyThreePydub = AudioSegment.from_file(harmony3Name)
    harmonyThreePydub = harmonyThreePydub - 10
    
    combined = firstHarmonyIterationPydub.overlay(harmonyThreePydub)
    combined.export(harmony, format='wav')
    
    
    harmonyPydub = AudioSegment.from_file(harmony)
    melodyPydub = AudioSegment.from_file(songName)
    
    combined = melodyPydub.overlay(harmonyPydub)
    
    combined.export(songAndHarmony, format='wav')
    
    
    
    anthemName = input("What would you like to name your anthem? ")
    anthemName = WAVDIR + anthemName + '.wav'
    
    
    #mixing harmony&melody with percussion
    harmonyAndMelodyPydub = AudioSegment.from_file(songAndHarmony)
    percussionPydub = AudioSegment.from_file(beatName)
    
    
    combined = harmonyAndMelodyPydub.overlay(percussionPydub)
    
    combined.export(anthemName, format='wav')



###############################################################################
# Begin Core >> FOR CORE IMPLEMENTION, DO NOT EDIT OUTSIDE OF THIS SECTION <<
###############################################################################

def generateTokenSentence(model, desiredLength, scale):
    """
    Requires: model is a single trained languageModel object.
              desiredLength is the desired length of the sentence.
    Modifies: nothing
    Effects:  returns a list of strings where each string is a word in the
              generated sentence. The returned list should NOT include
              any of the special starting or ending symbols.

              For more details about generating a sentence using the
              NGramModels, see the spec.
    """
    sentence = ['^::^', '^:::^'] #create an empty list, this will be the list that is returned at the end of this function

    nextToken = model.getNextToken(sentence, MAJOR_SCALES[scale]) #nextToken is the word generated by getNextToken that will be added to the sentence list

    while sentenceTooLong(desiredLength, len(sentence)) is not True:
        if nextToken == '$:::$':
            return sentence[2:]
        sentence.append(nextToken) #adds generated word to sentence list
        nextToken = model.getNextToken(sentence, None) #generates the next possible word to add

    return sentence [2:]

def generatePercussion(model, desiredLength):
    """
    Requires: model is a single trained languageModel object.
              desiredLength is the desired length of the sentence.
    Modifies: nothing
    Effects:  randomly returns one of three different percussive "backbeats"
              for use in making a national anthem.
    """
    sentence = []

    #generates random number for probability of backbeat
    bbProb = random.randint(0,9)

    #defines backbeats
    backbeat1 = [('d1', 4), ('g1', 4)]
    backbeat2 = [('g1', 2), ('c2', 2)]
    backbeat3 = [('c1', 4), ('d1', 8)]

    #chooses a backbeat randomly
    if bbProb in range(0,4):
        selectedBeat = backbeat1
    elif bbProb in range(4, 7):
        selectedBeat = backbeat2
    elif bbProb in range(7, 10):
        selectedBeat = backbeat3

    #loops backbeat for desiredLength
    while sentenceTooLong(desiredLength, len(sentence)) is not True:
        for beatTuple in selectedBeat:
            sentence.append(beatTuple)

    return sentence

def harmonize(model, scale, desiredLength):
    """
    Requires: model is a single trained languageModel object.
              desiredLength is the desired length of the sentence.
              scale is the key in which the song is in.
    Modifies: nothing
    Effects:  returns a list of three songs that consist of a single note,
              that, when put together, form a harmony.
    """
    rootNoteList = ROOT_NOTES[scale]

    sentence1 = []
    sentence2 = []
    sentence3 = []

    r1 = (rootNoteList[0] + '3', 4)
    r2 = (rootNoteList[1] + '3', 4)
    r3 = (rootNoteList[2] + '3', 4)

    while len(sentence1) <= desiredLength:
        sentence1.append(r1)
        sentence2.append(r2)
        sentence3.append(r3)

    sentence = [sentence1, sentence2, sentence3]

    return sentence

def genEndPhrase(song, scale):
    """
    Requires: song is a list of tuples which contain notes and their note values.
              the song is the generated melody.
              scale is the key in which the song is in.
    Modifies: nothing
    Effects:  returns a pleasing phrase (list) from the root notes of the scale in which the key is in,
              and appends the phrase to the end of the generated song to end the song on a pleasing note.
    """

    rootNoteList = ROOT_NOTES[scale]


    endNote = song[-1][0] #end note is the last note of song, the already generated melody. Note with octave attached to it.

    #splits the end note into components of note value and octave
    if endNote[1] == '#':
        noteValue = endNote[:2]
        octave = endNote[2]
    elif endNote[1] == 'b':
        noteValue = endNote[:2]
        octave = endNote[2]
    else:
        noteValue = endNote[0]
        octave = endNote[1]

    finalPhrase = [(rootNoteList[2] + str(octave), 2), (rootNoteList[1] + str(octave), 2), (rootNoteList[0] + str(octave), 4), (rootNoteList[0] + str(octave), 1),]
    #sample final phrase

    finalPhraseOptions = [] #list of lists, which list the options available for an ending phrase
    #will be used later

    return finalPhrase

###############################################################################
# End Core
###############################################################################

###############################################################################
# Main
###############################################################################

PROMPT = [
    'Generate song lyrics by The Beatles',
    'Generate a new national anthem for a new country, based on data from existing national anthems',
    'Quit the music generator'
]

def main():
    """
    Requires: Nothing
    Modifies: Nothing
    Effects:  This is your main function, which is done for you. It runs the
              entire generator program for both the reach and the core.

              It prompts the user to choose to generate either lyrics or music.
    """

    mainMenu = Menu(PROMPT)

    lyricsTrained = False
    musicTrained = False

    print('Welcome to the {} music generator!'.format(TEAM))
    while True:
        userInput = mainMenu.getChoice()

        if userInput == 1:
            if not lyricsTrained:
                print('Starting lyrics generator...')
                lyricsModel = trainLyricModels(LYRICSDIRS)
                lyricsTrained = True

            runLyricsGenerator(lyricsModel)

        elif userInput == 2:
            if not musicTrained:
                print('Starting music generator...')
                musicModel = trainMusicModels(MUSICDIRS)
                musicTrained = True

            songName = input('What would you like to name your melody? ')

            runMusicGenerator(musicModel, WAVDIR + songName + '.wav')

        elif userInput == 3:
            print('Thank you for using the {} music generator!'.format(TEAM))
            sys.exit()

# This is how python tells if the file is being run as main
if __name__ == '__main__':
    main()
    # note that if you want to individually test functions from this file,
    # you can comment out main() and call those functions here. Just make
    # sure to call main() in your final submission of the project!
