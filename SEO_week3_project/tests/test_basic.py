import unittest, sys, os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
sys.path.append('../SEO_week3_project') # imports python file from parent directory
from main import app #imports flask app object

class BasicTests(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        self.app = app.test_client()

    ###############
    #### tests ####
    ###############

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_new_page(self):
        response = self.app.get('/new', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_add_page(self):
        response = self.app.get('/add', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    

if __name__ == "__main__":
    unittest.main()