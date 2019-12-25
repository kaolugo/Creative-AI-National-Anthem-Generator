from creative_ai.utils.print_helpers import ppGramJson

class BigramModel():

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
        Modifies: self.nGramCounts, a two-dimensional dictionary. For examples
                  and pictures of the BigramModel's version of
                  self.nGramCounts, see the spec.
        Effects:  this function populates the self.nGramCounts dictionary,
                  which has strings as keys and dictionaries of
                  {string: integer} pairs as values.
                  Returns self.nGramCounts
        """

        for listWords in text:
            for i in range(len(listWords) - 1):
                if listWords[i] in self.nGramCounts:
                    if listWords[i + 1] in self.nGramCounts[listWords[i]]:
                        self.nGramCounts[listWords[i]][listWords[i + 1]] += 1
                    else:
                        self.nGramCounts[listWords[i]][listWords[i + 1]] = 1

                else:
                    self.nGramCounts[listWords[i]] = {}

                    self.nGramCounts[listWords[i]][listWords[i + 1]] = 1
        return self.nGramCounts

    def trainingDataHasNGram(self, sentence):
        """
        Requires: sentence is a list of strings
        Modifies: nothing
        Effects:  returns True if this n-gram model can be used to choose
                  the next token for the sentence. For explanations of how this
                  is determined for the BigramModel, see the spec.
        """
        if len(sentence) >= 2:
            if sentence[-1] in self.nGramCounts:
                return True
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
                  BigramModel sees as candidates, see the spec.
        """
        return self.nGramCounts[sentence[-1]]

###############################################################################
# End Core
###############################################################################

###############################################################################
# Main
###############################################################################

if __name__ == '__main__':

    # trainModel test cases

    #test case #1
    bi = BigramModel()
    text = [ ['Summertime', 'and', 'the', 'livin\'s', 'easy', '$:::$' ], ['Summertime', 'and', 'the', 'livin\'s', 'easy', '$:::$' ]]
    bi.trainModel(text)
    # Should print: { 'Summertime' : {'and' : 2}, 'and' : {'the' : 2}, 'the' : {'livin'\s' : 2}, 'livin'\s' : {'easy' : 2}, 'easy' : {'$:::$' : 2}}
    print(bi)

    #test case #2
    bi = BigramModel()
    text = [['Climb', 'up', 'the', 'H', 'of', 'the', 'Hollywood', 'sign']]
    bi.trainModel(text)
    #Should print { 'Climb' : {'up' : 1}, 'up' : {'the' : 1}, 'the' : {'H' : 1, 'Hollywood' : 1}, 'H' : {'of' : 1}, 'of' : {'the' : 1}, 'Hollywood' : {'sign' : 1}}
    print(bi)

    #test case #3
    bi = BigramModel()
    text = [[]]
    bi.trainModel(text)
    #Should print {}
    print(bi)

    #test case #4
    bi = BigramModel()
    text = [['ha','ha','ha','ha','ha','ha','ha'],['ha','ha','ha','ha','ha'],['ha','ha','ha','ha']]
    bi.trainModel(text)
    #Should print {'ha' : {'ha' : 13}}
    print(bi)

    #test case #5
    bi = BigramModel()

    text = [ ['Summertime', 'and', 'the', 'livin\'s', 'easy', '$:::$' ], ['Summertime', 'and', 'the', 'livin\'s', 'easy', '$:::$' ], ['Summertime', 'sadness']]
    bi.trainModel(text)
    # Should print: { 'Summertime' : {'and' : 2, 'sadness' : 1}, 'and' : {'the' : 2}, 'the' : {'livin'\s' : 2},'livin'\s' : {'easy' : 2}, 'easy' : {'$:::$' : 2}}
    print(bi)

    # trainingDataHasNGram test cases

    #test case #1
    bi = BigramModel()
    text = [ ['Summertime', 'and', 'the', 'livin\'s', 'easy', '$:::$' ], ['Summertime', 'and', 'the', 'livin\'s', 'easy', '$:::$' ]]
    bi.trainModel(text)
    print(bi)
    sentence = ['a', 'b', 'c', 'Summertime']

    print(bi.trainingDataHasNGram(sentence))
    #should print true

    #test case #2
    sentence = ['a', 'b', 'cat']

    print(bi.trainingDataHasNGram(sentence))
    #should print false

    #test case #3
    sentence = ['a', 'b', '$:::$']

    print(bi.trainingDataHasNGram(sentence))
    #should print false


    #getCandidateDictionary test cases

    #test case #1
    bi = BigramModel()

    text = [ ['Summertime', 'and', 'the', 'livin\'s', 'easy', '$:::$' ], ['Summertime', 'and', 'the', 'livin\'s', 'easy', '$:::$' ], ['Summertime', 'sadness']]
    bi.trainModel(text)
    print(bi)

    sentence = ['a', 'b', 'c', 'Summertime']

    print(bi.getCandidateDictionary(sentence))
    # Should print {'and' : 2, 'sadness' : 1}

    #test case #2
    sentence = ['a', 'b', 'c', 'the']
    print(bi.getCandidateDictionary(sentence))
    #should print {'\"livin's\"': 2}
