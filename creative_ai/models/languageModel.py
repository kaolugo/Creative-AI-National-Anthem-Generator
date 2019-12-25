import random
from creative_ai.data.dataLoader import prepData
from creative_ai.models.unigramModel import UnigramModel
from creative_ai.models.bigramModel import BigramModel
from creative_ai.models.trigramModel import TrigramModel
from creative_ai.utils.print_helpers import key_value_pairs

class LanguageModel():

    def __init__(self, models=None):
        """
        Requires: nothing
        Modifies: self (this instance of the LanguageModel object)
        Effects:  This is the LanguageModel constructor. It sets up an empty
                  dictionary as a member variable.

        This function is done for you.
        """

        if models != None:
            self.models = models
        else:
            self.models = [TrigramModel(), BigramModel(), UnigramModel()]

    def __str__(self):
        """
        Requires: nothing
        Modifies: nothing
        Effects:  This is a string overloaded. This function is
                  called when languageModel is printed.
                  It will show the number of trained paths
                  for each model it contains. It may be
                  useful for testing.

        This function is done for you.
        """

        output_list = [
            '{} contains {} trained paths.'.format(
                model.__class__.__name__, key_value_pairs(model.nGramCounts)
                ) for model in self.models
            ]

        output = '\n'.join(output_list)

        return output

    def updateTrainedData(self, text, prepped=True):
        """
        Requires: text is a 2D list of strings
        Modifies: self (this instance of the LanguageModel object)
        Effects:  adds new trained data to each of the languageModel models.
        If this data is not prepped (prepped==False) then it is prepepd first
        before being passed to the models.

        This function is done for you.
        """

        if (not prepped):
            text = prepData(text)

        for model in self.models:
            model.trainModel(text)

