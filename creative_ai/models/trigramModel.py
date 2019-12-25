from creative_ai.utils.print_helpers import ppGramJson

class TrigramModel():

    def __init__(self):
        """
        Requires: nothing
        Modifies: self (this instance of the NGramModel object)
        Effects:  This is the NGramModel constructor. It sets up an empty
                  dictionary as a member variable.

        This function is done for you.
        """

        self.nGramCounts = {}

    def __str__(self):
        """
        Requires: nothing
        Modifies: nothing
        Effects:  Returns the string to print when you call print on an
                  NGramModel object. This string will be formatted in JSON
                  and display the currently trained dataset.

        This function is done for you.
        """

        return ppGramJson(self.nGramCounts)


###############################################################################
# Begin Core >> FOR CORE IMPLEMENTION, DO NOT EDIT ABOVE OF THIS SECTION <<
###############################################################################

    def trainModel(self, text):
        """
        Requires: text is a list of lists of strings
        Modifies: self.nGramCounts, a three-dimensional dictionary. For
                  examples and pictures of the TrigramModel's version of
                  self.nGramCounts, see the spec.
        Effects:  this function populates the self.nGramCounts dictionary,
                  which has strings as keys and dictionaries as values,
                  where those inner dictionaries have strings as keys
                  and dictionaries of {string: integer} pairs as values.
                  Returns self.nGramCounts
        """

        for listWords in text:
            for i in range(len(listWords) - 2): #access first word

                #for j in range(i + 1, len(listWords) - 1): #access second word

                if listWords[i] in self.nGramCounts: #checks if first word is a existing first key in dictionary

                    if listWords[i + 1] in self.nGramCounts[listWords[i]]: #checks if second word is a existing second key in dictionary

                        if listWords[i + 2] in self.nGramCounts[listWords[i]][listWords[i + 1]]: #checks if the third word is a existing third key in dictionary
                            self.nGramCounts[listWords[i]][listWords[i + 1]][listWords[i + 2]] += 1

                        else:
                            self.nGramCounts[listWords[i]][listWords[i + 1]][listWords[i + 2]] = 1

                    else: #if second word is not an existing second key, we make a second key for the second word in dictionary

                        self.nGramCounts[listWords[i]][listWords[i + 1]] = {}
                        self.nGramCounts[listWords[i]][listWords[i + 1]][listWords[i + 2]] = 1

                else: #if first word is not an existing first key, we make a first key for the first word in the dictionary, as well as a second key

                    self.nGramCounts[listWords[i]] = {}
                    self.nGramCounts[listWords[i]][listWords[i + 1]] = {}
                    self.nGramCounts[listWords[i]][listWords[i + 1]][listWords[i + 2]] = 1

        return self.nGramCounts

    def trainingDataHasNGram(self, sentence):
        """
        Requires: sentence is a list of strings
        Modifies: nothing
        Effects:  returns True if this n-gram model can be used to choose
                  the next token for the sentence. For explanations of how this
                  is determined for the TrigramModel, see the spec.
        """

        if len(sentence) >= 3:
            if sentence[-2] in self.nGramCounts:
                if sentence[-1] in self.nGramCounts[sentence[-2]]:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def getCandidateDictionary(self, sentence):
        """
        Requires: sentence is a list of strings, and trainingDataHasNGram
                  has returned True for this particular language model
        Modifies: nothing
        Effects:  returns the dictionary of candidate next words to be added
                  to the current sentence. For details on which words the
                  TrigramModel sees as candidates, see the spec.
        """

        return self.nGramCounts[sentence[-2]][sentence[-1]]

###############################################################################
# End Core
###############################################################################

###############################################################################
# Main
###############################################################################

if __name__ == '__main__':
    # An example trainModel test case

    tri11 = TrigramModel()

    trainingTrigramModelSentence = [['very', 'hungry', 'caterpillar', 'very', 'hungry', 'kaoru']]

    tri11.trainModel(trainingTrigramModelSentence)
    print(tri11)


    tri = TrigramModel()

    text = [ ['the', 'brown', 'fox'], ['the', 'lazy', 'dog'] ]
    tri.trainModel(text)

    print(tri)

    # trainingDataHasNGram Test Case

    sentence = ['a', 'b', 'c', 'the', 'brown']

    #should print true
    print(tri.trainingDataHasNGram(sentence))

    sentence = ['a', 'b', 'c']

    #should print false
    print(tri.trainingDataHasNGram(sentence))

    #should print true
    sentence = ['the', 'brown']
    print(tri.trainingDataHasNGram(sentence))

    #should print false
    sentence = ['the']
    print(tri.trainingDataHasNGram(sentence))


    tri2 = TrigramModel()

    text = [ ['the', 'brown', 'fox'], ['the', 'lazy', 'dog'], ['the', 'lazy', 'cat'] ]

    tri2.trainModel(text)
    # {"'the'": {"'brown'": {"'fox'": 1},"'lazy'": {"'cat'": 1, "'dog'": 1}}}


    print(tri2)

    sentence = ['a', 'b', 'c', 'the', 'lazy']

    print(tri2.getCandidateDictionary(sentence))
    #{'cat' : 1, 'dog' : 1}
