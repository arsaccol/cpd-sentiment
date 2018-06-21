
class Trie:
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
            # TODO: correct this so that we iterate over dict
            # keys in sorted order; this will give us a correct 
            # lexicographical sort
            for child in node.children.values():
                recursive_fn(child, all_words, current_word)
            current_word = current_word[:-1]

        # call recursive_fn defined above
        recursive_fn(self, all_words, current_word)

        return all_words
            

            

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
            raise KeyError
            return None

        if key_ok and node_it.accepts:
            return node_it.data
        else:
            print('Error: key ' + '\"' + key + '\"' + \
                  ' provided is a prefix in the trie, but isn\'t a valid key. ' +
                  'Returning None.')
            return None
            
        


        
    def __repr__(self, depth=0):  

        string = '__' * (depth-1) + self.char + '\t\t' + \
            'accepts: ' + str(self.accepts) + \
            '\tdata: ' + str(self.data) + '\n'

        for child in self.children.values():
            string += child.__repr__(depth+1)

        return string 

if __name__ == '__main__':
    t = Trie()

    t.insert('buy', 1234)
    t.insert('bull', 1234)
    t.insert('bear', 1234)
    t.insert('bid', 1234)
    t.insert('bell', 1234)
    t.insert('sell', 1234)
    t.insert('stock', 1234)
    t.insert('stop', 1234)
    t.insert('stomp', 7777)

    print(t)
    print(t['stomp'])
    print(t['sto'])

    print(t.get_all_words())

