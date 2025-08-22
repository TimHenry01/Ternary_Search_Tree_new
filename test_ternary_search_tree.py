import unittest
import sys
import os

# Add the parent directory to the path to import our module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ternary_search_tree import TernarySearchTree

# Test cases for TernarySearchTree class.
class TestTernarySearchTree(unittest.TestCase):
    
    # Set up test fixtures before each test method.
    def setUp(self):
        self.tst = TernarySearchTree()
        # Words to insert from the provided file
        self.words_to_insert = ["combine", "combinations", "combination", "combined", "combines", "ducks", "ducked", "duck", "futile", "futility", "future", "fontain", "font", "far", "a", "the", "their", "therefor", "there", "bomb"]
        # Words not to insert from the provided file
        self.words_not_to_insert = ["futures", "fontains", "alphabet", "gamma", "monster", "test"]

    # Test inserting a single word.
    def test_insert_single_word(self):
        self.tst.insert("hello")
        self.assertEqual(len(self.tst), 1)
        self.assertTrue(self.tst.search("hello", exact=True))
    
    # Test inserting multiple words and verifying counts.
    def test_insert_multiple_words(self):
        for word in self.words_to_insert:
            self.tst.insert(word)
        
        # The number of unique words from the file
        unique_words = len(set(self.words_to_insert))
        self.assertEqual(len(self.tst), unique_words)
    
    # Test that duplicate words are not inserted as new entries.
    def test_insert_duplicate_words(self):
        self.tst.insert("hello")
        self.tst.insert("hello")  # Duplicate
        
        self.assertEqual(len(self.tst), 1)
        self.assertTrue(self.tst.search("hello", exact=True))
    
    # Test searching for words that exist, using an exact match.
    def test_search_existing_words(self):
        for word in self.words_to_insert:
            self.tst.insert(word)
        
        for word in self.words_to_insert:
            self.assertTrue(self.tst.search(word, exact=True))
            
    # Test searching for prefixes of words that exist.
    def test_search_for_prefixes(self):
        self.tst.insert("application")
        self.assertTrue(self.tst.search("app", exact=False))
        self.assertTrue(self.tst.search("appl", exact=False))
        self.assertFalse(self.tst.search("appli", exact=True)) # 'appli' is a prefix, not a full word
    
    # Test searching for words that don't exist in the tree.
    def test_search_non_existing_words(self):
        for word in self.words_to_insert:
            self.tst.insert(word)
        
        for word in self.words_not_to_insert:
            self.assertFalse(self.tst.search(word, exact=True))
            self.assertFalse(self.tst.search(word, exact=False))
    
    # Test search with invalid input.
    def test_search_invalid_input(self):
        self.assertFalse(self.tst.search(""))
        self.assertFalse(self.tst.search(None))
        self.tst.insert("hello")
        # Ensure searching for None or an integer doesn't cause an error
        self.assertFalse(self.tst.search(123))
        self.assertFalse(self.tst.search(None))
    
    # Test retrieving all strings from the tree.
    def test_all_strings(self):
        for word in self.words_to_insert:
            self.tst.insert(word)
        
        all_words = self.tst.all_strings()
        self.assertEqual(set(all_words), set(self.words_to_insert))
    
    # Test edge cases from the notebook and other scenarios.
    def test_notebook_edge_cases(self):
        self.tst.insert('abc')
        self.tst.insert('aqt')
        
        # Test search for prefixes and non-existent words
        self.assertTrue(self.tst.search('ab'))
        self.assertFalse(self.tst.search('ac'))
        
        # Test empty string insertion
        self.tst.insert('')
        self.assertEqual(len(self.tst), 3) # The TST has 'abc', 'aqt', and '' now
        self.assertTrue(self.tst.search(''))
        self.assertTrue(self.tst.search('a'))
        self.assertTrue(self.tst.search('abc'))
        self.assertFalse(self.tst.search('', exact=True)) # Exact search for empty string should be False