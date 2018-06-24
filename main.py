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
            clean_word(word)

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
    #print('Trie dictionary has',len(word_dictionary),'words')
    #print(word_dictionary['teste'])  #isso printa o valor atribuido à palavra teste.
    #if 'bad' in word_dictionary:
    #    print(word_dictionary['bad'])
    #    listt = word_dictionary['bad']
    #    blabla = listt[0]/listt[1]
    #    print(blabla)

   # print('Trie dictionary has',len(word_dictionary),'words')
   # print(word_dictionary['teste'])  #isso printa o valor atribuido à palavra teste.
   # if 'bad' in word_dictionary:
   #    print('bad:', word_dictionary['bad'])
   # if 'good' in word_dictionary:
   #    print('good:', word_dictionary['good'])


    print('Enter the word or sentence to have its score calculated(type ESC for quitting: ')
    input_word = input('>> ')


    while input_word != 'SAIR':
        accumulator = 0
        occurr = 0
        for word in input_word.split():
            clean_word(word)
            try:
                word_stats = word_dictionary[word]
            except KeyError:
                # THIS MIGHT NOT BE DESIRED BEHAVIOR
                # we insert the word with a "neutral" average of 2.0,
                # as that is the average between the min (0) and max (4) possible values
                word_dictionary[word] = WordStats(score_sum=1, occurrences=1, average=2.0)

            accumulator = accumulator + word_stats.score_sum / word_stats.occurrences
            occurr = occurr + 1
            sentence_value = accumulator/occurr

        print('sentence value = ' + (str(sentence_value)))
        if sentence_value < 1:
            print('sentimento negativo')
        elif sentence_value < 2:
            print('sentimento um tanto negativo')
        elif sentence_value < 3:
            print('sentimento neutro')
        elif sentence_value < 4:
            print('sentimento um pouco positivo')
        else:
            print('sentimento positivo')

        print('Escreva uma valiacao (digite SAIR para sair) : ')
        input_word = input('>> ')

if __name__ == '__main__':
    main()