###############################################################################
# Begin Core >> FOR CORE IMPLEMENTION, DO NOT EDIT ABOVE OF THIS SECTION <<
###############################################################################

    def selectNGramModel(self, sentence):
        """
        Requires: self.models is a list of NGramModel objects sorted by descending
                  priority: tri-, then bi-, then unigrams.

                  sentence is a list of strings.
        Modifies: nothing
        Effects:  returns the best possible model that can be used for the
                  current sentence based on the n-grams that the models know.
                  (Remember that you wrote a function that checks if a model can
                  be used to pick a word for a sentence!)
        """
        if self.models[0].trainingDataHasNGram(sentence):
            return self.models[0]
        elif self.models[1].trainingDataHasNGram(sentence):
            return self.models[1]
        elif self.models[2].trainingDataHasNGram(sentence):
            return self.models[2]
        else:
            return self.models[2]

    def weightedChoice(self, candidates):
        """
        Requires: candidates is a dictionary; the keys of candidates are items
                  you want to choose from and the values are integers
        Modifies: nothing
        Effects:  returns a candidate item (a key in the candidates dictionary)
                  based on the algorithm described in the spec.
        """
        # makes two lists from keys and values of candidates
        tokens = list(candidates.keys())
        counts = list(candidates.values())

        # makes empty cumulative list and total counter
        cumcounts = []
        total = 0

        # makes cumulative count list (of values)
        for value in counts:
            total = total + value
            cumcounts.append(total)

        randNum = random.randrange(0, cumcounts[-1])

        # walk through token list and returns correct value
        for i in range(len(tokens)):
            if cumcounts[i] > randNum:
                return tokens[i]

    def checkNoteDistance(self, sentence, note):
        """
        Requires: sentence is a pre-chosen list of strings, and this model can
                  be used to check the validity of a note, which is a tuple.
        Modifies: nothing
        Effects:  returns a boolean value of whether the next note is valid
                  with regards to distance from previous note based on our
                  own "weighted" algorithm.
        """
        #determines if the jump from first note to second note is short range,
        #mid range, or long range ("big jump")
        noteRange = ['big', 'mid', 'short']
        frequency = [1, 5, 20]

        #implements different probabilities for the three jumps
        randNum = random.randrange(0, 19)

        for i in range(len(noteRange)):
            if frequency[i] > randNum:
                #length is the chosen range
                length = noteRange[i]

        #takes the last element (which is a tuple) of the "sentence" parameter and splits into components of 'noteValue' & 'octave' to prep the data for use as parameters in function, genListOfNotes

        if sentence[-1] == '^::^' or sentence[-1] == '^:::^':
            return True
        elif sentence[-1][0][1] == '#':
            noteValue = sentence[-1][0][:2]
            octave = sentence[-1][0][2]
        elif sentence[-1][0][1] == 'b':
            noteValue = sentence[-1][0][:2]
            octave = sentence[-1][0][2]
        else:
            noteValue = sentence[-1][0][0]
            octave = sentence[-1][0][1]

        #generate list of subsequent notes centering around the note in question
        upperAndLower = self.genListOfNotes(noteValue, octave)
        upper = upperAndLower[0]
        lower = upperAndLower[1]

        #use new function, genListOfNotes here
        #returns booleans
        if length == 'big':
            for i in range(14, 18):
                if upper[i] == note[0] or lower[i] == note[0]:
                    return True
                else:
                    return False
        elif length == 'mid':
            for i in range(8, 14):
                if upper[i] == note[0] or lower[i] == note[0]:
                    return True
                else:
                    return False
        elif length == 'short':
            for i in range(0, 8):
                if upper[i] == note[0] or lower[i] == note[0]:
                    return True
                else:
                    return False

    def genListOfNotes(self, note, octave):
        """
        Requires: note is a string that indicates the note in question (ex: C, C#) and octave is an int that symbolizes the octave in which the note is at.
        Modifies: nothing
        Effects:  returns two lists of notes as a tuple. The first list contains notes that are within 7 whole steps below the note. The second list contains notes that are within 7 whole steps above the note. The original note will always be the first element in each of these lists.
        """

        if note == 'a':
            upper = ['a', 'a#', 'bb', 'b', 'c', 'c#', 'db', 'd', 'd#', 'eb', 'e', 'f', 'f#', 'gb', 'g', 'g#', 'ab', 'a']
            lower = ['a', 'ab', 'g#', 'g', 'gb', 'f#', 'f', 'e', 'eb', 'd#', 'd', 'db', 'c#', 'c', 'b', 'bb', 'a#', 'a']

            #adding the octave value for each note
            for upperNote in range(len(upper) - 2):
                upper[upperNote] = upper[upperNote] + str(octave)

            for upperNote in range(len(upper) - 2, len(upper)):
                upper[upperNote] = upper[upperNote] + str(octave + 1)

            for lowerNote in range(2, len(lower)):
                lower[lowerNote] = lower[lowerNote] + str(octave - 1)

            for lowerNote in range(2):
                lower[lowerNote] = lower[lowerNote] + str(octave)


        elif note == 'a#':
            upper = ['a#', 'bb', 'b', 'c', 'c#', 'db', 'd', 'd#', 'eb', 'e', 'f', 'f#', 'gb', 'g', 'g#', 'ab', 'a', 'a#']
            lower = ['a#', 'a', 'ab', 'g#', 'g', 'gb', 'f#', 'f', 'e', 'eb', 'd#', 'd', 'db', 'c#', 'c', 'b', 'bb', 'a#']

            for upperNote in range(len(upper) - 3):
                upper[upperNote] = upper[upperNote] + str(octave)

            for upperNote in range(len(upper) - 3, len(upper)):
                upper[upperNote] = upper[upperNote] + str(octave + 1)

            for lowerNote in range(3, len(lower)):
                lower[lowerNote] = lower[lowerNote] + str(octave - 1)

            for lowerNote in range(3):
                lower[lowerNote] = lower[lowerNote] + str(octave)


        elif note == 'bb':
            upper = ['bb', 'b', 'c', 'c#', 'db', 'd', 'd#', 'eb', 'e', 'f', 'f#', 'gb', 'g', 'g#', 'ab', 'a', 'a#', 'bb']
            lower = ['bb', 'a#', 'a', 'ab', 'g#', 'g', 'gb', 'f#', 'f', 'e', 'eb', 'd#', 'd', 'db', 'c#', 'c', 'b', 'bb']

            for upperNote in range(len(upper) - 4):
                upper[upperNote] = upper[upperNote] + str(octave)

            for upperNote in range(len(upper) - 4, len(upper)):
                upper[upperNote] = upper[upperNote] + str(octave + 1)

            for lowerNote in range(4, len(lower)):
                lower[lowerNote] = lower[lowerNote] + str(octave - 1)

            for lowerNote in range(4):
                lower[lowerNote] = lower[lowerNote] + str(octave)


        elif note == 'b':
            upper = ['b', 'c', 'c#', 'db', 'd', 'd#', 'eb', 'e', 'f', 'f#', 'gb', 'g', 'g#', 'ab', 'a', 'a#', 'bb', 'b']
            lower = ['b', 'bb', 'a#', 'a', 'ab', 'g#', 'g', 'gb', 'f#', 'f', 'e', 'eb', 'd#', 'd', 'db', 'c#', 'c', 'b']

            for upperNote in range(len(upper) - 5):
                upper[upperNote] = upper[upperNote] + str(octave)

            for upperNote in range(len(upper) - 5, len(upper)):
                upper[upperNote] = upper[upperNote] + str(octave + 1)

            for lowerNote in range(5, len(lower)):
                lower[lowerNote] = lower[lowerNote] + str(octave - 1)

            for lowerNote in range(5):
                lower[lowerNote] = lower[lowerNote] + str(octave)

        elif note == 'c':
            upper = ['c', 'c#', 'db', 'd', 'd#', 'eb', 'e', 'f', 'f#', 'gb', 'g', 'g#', 'ab', 'a', 'a#', 'bb', 'b', 'c']
            lower = ['c', 'b', 'bb', 'a#', 'a', 'ab', 'g#', 'g', 'gb', 'f#', 'f', 'e', 'eb', 'd#', 'd', 'db', 'c#', 'c']

            for upperNote in range(len(upper) - 6):
                upper[upperNote] = upper[upperNote] + str(octave)

            for upperNote in range(len(upper) - 6, len(upper)):
                upper[upperNote] = upper[upperNote] + str(octave + 1)

            for lowerNote in range(6, len(lower)):
                lower[lowerNote] = lower[lowerNote] + str(octave - 1)

            for lowerNote in range(6):
                lower[lowerNote] = lower[lowerNote] + str(octave)

        elif note == 'c#':
            upper = ['c#', 'db', 'd', 'd#', 'eb', 'e', 'f', 'f#', 'gb', 'g', 'g#', 'ab', 'a', 'a#', 'bb', 'b', 'c', 'c#']
            lower = ['c#', 'c', 'b', 'bb', 'a#', 'a', 'ab', 'g#', 'g', 'gb', 'f#', 'f', 'e', 'eb', 'd#', 'd', 'db', 'c#']

            for upperNote in range(len(upper) - 6):
                upper[upperNote] = upper[upperNote] + str(octave)

            for upperNote in range(len(upper) - 6, len(upper)):
                upper[upperNote] = upper[upperNote] + str(octave + 1)

            for lowerNote in range(6, len(lower)):
                lower[lowerNote] = lower[lowerNote] + str(octave - 1)

            for lowerNote in range(6):
                lower[lowerNote] = lower[lowerNote] + str(octave)


        elif note == 'db':
            upper = ['db', 'd', 'd#', 'eb', 'e', 'f', 'f#', 'gb', 'g', 'g#', 'ab', 'a', 'a#', 'bb', 'b', 'c', 'c#', 'db']
            lower = ['db', 'c#', 'c', 'b', 'bb', 'a#', 'a', 'ab', 'g#', 'g', 'gb', 'f#', 'f', 'e', 'eb', 'd#', 'd', 'db']

            for upperNote in range(len(upper) - 7):
                upper[upperNote] = upper[upperNote] + str(octave)

            for upperNote in range(len(upper) - 7, len(upper)):
                upper[upperNote] = upper[upperNote] + str(octave + 1)

            for lowerNote in range(7, len(lower)):
                lower[lowerNote] = lower[lowerNote] + str(octave - 1)

            for lowerNote in range(7):
                lower[lowerNote] = lower[lowerNote] + str(octave)

        elif note == 'd':
            upper = ['d', 'd#', 'eb', 'e', 'f', 'f#', 'gb', 'g', 'g#', 'ab', 'a', 'a#', 'bb', 'b', 'c', 'c#', 'db', 'd']
            lower = ['d', 'db', 'c#', 'c', 'b', 'bb', 'a#', 'a', 'ab', 'g#', 'g', 'gb', 'f#', 'f', 'e', 'eb', 'd#', 'd']

            for upperNote in range(len(upper) - 8):
                upper[upperNote] = upper[upperNote] + str(octave)

            for upperNote in range(len(upper) - 8, len(upper)):
                upper[upperNote] = upper[upperNote] + str(octave + 1)

            for lowerNote in range(8, len(lower)):
                lower[lowerNote] = lower[lowerNote] + str(octave - 1)

            for lowerNote in range(8):
                lower[lowerNote] = lower[lowerNote] + str(octave)

        elif note == 'd#':
            upper = ['d#', 'eb', 'e', 'f', 'f#', 'gb', 'g', 'g#', 'ab', 'a', 'a#', 'bb', 'b', 'c', 'c#', 'db', 'd', 'd#']
            lower = ['d#', 'd', 'db', 'c#', 'c', 'b', 'bb', 'a#', 'a', 'ab', 'g#', 'g', 'gb', 'f#', 'f', 'e', 'eb', 'd#']

            for upperNote in range(len(upper) - 9):
                upper[upperNote] = upper[upperNote] + str(octave)

            for upperNote in range(len(upper) - 9, len(upper)):
                upper[upperNote] = upper[upperNote] + str(octave + 1)

            for lowerNote in range(9, len(lower)):
                lower[lowerNote] = lower[lowerNote] + str(octave - 1)

            for lowerNote in range(9):
                lower[lowerNote] = lower[lowerNote] + str(octave)


        elif note == 'eb':
            upper = ['eb', 'e', 'f', 'f#', 'gb', 'g', 'g#', 'ab', 'a', 'a#', 'bb', 'b', 'c', 'c#', 'db', 'd', 'd#', 'eb']
            lower = ['eb', 'd#', 'd', 'db', 'c#', 'c', 'b', 'bb', 'a#', 'a', 'ab', 'g#', 'g', 'gb', 'f#', 'f', 'e', 'eb']

            for upperNote in range(len(upper) - 10):
                upper[upperNote] = upper[upperNote] + str(octave)

            for upperNote in range(len(upper) - 10, len(upper)):
                upper[upperNote] = upper[upperNote] + str(octave + 1)

            for lowerNote in range(10, len(lower)):
                lower[lowerNote] = lower[lowerNote] + str(octave - 1)

            for lowerNote in range(10):
                lower[lowerNote] = lower[lowerNote] + str(octave)

        elif note == 'e':
            upper = ['e', 'f', 'f#', 'gb', 'g', 'g#', 'ab', 'a', 'a#', 'bb', 'b', 'c', 'c#', 'db', 'd', 'd#', 'eb', 'e']
            lower = ['e', 'eb', 'd#', 'd', 'db', 'c#', 'c', 'b', 'bb', 'a#', 'a', 'ab', 'g#', 'g', 'gb', 'f#', 'f', 'e']

            for upperNote in range(len(upper) - 11):
                upper[upperNote] = upper[upperNote] + str(octave)

            for upperNote in range(len(upper) - 11, len(upper)):
                upper[upperNote] = upper[upperNote] + str(octave + 1)

            for lowerNote in range(11, len(lower)):
                lower[lowerNote] = lower[lowerNote] + str(octave - 1)

            for lowerNote in range(11):
                lower[lowerNote] = lower[lowerNote] + str(octave)

        elif note == 'f':
            upper = ['f', 'f#', 'gb', 'g', 'g#', 'ab', 'a', 'a#', 'bb', 'b', 'c', 'c#', 'db', 'd', 'd#', 'eb', 'e', 'f']
            lower = ['f', 'e', 'eb', 'd#', 'd', 'db', 'c#', 'c', 'b', 'bb', 'a#', 'a', 'ab', 'g#', 'g', 'gb', 'f#', 'f']

            for upperNote in range(len(upper) - 12):
                upper[upperNote] = upper[upperNote] + str(octave)

            for upperNote in range(len(upper) - 12, len(upper)):
                upper[upperNote] = upper[upperNote] + str(octave + 1)

            for lowerNote in range(12, len(lower)):
                lower[lowerNote] = lower[lowerNote] + str(octave - 1)

            for lowerNote in range(12):
                lower[lowerNote] = lower[lowerNote] + str(octave)

        elif note == 'f#':
            upper = ['f#', 'gb', 'g', 'g#', 'ab', 'a', 'a#', 'bb', 'b', 'c', 'c#', 'db', 'd', 'd#', 'eb', 'e', 'f', 'f#']
            lower = ['f#', 'f', 'e', 'eb', 'd#', 'd', 'db', 'c#', 'c', 'b', 'bb', 'a#', 'a', 'ab', 'g#', 'g', 'gb', 'f#']

            for upperNote in range(len(upper) - 13):
                upper[upperNote] = upper[upperNote] + str(octave)

            for upperNote in range(len(upper) - 13, len(upper)):
                upper[upperNote] = upper[upperNote] + str(octave + 1)

            for lowerNote in range(13, len(lower)):
                lower[lowerNote] = lower[lowerNote] + str(octave - 1)

            for lowerNote in range(13):
                lower[lowerNote] = lower[lowerNote] + str(octave)

        elif note == 'gb':
            upper = ['gb', 'g', 'g#', 'ab', 'a', 'a#', 'bb', 'b', 'c', 'c#', 'db', 'd', 'd#', 'eb', 'e', 'f', 'f#', 'gb']
            lower = ['gb', 'f#', 'f', 'e', 'eb', 'd#', 'd', 'db', 'c#', 'c', 'b', 'bb', 'a#', 'a', 'ab', 'g#', 'g', 'gb']

            for upperNote in range(len(upper) - 14):
                upper[upperNote] = upper[upperNote] + str(octave)

            for upperNote in range(len(upper) - 14, len(upper)):
                upper[upperNote] = upper[upperNote] + str(octave + 1)

            for lowerNote in range(14, len(lower)):
                lower[lowerNote] = lower[lowerNote] + str(octave - 1)

            for lowerNote in range(14):
                lower[lowerNote] = lower[lowerNote] + str(octave)

        elif note == 'g':
            upper = ['g', 'g#', 'ab', 'a', 'a#', 'bb', 'b', 'c', 'c#', 'db', 'd', 'd#', 'eb', 'e', 'f', 'f#', 'gb', 'g']
            lower = ['g', 'gb', 'f#', 'f', 'e', 'eb', 'd#', 'd', 'db', 'c#', 'c', 'b', 'bb', 'a#', 'a', 'ab', 'g#', 'g']

            for upperNote in range(len(upper) - 15):
                upper[upperNote] = upper[upperNote] + str(octave)

            for upperNote in range(len(upper) - 15, len(upper)):
                upper[upperNote] = upper[upperNote] + str(octave + 1)

            for lowerNote in range(15, len(lower)):
                lower[lowerNote] = lower[lowerNote] + str(octave - 1)

            for lowerNote in range(15):
                lower[lowerNote] = lower[lowerNote] + str(octave)

        elif note == 'g#':
            upper = ['g#', 'ab', 'a', 'a#', 'bb', 'b', 'c', 'c#', 'db', 'd', 'd#', 'eb', 'e', 'f', 'f#', 'gb', 'g', 'g#']
            lower = ['g#', 'g', 'gb', 'f#', 'f', 'e', 'eb', 'd#', 'd', 'db', 'c#', 'c', 'b', 'bb', 'a#', 'a', 'ab', 'g#']

            for upperNote in range(len(upper) - 16):
                upper[upperNote] = upper[upperNote] + str(octave)

            for upperNote in range(len(upper) - 16, len(upper)):
                upper[upperNote] = upper[upperNote] + str(octave + 1)

            for lowerNote in range(16, len(lower)):
                lower[lowerNote] = lower[lowerNote] + str(octave - 1)

            for lowerNote in range(16):
                lower[lowerNote] = lower[lowerNote] + str(octave)

        elif note == 'ab':
            upper = ['ab', 'a', 'a#', 'bb', 'b', 'c', 'c#', 'db', 'd', 'd#', 'eb', 'e', 'f', 'f#', 'gb', 'g', 'g#', 'ab']
            lower = ['ab', 'g#', 'g', 'gb', 'f#', 'f', 'e', 'eb', 'd#', 'd', 'db', 'c#', 'c', 'b', 'bb', 'a#', 'a', 'ab']

            for upperNote in range(len(upper) - 17):
                upper[upperNote] = upper[upperNote] + str(octave)

            for upperNote in range(len(upper) - 17, len(upper)):
                upper[upperNote] = upper[upperNote] + str(octave + 1)

            for lowerNote in range(17, len(lower)):
                lower[lowerNote] = lower[lowerNote] + str(octave - 1)

            for lowerNote in range(17):
                lower[lowerNote] = lower[lowerNote] + str(octave)

        return (upper, lower)

    def getNextToken(self, sentence, filter=None):
        """
        Requires: sentence is a list of strings, and this model can be used to
                  choose the next token for the current sentence
        Modifies: nothing
        Effects:  returns the next token to be added to sentence by calling
                  the getCandidateDictionary and weightedChoice functions.
                  For more information on how to put all these functions
                  together, see the spec.

                  If a filter is being used, and none of the models
                  can produce a next token using the filter, then a random
                  token from the filter is returned instead.
        """
        nGramModel = self.selectNGramModel(sentence)

        if filter == None:
            candidateDictionary = nGramModel.getCandidateDictionary(sentence)
            candidateWord = self.weightedChoice(candidateDictionary)
            return candidateWord

        else: #if filter is not None
            candidateDictionary = nGramModel.getCandidateDictionary(sentence)

            filteredCandidates = {}

            # cycle thru candidateDictionary to check that the word chosen is in the filter (ie, the scale that was chosen)
            for key in candidateDictionary:
                for note in filter:
                    if note in key: #[:2]
                        if self.checkNoteDistance(sentence, note):
                            filteredCandidates[key] = candidateDictionary[key]
                #if key in filter:
                    #filteredCandidates[key] = candidateDictionary[key]

            # if dictionary is empty or not...
            if filteredCandidates:
                return self.weightedChoice(filteredCandidates)
            else:
                #choose a random duration for the note
                #2nd half of the resulting tuple
                noteValues = [2, 4, 8, -2, -4, -8]
                noteValue = random.randint(0, 5)

                #choose a random octave for the note to be in
                octave = random.randint(2, 5)

                #combine generated random note & octave
                note = random.choice(filter) + str(octave)


                #keep generating random notes until it fits the criteria
                while not self.checkNoteDistance(sentence, note):
                    octave = random.randint(3, 5)
                    note = random.choice(filter) + str(octave)

                randomWordInFilter = (note, noteValues[noteValue])
                return randomWordInFilter

