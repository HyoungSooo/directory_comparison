from unittest import TestCase
from search_folder import SearchFolder


class TestSearchFolder(TestCase):
    def test_check_function(self):
        SearchFolder.check('test\\test_folder', 'test\\real_folder')
        self.assertEqual(len(SearchFolder.diff['T']), 6)
        self.assertEqual(len(SearchFolder.diff['R']), 2)
        self.assertEqual(len(SearchFolder.diff['X']), 1)
