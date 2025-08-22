class TernarySearchTree:
    # Tree initialization 
    def __init__(self):
        self.root = None  # Because there are no words yet
        self.word_count = 0  # Keeps track of how many words are inserted

    # Node initialization
    class Node:
        def __init__(self, char):
            self.char = char  # Letter that is stored in the node
            self.end_of_word = False  # True when the letter is the end of the word
            self._ls = None  # Next node that has a character lesser
            self._eq = None  # Next node that is the following character of the word
            self._gt = None  # Nets node that has a character greater

    # Length of the tree
    def __len__(self):
        return self.word_count  # returns number of words

    # Words inside the tree
    def all_strings(self):
        # A more efficient way to get all strings by traversing the tree
        def _collect_strings_recursive(node, path, result):
            if node:
                _collect_strings_recursive(node._ls, path, result)
                
                path.append(node.char)
                if node.end_of_word:
                    result.append("".join(path))
                _collect_strings_recursive(node._eq, path, result)
                path.pop()

                _collect_strings_recursive(node._gt, path, result)

        all_words = []
        _collect_strings_recursive(self.root, [], all_words)
        return all_words

    # Helper function for inserting words
    def insert_character(self, node, word, index):
        char = word[index]  # character to insert

        if node is None:
            node = self.Node(char)  # creates a new node if there is none already

        if char < node.char:
            node._ls = self.insert_character(node._ls, word, index)  # go left
        elif char > node.char:
            node._gt = self.insert_character(node._gt, word, index)  # go right
        else:
            if index + 1 == len(word):
                if not node.end_of_word:  # Check if a new word is being added
                    self.word_count += 1
                node.end_of_word = True  # marks as end of the word
            else:
                node._eq = self.insert_character(node._eq, word, index + 1)  # go middle

        return node

    # Insert word function
    def insert(self, word):
        if not isinstance(word, str) or not word:
            return  # doesn't insert empty strings or invalid types into the tree

        self.root = self.insert_character(self.root, word, 0)

    # Helper function for search tool
    def search_helper(self, node, word, index):
        if node is None:
            return None  # if the node doesn't exist, then the word doesn't either

        char = word[index]  # current letter to compare
        
        if char < node.char:
            return self.search_helper(node._ls, word, index)  # going to left node
        
        elif char > node.char:
            return self.search_helper(node._gt, word, index)  # going to right node
        
        else:
            if index + 1 == len(word):
                return node  # return node if last character
            return self.search_helper(node._eq, word, index + 1)  # going to middle node

    # Search tool
    def search(self, word, exact=False):
        if not isinstance(word, str) or not word:
            return False

        node = self.search_helper(self.root, word, 0)
        
        if not node:
            return False

        return node.end_of_word if exact else True

    def is_empty(self):
        return self.root is None

    def clear(self):
        self.root = None
        self.word_count = 0

    # Tree visualization
    def __str__(self):
        def _str_helper(node, prefix="    ", child=""):
            child = f"{child}:" if child else ""
            lines = [f"{child} {prefix} char: {node.char}, terminates: {node.end_of_word}"]

            if node._ls:
                lines.append(_str_helper(node._ls, prefix + "  ", "_ls"))
            if node._eq:
                lines.append(_str_helper(node._eq, prefix + "  ", "_eq"))
            if node._gt:
                lines.append(_str_helper(node._gt, prefix + "  ", "_gt"))

            return "\n".join(lines)

        if self.root is None:
            return ""
        return "terminates: False\n" + _str_helper(self.root)