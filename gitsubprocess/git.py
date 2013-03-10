__author__ = 'samportnow'

import os
import subprocess

from gitsubprocess.exceptions import (
    FileNotFound, GitInitException,
    InvalidRepository, NothingToCommit)

# rather than make dir, we want to test if the path is a git repo
# add and commit function


class Repository(object):
    '''Represents a git repository.'''

    def __init__(self, path):
        self.path = path

    def _execute(self, *args):
        response = subprocess.Popen(
            ["git", ] + list(args),
            cwd=self.path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False
        ).communicate()
        return { 'output': response[0], 'error': response[1] }

    def is_git_repo(self):
        if self._execute('status')['error'].startswith('fatal'):
            return False
        else:
            return True

    def create(self):
        if os.path.exists(self.path):
            raise GitInitException('The path exists: %s' % self.path)
        else:
            os.mkdir(self.path)
            self.init()
            return True

    def init(self):
        self._execute('init')
        return True

    def add(self, filename):
        if not self.is_git_repo():
            raise InvalidRepository
        response = self._execute('add', filename)
        # TODO: I don't like this method of testing if it failed; it relies on
        # the output of git remaining constant, and the output being in English
        if 'did not match' in response['error']:
            raise FileNotFound
        return True

    def commit(self, message):
        response = self._execute('commit', '-m', message)
        if 'nothing to commit' in response['output']:
            raise NothingToCommit
        return True

    # Refactored above this line - LyndsySimon, 2013-03-08


    def add_and_commit(self, path, file, fullname, email, message):
        if self.is_git_repo(path):
            add = subprocess.Popen(
                ["git", "add", file],
                cwd=path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=False
            ).communicate()
            if add:
                subprocess.Popen(
                    ["git", "commit", "-m", message],
                    cwd=path,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    shell=False
                ).communicate()
                return True

    def get_head_hash(self, path):
        try:
            os.mkdir(path)
        except:
            pass

        return subprocess.Popen(
            ["git", "rev-parse", "HEAD"],
            cwd=path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False
        ).communicate()

    def get_file_recent_hash(self, path, filename):
        try:
            os.mkdir(path)
        except:
            pass
        file_and_hash = {}
        file = subprocess.Popen(
            ["git", "ls-files", "-s", filename],
            cwd=path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False
        ).communicate()
        position = file[0].find(filename)
        hash = file[0][:position].strip()
        file = file[0][position:].strip()
        file_and_hash[file] = hash
        return file_and_hash

    def clone(self, path, url, wd=""):
        subprocess.Popen(
            ["git", "clone", url, wd],
            cwd=path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False
        ).communicate()

    def get_status(self, path):
        try:
            os.mkdir(path)
        except:
            pass
        subprocess.Popen(
            ["git", "status"],
            cwd=path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False
        ).communicate()

    def get_history(self, path, filename):
        try:
            os.mkdir(path)
        except:
            pass
        Git_Commit_Fields = [
            'Commit Hash',
            'Tree Hash',
            'Parent hashes',
            'Author name',
            'Author email',
            'Author date',
            'Author date, relative',
            'Committer name',
            'Commited Email',
            'Commiter date',
            'Commiter date relative',
            'Subject'
        ]
        Git_Log_Format = [
            '%H', '%T', '%P', '%an', '%ae', '%ad',
            '%ar', '%cn', '%ce', '%cd', '%cr', '%s']

        Git_Log_Format = '%x1f'.join(Git_Log_Format) + '%x1e'

        p = subprocess.Popen(
            ['git', 'log', '--format="%s"' % Git_Log_Format, '--',  filename],
            cwd=path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False,
        )
        (log, _) = p.communicate()

        log = log.strip('\n\x1e').split("\x1e")
        log = [row.strip().split("\x1f") for row in log]
        log = [dict(zip(Git_Commit_Fields, row)) for row in log if row]
        return log

    def get_diff(self, path, hash, filename):
        try:
            os.mkdir(path)
        except:
            pass
        return subprocess.Popen(
            ["git", "diff", hash, '--', filename],
            cwd=path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False
        ).communicate()

    def reset(self, path, hash, filename):
        try:
            os.mkdir(path)
        except:
            pass
        subprocess.Popen(
            ["git", "reset", hash, '--', filename],
            cwd=path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False
        ).communicate()

    def get_and_copy(self, path, filename, new_path):
        if self.is_git_repo(path):
            moved = subprocess.Popen(
                ["git", "mv", filename, new_path],
                cwd=path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=False
            ).communicate()
            if moved[1].startswith('fatal:'):
                raise Exception('Must be a git repo')

    def get_file_version(self, repo_path, hash, filename, new_path=None):
        if self.is_git_repo(repo_path):
            if new_path:
                with open(new_path, 'w') as f:
                    p = subprocess.Popen(
                        ["git", "show", hash + ':' + filename],
                        cwd=repo_path,
                        stdout=f,
                        stderr=subprocess.PIPE,
                        shell=False
                    ).communicate()
                    if p[1].startswith('fatal'):
                        return False
                    #TODO don't write a new file if it's false
                return True
            else:
                p = subprocess.Popen(
                    ["git", "show", hash + ':' + filename],
                    cwd=repo_path,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    shell=False
                ).communicate()
                return p[0]




#get file version, pass a path, a hash, and a filename, and a new path to copy the file

#https://help.github.com/articles/remove-sensitive-data

#init("/Users/samportnow/Documents/Git")
#add("/Users/samportnow/Documents/Git",".")
#commit("/Users/samportnow/Documents/Git", "Sam Portnow", "samson91787@gmail.com", "Made some changes")
#print get_hash_commit("/Users/samportnow/Documents/Git")
#print get_status("/Users/samportnow/Documents/Git")
#print get_history("/Users/samportnow/Documents/Git/", "test_git.py")

# def commit
# def init
# def add

# def get_file ... this will be a special function
# def file_delete ... this will be a special function
#def file_versions
#print add_and_commit('/Users/samportnow/Documents/Git','.','Sam Portnow', 'samson91787@gmail.com','adding files')
#print get_and_copy('/Users/samportnow/Documents/Git','jefftest.txt','/Users/samportnow/Documents/Git/')
#print get_file_version('/Users/samportnow/Documents/Git/gitsubprocess','9e6fa9292737b804fa4bdaa2065cb6279a3e52d0','jefftest.txt')
