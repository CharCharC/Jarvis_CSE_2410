import unittest
from T_wotd import *


class test_wotd(unittest.TestCase):
    
   def test_scraping(self):
      result = wotd(1, "y")
      self.assertTrue(result)

   def test_prompt_yes(self):
      result = wotd(0, "y")
      self.assertTrue(result)

   def test_prompt_no(self):
      result = wotd(2, "n")
      self.assertFalse(result)

if __name__ == '__main__':
   unittest.main()