from creative_ai.utils.print_helpers import ppGramJson

class UnigramModel():

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
        Modifies: self.nGramCounts
        Effects:  this function populates the self.nGramCounts dictionary,
                  which is a dictionary of {string: integer} pairs.
                  For further explanation of UnigramModel's version of
                  self.nGramCounts, see the spec.
                  Returns self.nGramCounts
        """
        for unigram in text:
            for word in unigram:

                if word in self.nGramCounts:
                    self.nGramCounts[word] = self.nGramCounts[word] + 1
                else:
                    self.nGramCounts[word] = 1

        return self.nGramCounts

    def trainingDataHasNGram(self, sentence):
        """
        Requires: sentence is a list of strings
        Modifies: nothing
        Effects:  returns True if this n-gram model can be used to choose
                  the next token for the sentence. For explanations of how this
                  is determined for the UnigramModel, see the spec.
        """
        if self.nGramCounts:
            return True
        else:
            return False

    def getCandidateDictionary(self, sentence):
        """
        Requires: sentence is a list of strings, and trainingDataHasNGram
                  has returned True for this particular language model
        Modifies: nothing
        Effects:  returns the dictionary of candidate next words to be added
                  to the current sentence. For details on which words the
                  UnigramModel sees as candidates, see the spec.
        """
        return self.nGramCounts

###############################################################################
# End Core
###############################################################################

###############################################################################
# Main
###############################################################################

# This is the code python runs when unigramModel.py is run as main
if __name__ == '__main__':

    # trainModel test cases
    
    #test case #1
    uni = UnigramModel()
    text = [ [ 'brown' ] ]
    uni.trainModel(text)
    # Should print: { 'brown' : 1 }
    print(uni)

    #test case #2
    text = [ ['the', 'brown', 'fox'], ['the', 'lazy', 'dog'] ]
    uni.trainModel(text)
    # Should print: { 'brown': 2, 'dog': 1, 'fox': 1, 'lazy': 1, 'the': 2 }
    print(uni)
    
    #test case #3
    text = [[]]
    uni.trainModel(text)
    # Should print: { 'brown': 2, 'dog': 1, 'fox': 1, 'lazy': 1, 'the': 2 }
    print(uni)
    
    #test case #4
    text = [[]]
    uni1 = UnigramModel()
    uni1.trainModel(text)
    #should print {}
    print(uni1)
    
    #test case #5
    text = [['^::^', '^:::^', 'Climb', 'up', 'the', 'H', 'of', 'the', 'Hollywood', 'sign', '$:::$'], ['In', 'these', 'stolen', 'moments']]
    uni1.trainModel(text)
    #should print {"'$:::$'": 1,"'Climb'": 1,"'H'": 1,"'Hollywood'": 1,"'In'": 1,"'^:::^'": 1,"'^::^'": 1,"'moments'": 1,"'of'": 1,"'sign'": 1,"'stolen'": 1,"'the'": 2,"'these'": 1,"'up'": 1}
    print(uni1)

    # trainingDataHasNGram test cases
    
    #test case #1
    uni = UnigramModel()
    sentence = "Eagles fly in the sky"
    print(uni.trainingDataHasNGram(sentence)) # should be False
    
    #test case #2
    uni.trainModel(text)
    print(uni.trainingDataHasNGram(sentence)) # should be True
    
    # getCandidateDictionary test cases
    
    #test case #1
    uni = UnigramModel()
    text = [['move', 'bilch'], ['get', 'out', 'the', 'way']]
    uni.trainModel(text)
    
    sentence = "Kaoru wants to test this function"
    #should print {'bilch' : 1, 'get' : 1, 'move' : 1, 'out' : 1, 'the' : 1, 'way' : 1}
    print(uni.getCandidateDictionary(sentence))
    
