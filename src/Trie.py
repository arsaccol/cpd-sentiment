
class Trie:
    def __init__(self, char='', data=None):
        self.accepts = False
        self.children = dict()
        self.char = char
        self.data = data
    
    def insert(self, word, data=None):
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
        
        
    def __repr__(self, depth=0):  

        string = '__' * (depth-1) + self.char + '\t' + \
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
    print(t)

