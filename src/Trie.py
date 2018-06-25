# TODO: implement proper __iter__ and __next__ functions, to enable 
#       iteration over words with for
class Trie:
    '''
    Trie dictionary. Stores words associated with satellite data.

    -To insert a value, use 
            trie_object.insert(key, value) 
            or
            trie_object[key] = value

    -To iterate over the trie, use
            for word_node in trie_object:
                word_access = word_node.word
                data_access = word_node.data

        Unfortunately, these are "live" nodes from the trie itself,
         so please watch out not to alter them by assigning things.
        If you wish to alter trie contents, use insertion as described
         in the previous item.
            


    -To get a list of words beginning with a prefix, use
            words_with_prefix = trie_object.get_words_with_prefix(prefix)

    -To get (key,value) pairs corresponding to words beginning with a prefix, use
            kv_pairs_with_prefix = trie_object.get_words_with_prefix(prefix, get_data=True)
            
        (To either option, a KeyError exception will be raised if prefix is not found)



    -To get a value with a key in the trie, use
            value_storage = trie_object[key]
            (Raises KeyError if key not present) 


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
        self.word = None
    

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
        node_it.word = word
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


    def get_words_with_prefix(self, prefix, get_data=False):
        '''
        Returns a list with all words starting with the prefix.
        Raises exception KeyError if prefix is not present.
        '''
        node_it = self

        # first, we get to the node where the prefix is located
        for ch in prefix:
            if ch in node_it.children.keys():
                node_it = node_it.children[ch]
            else:
                raise KeyError('Prefix ' + '\"' + prefix + '\"' + ' not found')

        # we found the prefix node, so we return a list containing all words such that
        # they're the prefix concatenated with our node's suffixes
        # if get_data is set, we actually return a pair (words, data)
        if get_data:
            # the usage of self in this line is an inefficient hack
            # we should be able to find the data from node_it[suffix], but
            # that's not working
            return [ (prefix[:-1] + suffix, self[prefix[:-1] + suffix]) \
                     for suffix in node_it.get_all_words()  ]
        else:
            return [prefix[:-1] + suffix for suffix in node_it.get_all_words()]

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
            raise KeyError('Key '+ '\"' + key + '\" '+ ' not present.')

        if key_ok and node_it.accepts:
            return node_it.data
        else:
            raise KeyError('Key ' + '\"' + key + '\"' + ' is a prefix in the trie, but is not a valid key.')
        

    def __setitem__(self, key, value):
        self.insert(key, value)

    
    def __repr__(self, depth=0):  

        string = '__' * (depth-1) + self.char + '\t\t' + \
            'accepts: ' + str(self.accepts) + \
            '\tdata: ' + str(self.data) + '\n'

        for child in self.children.values():
            string += child.__repr__(depth+1)

        return string 
    
    def __iter__(self):
        '''
        Iterator: Trie is its own.
        '''
        self.node_it = self
        self.traversal_stack = [self.node_it]
        return self

    def __next__(self):
        '''
        Iterator step.
        '''
        while self.traversal_stack:
            self.node_it = self.traversal_stack.pop()

            if self.node_it.accepts:
                return self.node_it

            for char in reversed(sorted(self.node_it.children.keys())):
                child = self.node_it.children[char]
                self.traversal_stack.append(child)

        raise StopIteration


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

    print('Iterating over trie!')
    for accepting_node in t:
        pass
        print(accepting_node.word, '---', accepting_node.data)

    prefix = 'stopper'
    try:
        words_with_prefix = t.get_words_with_prefix(prefix)
        print('\nWords with prefix ' + '\"' + prefix + '\"' + ':')
        for word in words_with_prefix:
            print(word)
    except KeyError:
        print('Prefix', '\"' + prefix + '\"', 'not found.')


    try:
        words_and_data_with_prefix = t.get_words_with_prefix(prefix, get_data=True)
        print('\nWords and data with prefix ' + '\"' + prefix + '\"' + ':')
        for word, data in words_and_data_with_prefix:
            print(word, '=====', data)
    except KeyError:
        print('Prefix', '\"' + prefix + '\"', 'not found.')


