# might have to use src.Trie if importing from main.py...
from Trie import Trie 
from collections import namedtuple
import sys
from pprint import pprint
import linecache

Review = namedtuple('Review', ['score', 'text'])
WordStats = namedtuple('WordStats', ['score_sum', 'occurrences', 'average_score', 'review_list'])

ReviewOccurrence = namedtuple('ReviewOccurrence', ['file_line_id', 'word_position'])
#ReviewList = namedtuple('ReviewList', [

class Classifier:
    # TODO: implement Kaggle test functionality
    '''
    Initialize with a filename, it'll extract scores for the words from sentences in 
        the input file.
    Then, call Classifier.evaluate_sentence at your leisure to evaluate sentences.
    '''

    def __init__(self, filename):
        self.review_filename = filename
        self.word_stats_trie= Trie()
        self.review_list = self.get_review_list(filename)
        self.set_word_stats()


    def get_reviews_with_word(self, word):
        '''
        Returns pairs (word_position, review_text) for every occurrence
            of the word in a review, where word_position is the word's position
            in the review, starting from 1 (not counting the score as a word), and
            review_text is the review text itself in lowercase and stripped of some 
            redundant characters.
        '''
        review_occurrences = self.word_stats_trie[word].review_list

        review_lines = [(review_id, \
                        position+1, \
                        self.clean_word(linecache.getline(self.review_filename,\
                                        review_id+1))) \
                        for review_id, position in review_occurrences]

        return review_lines

    def print_reviews_with_word(self, word, sentiment=None):
        position_review_pairs = self.get_reviews_with_word(word)

        review_counter = 0
        if not sentiment:
            print('\n=================================================================')
            print('Reviews with word ' + '\"' + word + '\":')
            for review_id, position, text in position_review_pairs:
                sentiment_val = self.evaluate_sentence(text[2:])
                print('=================================================================')
                print('Review #' + str(review_id) + '\t  Word #' + str(position) + \
                      '\t  Sentiment ' + str(sentiment_val))
                print('Text: ' + text[2:])
                print()
                review_counter += 1
                print('=================================================================')
        elif sentiment == 'Negative':
            print('\n=================================================================')
            print('Reviews with word ' + '\"' + word + '\"' + ' (negative sentiment):')
            for review_id, position, text in position_review_pairs:
                sentiment_val = self.evaluate_sentence(text[2:])
                if int(sentiment_val) < 2:
                    print('=================================================================')
                    print('Review #' + str(review_id) + '\t  Word #' + str(position) + \
                          '\t  Sentiment ' + str(sentiment_val))
                    print('Text: ' + text[2:])
                    print()
                    review_counter += 1
                    print('=================================================================')
        elif sentiment == 'Neutral':
            print('\n=================================================================')
            print('Reviews with word ' + '\"' + word + '\"' + ' (positive sentiment):')
            for review_id, position, text in position_review_pairs:
                sentiment_val = self.evaluate_sentence(text[2:])
                if int(sentiment_val) == 2:
                    print('=================================================================')
                    print('Review #' + str(review_id) + '\t  Word #' + str(position) + \
                          '\t  Sentiment ' + str(sentiment_val))
                    print('Text: ' + text[2:])
                    print()
                    review_counter += 1
                    print('=================================================================')

        elif sentiment == 'Positive':
            print('\n=================================================================')
            print('Reviews with word ' + '\"' + word + '\"' + ' (positive sentiment):')
            for review_id, position, text in position_review_pairs:
                sentiment_val = self.evaluate_sentence(text[2:])
                if int(sentiment_val) > 2:
                    print('=================================================================')
                    print('Review #' + str(review_id) + '\t  Word #' + str(position) + \
                          '\t  Sentiment ' + str(sentiment_val))
                    print('Text: ' + text[2:])
                    print()
                    review_counter += 1
                    print('=================================================================')

        return review_counter
            


    def evaluate_sentence(self, sentence, store_absent=False):
        '''
        Calculates and returns average of scores of all words in the sentence.
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
        '''
        Finds WordStats for every word in each review, and stores them
            in self.word_stats_trie.
        Requires self.get_review_list() to have been run.

        For each word we may define a WordStats.

        -WordStats.score_sum is the sum of average_scores of each occurrence of
            each our given word processed so far.

        -WordStats.occurrences is the number of times the word has been found.

        -WordStats.average_score is simply the average, score_sum divided by occurrences,
            of our given word.
        '''
        review_counter = 0
        for review in self.review_list:
            word_counter = 0
            for word in review.text.split():
                if word in self.word_stats_trie:
                    old_word_stats = self.word_stats_trie[word] 

                    new_score_sum = review.score + old_word_stats.score_sum
                    new_occurrences = 1 + old_word_stats.occurrences
                    # rather than compute new_average on the fly, we should use
                    # Trie iteration on all words at a later stage
                    new_average = new_score_sum / new_occurrences

                    # set review occurrence list for this word
                    review_list = old_word_stats.review_list
                    review_list.append(ReviewOccurrence(review_counter, word_counter))

                    new_word_stats = WordStats(new_score_sum, new_occurrences, \
                                               new_average, review_list)

                    self.word_stats_trie[word] = new_word_stats

                else:
                    new_stats = WordStats(score_sum=review.score, \
                                          occurrences=1, \
                                          average_score=review.score, \
                                          review_list=[ReviewOccurrence(review_counter, \
                                                                        word_counter)] \
                                          )
                    self.word_stats_trie[word] = new_stats

                word_counter += 1

            review_counter += 1


    def get_review_list(self, filename):
        '''
        Gets a list of Reviews.
        Bear in mind that Review.score is an integer.
        '''
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
        '''
        Gets reviews from lines of text from the input file.

        -Review.score is stored as an integer, the first "word" in the line.

        -Review.text is stored as a single string containing the review text proper.

        '''
        
        score = int(line.split()[0])
        text = self.clean_word(line[1:])

        return Review(score, text)
        
            
    def clean_word(self, word):
        '''
        Removes unwanted characters.
        '''
        word = word.replace('\t', '')
        word = word.replace('\n', '')
        word = word.lower()
        word = word.replace('.', '')
        word = word.replace(',', '')

        return word 


KaggleReview = namedtuple('KaggleReview', ['phrase_id', 'text', 'sentiment'])

# WARNING: this entire class is a big hack. Its functionality should
#          be integrated with the original Classifier class. Instead,
#          the class has lots of duplicate code from Classifier.
class KaggleClassifier:
    # ...Screw it at this point, I'll just reimplement the Classifier, 
    # only adapted to Kaggle's dataset format
    # Later I'll have to find a way to put both classes together, though.


    def __init__(self, filename='./input/train.tsv'):
        self.word_stats_trie = Trie()
        self.train_from_file_input(filename)
        self.test_from_file_input_to_output()


    def get_review(self, line, test=False):
        phrase_id = int(line.split()[0])
        text = ' '.join(line.split()[2:-1])
        if test:
            sentiment = -1
        else:
            sentiment = int(line.split()[-1])

        #print(phrase_id, '---', text, '---', sentiment)

        return KaggleReview(phrase_id=phrase_id, text=text, sentiment=sentiment)
        
    def train_from_file_input(self, filename='./input/train.tsv'):
        try:
            train_file = open(filename, encoding='UTF-8-sig')
        except IOError:
            print('Could not open training file', filename)
            sys.exit()
        with train_file:
            # skip column descriptor line
            train_file.readline() 
            for line in train_file:
                review = self.get_review(line)
                self.update_word_stats(review)
    
    def test_from_file_input_to_output(self, input_filename='./input/test.tsv'):
        output_filename = './output/' + 'results.csv'

        try:
            test_file = open(input_filename, encoding='UTF-8-sig')
            results_file = open(output_filename, 'w+')
        except IOError:
            print('Could not open test file', filename)
            sys.exit()
        with test_file, results_file:
            test_file.readline()
            results_file.write('PhraseId,Sentiment' + '\n')

            for line in test_file:
                review = self.get_review(line, test=True)
                phrase_id = review.phrase_id
                print(review.text)
                sentiment = int(self.evaluate_sentence(review.text) + 0.5)
                output_line = str(phrase_id) + ',' + str(sentiment) + '\n'

                results_file.write(output_line)
                
                



    def evaluate_sentence(self, sentence, store_absent=False):
        '''
        Calculates and returns average of scores of all words in the sentence.
        '''
        
        total_sum = 0.0
        sentence_length = len(sentence.split())
        # I'm doubtful 0-length sentences should be a thing,
        # yet there have been a few.
        if sentence_length == 0:
            return -1

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
        
        

    def update_word_stats(self, review):
        # copied straight from Classifier
        # only change is review.sentiment instead of review.score
        for word in review.text.split():
            if word in self.word_stats_trie:
                old_word_stats = self.word_stats_trie[word] 
                new_score_sum = review.sentiment + old_word_stats.score_sum
                new_occurrences = 1 + old_word_stats.occurrences
                # rather than compute new_average on the fly, we should use
                # Trie iteration on all words at a later stage
                new_average = new_score_sum / new_occurrences

                new_word_stats = WordStats(new_score_sum, new_occurrences, new_average)

                self.word_stats_trie[word] = new_word_stats

            else:
                new_stats = WordStats(score_sum=review.sentiment, \
                                      occurrences=1, \
                                      average_score=review.sentiment)
                self.word_stats_trie[word] = new_stats
            
    def clean_word(self, word):
        '''
        Removes unwanted characters.
        '''
        word = word.replace('\t', '')
        word = word.replace('\n', '')
        word = word.lower()
        word = word.replace('.', '')
        word = word.replace(',', '')

        return word 




#===================== test_classifier =====================
def test_classifier():
    import sys
    if len(sys.argv) == 2:
        # command-line arguments to avoid typing stuff over again and again
        classifier = Classifier(sys.argv[1])

    else:
        classifier = Classifier('./input/movieReviews.txt')


    all_words = classifier.word_stats_trie.get_all_words()
    for word in all_words:
        pass
        #print(word, '---',  classifier.word_stats_trie[word])

    
    sentences = ['bad bad crap terrible', 'good great marvelous bright fantastic']

    print()
    for sentence in sentences:
        print(classifier.evaluate_sentence(sentence), '---', sentence)

    significant_words = ['good', 'bad', 'crap', 'terrible', 'great', 'fantastic']
    sentiments = ['Negative', 'Neutral', 'Positive']

    for word in significant_words:
        for sentiment in sentiments:
            print()
            print('_' * 80)
            review_count = classifier.print_reviews_with_word(word, sentiment)
            print('_' * 80)
            print('Just printed ' + str(review_count) + ' reviews containing word ' + '\"' + word + '\"' + ' and ' + sentiment.lower() + ' sentiment')
            stop = input('Continue... (type \"stop\" to stop) ')
            if stop == 'stop':
                break
        if stop == 'stop':
            break

#===================== test_kaggle_classifier =====================
def test_kaggle_classifier():
    import sys
    if len(sys.argv) == 2:
        kaggle_classifier = KaggleClassifier(sys.argv[1])
    else:
        kaggle_classifier = KaggleClassifier()


if __name__ == '__main__':
    test_classifier()
    #test_kaggle_classifier()

