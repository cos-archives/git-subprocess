import os
import subprocess
import unittest


from gitsubprocess import Repository
from gitsubprocess.exceptions import *


class GitTestCase(unittest.TestCase):
    #TODO: This should be dynamic.
    TESTING_ROOT = '../tmp'
    VALID_REPO = '%s/valid_repo' % TESTING_ROOT
    INVALID_REPO = '%s/invalid_repo' % TESTING_ROOT
    TEST_REPO = '%s/test_repo' % TESTING_ROOT

    def _execute(self, command, cwd=TESTING_ROOT):
        return subprocess.Popen(
            command,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False
        ).communicate()

    def _add_file(self, name, contents):
        with open('%s/%s' % (self.TEST_REPO, name), 'a+') as f:
            f.write(contents)
        return True

    def setUp(self):
        if os.path.exists(self.TESTING_ROOT):
            raise Exception('Testing root exists - %s must not exist.' % self.TESTING_ROOT)
        self._execute(['mkdir', self.TESTING_ROOT], cwd=os.getcwd())

        self._execute(['mkdir', 'invalid_repo'])
        self._execute(['mkdir', 'valid_repo'])
        self._execute(['git', 'init'], cwd='%s/valid_repo' % self.TESTING_ROOT)


    def tearDown(self):
        self._execute(['rm','-rf',self.TESTING_ROOT])

    def test_is_valid(self):
        repo = Repository(self.VALID_REPO)
        self.assertTrue(repo.is_git_repo())

        repo = Repository(self.INVALID_REPO)
        self.assertFalse(repo.is_git_repo())

    def test_create(self):
        repo = Repository(self.TEST_REPO)
        self.assertTrue(repo.create())
        self.assertTrue(repo.is_git_repo())

    def test_create_existing_repo(self):
        repo = Repository(self.VALID_REPO)
        self.assertRaises(GitInitException, repo.create)

    def test_create_existing_directory(self):
        repo = Repository(self.INVALID_REPO)
        self.assertRaises(GitInitException, repo.create)

    def test_add_file(self):
        repo = Repository(self.TEST_REPO)
        repo.create()
        self._add_file('foo.txt','test string')
        self.assertTrue(repo.add('foo.txt'))

    def test_add_file_does_not_exist(self):
        repo = Repository(self.TEST_REPO)
        repo.create()
        with self.assertRaises(FileNotFound):
            repo.add('notarealfile.txt')

    def test_commit(self):
        repo = Repository(self.TEST_REPO)
        repo.create()
        self._add_file('foo.txt','test string')
        repo.add('foo.txt')
        self.assertTrue(repo.commit('Test commit'))

    def test_commit_no_changes(self):
        repo = Repository(self.TEST_REPO)
        repo.create()
        with self.assertRaises(NothingToCommit):
            repo.commit('test commit')


if __name__ == '__main__':
    unittest.main()