###############################################################################
# End Core
###############################################################################

###############################################################################
# Main
###############################################################################

if __name__ == '__main__':

    # tests for weightedChoice
    lang = LanguageModel()
    candidates = {'Arthur' : 3, 'Bill' : 2, 'Charlie' : 5, 'Dave' : 3}
    print(lang.weightedChoice(candidates))

    candidates = {'hi' : 2, 'hello' : 3, 'hey' : 5}
    print(lang.weightedChoice(candidates))

    candidates = {'orange' : 6, 'apple' : 1, 'banana' : 3}
    print(lang.weightedChoice(candidates))

    candidates = {'orange' : 6, 'apple' : 10, 'banana' : 3}
    print(lang.weightedChoice(candidates))

    # tests for selectNGramModel
    triModel = TrigramModel()
    biModel = BigramModel()
    uniModel = UnigramModel()

    learningModels = [triModel, biModel, uniModel]

    lang = LanguageModel(learningModels)

    # training sentences
    s1 = [['very', 'hungry', 'caterpillar', 'very', 'hungry', 'kaoru']]
    s2 = [['sun', 'and', 'a', 'moon']]
    s3 = [['game', 'cube']]
    s4 = [['hello']]

    # train models
    learningModels[0].trainModel(s1)
    learningModels[1].trainModel(s2)
    learningModels[1].trainModel(s3)
    learningModels[2].trainModel(s4)

    # expected: trigram
    sentence = ['Hello', 'I', 'am', 'very', 'hungry']
    print(lang.selectNGramModel(sentence))

    # expected: bigram
    sentence = ['Here', 'comes', 'the', 'sun']
    print(lang.selectNGramModel(sentence))

    # expected: bigram ??
    sentence = ['Wicked', 'game']
    print(lang.selectNGramModel(sentence))

    # expected: unigram
    sentence = ['hello']
    print(lang.selectNGramModel(sentence))

    #tests for getNextToken
    filter = None
    sentence = ['Hello', 'how', 'are', 'you', 'doing']
    print(lang.getNextToken(sentence))

    sentence = ['Dragged', 'down', 'by', 'the', 'stone']
    print(lang.getNextToken(sentence))

    sentence = ['Today', 'I', 'went']
    print(lang.getNextToken(sentence))
