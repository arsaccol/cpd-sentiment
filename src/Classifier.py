# might have to use src.Trie if importing from main.py...
from Trie import Trie 
from collections import namedtuple
import sys
from pprint import pprint

Review = namedtuple('Review', ['score', 'text'])
WordStats = namedtuple('WordStats', ['score_sum', 'occurrences', 'average_score'])

class Classifier:

    def __init__(self, filename='./input/single-words.txt'):
        self.word_stats_trie= Trie()
        self.review_list = self.get_review_list(filename)
        self.set_word_stats()

    def evaluate_sentence(self, sentence, store_absent=False):
        '''
        Calculates average of scores of all words in the sentence.
        '''
        
        total_sum = 0.0
        sentence_length = len(sentence.split())
        for word in sentence.split():
            word = self.clean_word(word)

            try:
                word_stats = self.word_stats_trie[word]
            except KeyError:
                word_stats = WordStats(score_sum=2, occurrences=1, average_score=2.0)
                if store_absent:
                    self.word_stats_trie[word] = word_stats 

            total_sum += word_stats.average_score
                
        sentence_score = total_sum / sentence_length

        return sentence_score
        

    def set_word_stats(self):
        for review in self.review_list:
            for word in review.text.split():
                if word in self.word_stats_trie:
                    old_word_stats = self.word_stats_trie[word] 

                    new_score_sum = review.score + old_word_stats.score_sum
                    new_occurrences = 1 + old_word_stats.occurrences
                    # rather than compute new_average on the fly, we should use
                    # Trie iteration on all words at a later stage
                    new_average = new_score_sum / new_occurrences

                    new_word_stats = WordStats(new_score_sum, new_occurrences, new_average)

                    self.word_stats_trie[word] = new_word_stats

                else:
                    new_stats = WordStats(score_sum=review.score, \
                                          occurrences=1, \
                                          average_score=review.score)
                    self.word_stats_trie[word] = new_stats


    def get_review_list(self, filename):
        try:
            review_file = open(filename, encoding='UTF-8-sig')
        except IOError:
            print('Could not open file', filename)
            sys.exit()
        with review_file:
            review_list = []

            for line in review_file:
                if line != '\n':
                    review = self.get_review_from_line(line)
                    review_list.append(review)

        return review_list


    def get_review_from_line(self, line):
        score = int(line.split()[0])
        text = self.clean_word(line[1:])

        return Review(score, text)
        
            
    def clean_word(self, word):
        word = word.replace('\t', '')
        word = word.replace('\n', '')
        word = word.lower()
        word = word.replace('.', '')
        word = word.replace(',', '')

        return word 

if __name__ == '__main__':

    import sys
    if len(sys.argv) == 2:
        classifier = Classifier(sys.argv[1])

    else:
        classifier = Classifier()


    all_words = classifier.word_stats_trie.get_all_words()
    for word in all_words:
        print(word, '---',  classifier.word_stats_trie[word])

    
    sentences = ['bad bad crap terrible', 'good great marvelous bright fantastic']

    print()
    for sentence in sentences:
        print(classifier.evaluate_sentence(sentence), '---', sentence)
    


