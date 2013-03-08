import unittest
from gitsubprocess import Repository


class GitTestCase(unittest.TestCase):
    #TODO: This should be dynamic.
    VALID_REPO = 'C:/tmp/valid_repo'
    INVALID_REPO = 'C:/tmp/invalid_repo'

    def test_is_valid(self):
        repo = Repository(self.VALID_REPO)
        self.assertTrue(repo.is_git_repo())

        repo = Repository(self.INVALID_REPO)
        self.assertFalse(repo.is_git_repo())


if __name__ == '__main__':
    unittest.main()
