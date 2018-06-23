import sys
from pprint import pprint
from collections import namedtuple
from src.Trie import Trie

Review = namedtuple('Review', ['score', 'text'])
WordStats = namedtuple('WordStats', ['score_sum', 'occurrences', 'average'])

def clean_word(word):
    word = word.replace('\t', '')
    word = word.replace('\n', '')
    word = word.lower()
    word = word.replace('.', '')
    word = word.replace(',', '')

    return word


def main():
   # if len(sys.argv) != 2:
    #    sys.exit('Wrong arguments')

    if len(sys.argv) == 2:
       input_file = open(sys.argv[1], encoding='UTF-8-sig')
    else:
       print("Opening default (movieReviews.txt)...")
       input_file = open('./input/movieReviews.txt', encoding='UTF-8-sig')

    # create list of reviews associated with scores
    review_list= []
    for line in input_file:
        if line != '\n':
            review_list.append( Review(score=line[0], text=line[1:]) )

    #word_dictionary = dict() # word -> number of occurrences
    word_dictionary = Trie()
    
    for review in review_list:
        count = 1
        # composed words with hyphens are separated into different single ones
        review = Review(review.score, review.text.replace('-', ' ').split(' '))
        current_review_dict = dict()
        for word in review.text:
            word = clean_word(word)

            if word in word_dictionary:
                old_word_stats = word_dictionary[word]
                new_score_sum = int(old_word_stats.score_sum) + int(review.score)
                new_occurrences = old_word_stats.occurrences + 1
                new_average = float(new_score_sum) / new_occurrences
                new_word_stats = WordStats(new_score_sum, new_occurrences, new_average)

                word_dictionary[word] = new_word_stats
            else:
                word_dictionary[word] = WordStats(score_sum=int(review.score), \
                                                  occurrences=1, \
            # TODO: make it so that average is calculated after all insertions
                                                  average=review.score)

            #word_dictionary[word] = None
    #print(word_dictionary)
    #print('combination: ', ['combination'])
    #print(word_dictionary.get_all_words())
    print('Trie dictionary has',len(word_dictionary),'words')
    #print(word_dictionary['teste'])  #isso printa o valor atribuido à palavra teste.
    if 'bad' in word_dictionary:
        print('bad:', word_dictionary['bad'])
    if 'good' in word_dictionary:
        print('good:', word_dictionary['good'])

if __name__ == '__main__':
    main()

