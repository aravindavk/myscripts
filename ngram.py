#!/usr/bin/python3

class Ngram:
    __finalList = {}

    def __rankMe(self, inp):
        if inp in self.__finalList:
            self.__finalList[inp] += 1
        else:
            self.__finalList[inp] = 1

            
    def get(self):
        print(self.__finalList)    

        
    def calculate(self, sentence, howmany):
        words = sentence.split()
        ngrams = []
        
        limit = len(words)-(howmany-1)
        for i in range(0, limit):
            self.__rankMe(" ".join(words[i:i+howmany]))
   
       

if __name__ == "__main__":
    sample = Ngram()
    sample.calculate("sample text to check ngram", 2)
    sample.calculate("script to check is fun", 2)    # some text repeats
    sample.calculate("en samachara", 2)
    sample.get()
