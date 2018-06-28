import sys
from pprint import pprint
from collections import namedtuple
from Trie import Trie
from Classifier import Classifier

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
    stop_words = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your",
                 "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her",
                 "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs",
                 "themselves", "what", "which", "who", "whom", "this", "that", "these",
                 "those", "am", "is", "are", "was", "were", "be", "been", "being", "have",
                 "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and",
                 "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for",
                 "with", "about", "against", "between", "into", "through", "during", "before",
                 "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off",
                 "over", "under", "again", "further", "then", "once", "here", "there", "when", "where",
                 "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such",
                 "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will",
                 "just", "don", "should", "now"]
    
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

    input_word = ''
    while input_word != 'SAIR':
        print('Escreva uma validacao (digite SAIR para sair) : ')
        input_word = input('>> ')
        accumulator = 0
        occurr = 0
        for word in input_word.split():
            clean_word(word)
            if word not in stop_words:
                try:
                    word_stats = word_dictionary[word]
                except KeyError:
                    word_dictionary[word] = WordStats(score_sum=2, occurrences=1, average=2.0)
                    word_stats = word_dictionary[word]
            else:
                word_dictionary[word] = WordStats(score_sum=2, occurrences=1, average=2.0)
                word_stats = word_dictionary[word]
            accumulator = accumulator + word_stats.score_sum / word_stats.occurrences
            occurr = occurr + 1
            sentence_value = accumulator/occurr

        if(input_word != 'SAIR'):
            print('sentence value = ' + (str(sentence_value)))
            if (round(sentence_value)) == 0 :
                print('sentimento negativo')
            elif (round(sentence_value)) == 1 :
                print('sentimento um tanto negativo')
            elif (round(sentence_value)) == 2 :
                print('sentimento neutro')
            elif (round(sentence_value)) == 3 :
                print('sentimento um pouco positivo')
            else:
                print('sentimento positivo')

        #READING INPUT FILE FOR EVALUATION


    input_file = open('./input/kaggleInput.tsv', encoding='UTF-8-sig') #opens input file with sentences to be evaluated
    f = open('./output/kaggle.txt', "w+")   #creates output file
    f.write('PhraseId,Sentiment' + '\n')    #writes first line in output file
    input_file.readline()                   #ignores first line in input file

    comment = []
    for line in input_file:   #goes through every line
        if line != '\n':
            id=line[0:6]
            comment=line[12:]
            ##
            input_word = comment
            accumulator = 0
            occurr = 0
            for word in input_word.split():
                clean_word(word)
                if word not in stop_words:
                    try:
                        word_stats = word_dictionary[word]
                    except KeyError:
                        word_dictionary[word] = WordStats(score_sum=2, occurrences=1, average=2.0)
                        word_stats = word_dictionary[word]
                else:
                    word_dictionary[word] = WordStats(score_sum=2, occurrences=1, average=2.0)
                    word_stats = word_dictionary[word]

            accumulator = accumulator + word_stats.score_sum / word_stats.occurrences
            occurr = occurr + 1
            sentence_value = accumulator / occurr


        f.write(id + ',' + (str(int(round(sentence_value)))) + '\n') #prints phrase id and phrase sentiment
                                                                        # in output file


if __name__ == '__main__':
    main()

