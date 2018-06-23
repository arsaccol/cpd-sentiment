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
       print("opening default(movieReviews.txt)...")
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
                aux_list = word_dictionary[word]
                aux_list[0] = (int(aux_list[0])) + (int(review.score))  #adds the score into the already existing element
                aux_list[1] = (int(aux_list[1])) + 1  #increases ocurrency number
                word_dictionary[word] = aux_list
            else:
                word_dictionary.insert(word,[review.score, 1, 0]) #review_score, ocurrencies, real_value
                                                                # (will be calculated after all insertions)

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


    input_word = input('Digite a frase ou palavra a ser calculada o score: ')
    acumulator = 0
    ocurr = 0

    for word in input_word.split():
         word = word.replace('\t', '')
         word = word.replace('\n', '')
         word = word.lower()
         word = word.replace('.', '')
         word = word.replace(',', '')
         aux = word_dictionary[word]
         acumulator = acumulator + aux[0]/aux[1]
         ocurr = ocurr + 1
    sentence_value = acumulator/ocurr
    print('phrase value = ' + (str(sentence_value)))




if __name__ == '__main__':
    main()

