import sys
from pprint import pprint
from collections import namedtuple
from src.Trie import Trie

Review = namedtuple('Review', ['score', 'text'])

def main():
   # if len(sys.argv) != 2:
    #    sys.exit('Wrong arguments')

    if len(sys.argv) == 2:
       input_file = open(sys.argv[1], encoding='UTF-8-sig')
    else:
       print("opening default(movieReviews.txt")
       input_file = open('./input/movieReviews.txt', encoding='UTF-8-sig')

    # create list of reviews associated with scores
    review_list= []
    for line in input_file:
        review_list.append( Review(score=line[0], text=line[1:]) )

    #word_dictionary = dict() # word -> number of occurrences
    word_dictionary = Trie()
    
    for review in review_list:
        count = 1
        # composed words with hyphens are separated into different single ones
        review = Review(review.score, review.text.replace('-', ' ').split(' '))
        current_review_dict = dict()
        for word in review.text:
            word = word.replace('\t', '')
            word = word.replace('\n', '')
            word = word.lower()
            word = word.replace('.', '')
            word = word.replace(',', '')
            '''
            if word not in current_review_dict:
                current_review_dict[word] = []
            else:
                current_review_dict[word].append(review.score)
            '''
            if word in word_dictionary:
                #add 1 in number of ocurrencies
                print(word)
            else:
                word_dictionary.insert(word, review.score)
                #sets word value
                #sets number of ocurrencies to 1

            #word_dictionary[word] = None

    #print(word_dictionary)
    #print('combination: ', ['combination'])
    #print(word_dictionary.get_all_words())
    print('Trie dictionary has',len(word_dictionary),'words')


if __name__ == '__main__':
    main()

