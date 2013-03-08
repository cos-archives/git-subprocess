__author__ = 'samportnow'

import os
import subprocess

# rather than make dir, we want to test if the path is a git repo
# add and commit function


def is_git_repo(path):
    if subprocess.Popen(
        ["git", "status"],
        cwd=path,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=False
    ).communicate()[1].startswith('fatal'):
        return False
    else:
        return True


def add_and_commit(path, file, fullname, email, message):
    if is_git_repo(path):
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


def init(path):
    try:
        os.mkdir(path)
    except:
        return 'Something wrong with the path'

    subprocess.Popen(
        ["git", "init"],
        cwd=path,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=False
    ).communicate()


def commit(path, fullname, email, message):
    try:
        os.mkdir(path)
    except:
        pass

    subprocess.Popen(
        ["git", "commit", "-m", message],
        cwd=path,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=False
    ).communicate()


def add(path, file):
    try:
        os.mkdir(path)
    except:
        pass

    subprocess.Popen(
        ["git", "add", file],
        cwd=path,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=False
    ).communicate()


def get_head_hash(path):
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


def get_file_recent_hash(path, filename):
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


def clone(path, url, wd=""):
    subprocess.Popen(
        ["git", "clone", url, wd],
        cwd=path,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=False
    ).communicate()


def get_status(path):
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


def get_history(path, filename):
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


def get_diff(path, hash, filename):
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


def reset(path, hash, filename):
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


def get_and_copy(path, filename, new_path):
    if is_git_repo(path):
        moved = subprocess.Popen(
            ["git", "mv", filename, new_path],
            cwd=path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False
        ).communicate()
        if moved[1].startswith('fatal:'):
            raise Exception('Must be a git repo')


def get_file_version(repo_path, hash, filename, new_path=None):
    if is_git_repo(repo_path):
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
