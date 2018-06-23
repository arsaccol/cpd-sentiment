# TODO: implement proper __iter__ and __next__ functions, to enable 
#       iteration over words with for
class Trie:
    '''
    Trie dictionary. Stores words associated with satellite data.

    -To insert a value, use 
            trie_object.insert(key, value) 
            or
            trie_object[key] = value


    -To get a value with a key in the trie, use
            value_storage = trie_object[key]
            (raises KeyError if key not present) 


    -To check if a key is present in the trie, use
            if key in trie_object:
                do_something()


    -To get a list with all keys present in the trie, use
            all_keys = trie_object.get_all_words()

    -To get the number of elements stores in the trie, do as usual:
            num_elements = len(trie_object)
    
    '''
    def __init__(self, char='', data=None):
        self.accepts = False
        self.children = dict()
        self.char = char
        self.data = data
    

    def insert(self, word, data=None):
        '''
        Inserts a word in the trie, possibly along with satellite data
        that will go in the node corresponding to the end of that word.
        '''
        node_it = self
        word_it = 0 

        # find the substring already present in the trie
        while word_it < len(word):
            char = word[word_it]
            if char in node_it.children:
                node_it = node_it.children[char]
                word_it += 1
            else:
                break

        # now is when we start adding stuff
        while word_it < len(word):
            char = word[word_it]
            node_it.children[char] = Trie(char=char)
            node_it = node_it.children[char]
            word_it += 1

        node_it.accepts = True
        node_it.data = data
        #print('word_it ', word_it, '\t node_it ', node_it)
        

    def get_all_words(self):
        all_words = []
        current_word = ''
        def recursive_fn(node, all_words, current_word):
            if node == None:
                return
            current_word += node.char
            if node.accepts:
                all_words.append(current_word)
            for character in sorted(node.children.keys()):
                child = node.children[character]
                recursive_fn(child, all_words, current_word)
            current_word = current_word[:-1]

        # call recursive_fn defined above
        recursive_fn(self, all_words, current_word)

        return all_words


    def __len__(self):
        if self.accepts:
            length = 1
        else:
            length = 0

        for child in self.children.values():
            length += child.__len__()

        return length
            

    def __contains__(self, key):
        node_it = self
        key_it = 0

        while key_it < len(key):  
            char = key[key_it]
            if char in node_it.children:
                node_it = node_it.children[char]
                key_it += 1
            else:
                break
        if key_it == len(key) and node_it.accepts:
            return True
        else:
            return False


    def __getitem__(self, key):
        node_it = self
        key_it = 0

        while key_it < len(key):  
            char = key[key_it]
            if char in node_it.children:
                node_it = node_it.children[char]
                key_it += 1
            else:
                break

        # key_it finishes with len(key), as that is
        # the condition to stop the loop
        if key_it == len(key):
            key_ok = True
        else:
            raise KeyError('Key not present.')

        if key_ok and node_it.accepts:
            return node_it.data
        else:
            raise KeyError('Key provided is a prefix in the trie, but isn\'t a valid key.')
        

    def __setitem__(self, key, value):
        self.insert(key, value)

    
    def __repr__(self, depth=0):  

        string = '__' * (depth-1) + self.char + '\t\t' + \
            'accepts: ' + str(self.accepts) + \
            '\tdata: ' + str(self.data) + '\n'

        for child in self.children.values():
            string += child.__repr__(depth+1)

        return string 


if __name__ == '__main__':
    t = Trie()

    words = ['buy', 'bull', 'bear', 'bid', 'bell',
             'sell', 'stock', 'stop', 'stomp', 'bust']

    counter = 1
    for word in words:
        t[word] = counter * 1000
        counter += 1

    t['setitem'] = {'this': 1234, 'that': 4321}

    print(t)
    print(t.get_all_words())
    print('length of trie:',len(t))

    try:
        value = t['buddy']
    except KeyError:
        print('Oops, we couldn\'t find "buddy"')

    #for word in t:
        #print(word)

