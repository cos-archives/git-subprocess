__author__ = 'samportnow'

import subprocess, os




def init(path):
    try:
        os.mkdir(path)
    except:
        pass

    subprocess.Popen(
        ["git", "init"],
        cwd = path,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
        shell = False
        ).communicate()

def commit(path, fullname, email, message):
    try:
        os.mkdir(path)
    except:
        pass

    subprocess.Popen(
    ["git", "commit", "-m", message],
    cwd = path,
    stdout = subprocess.PIPE,
    stderr = subprocess.PIPE,
    shell = False
    ).communicate()


def add(path, file):
    try:
        os.mkdir(path)
    except:
        pass

    subprocess.Popen(
    ["git", "add", file],
    cwd = path,
    stdout = subprocess.PIPE,
    stderr = subprocess.PIPE,
    shell = False
    ).communicate()

def get_hash_commit(path):
    try:
        os.mkdir(path)
    except:
        pass

    return subprocess.Popen(
        ["git", "rev-parse", "HEAD"],
        cwd = path,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
        shell = False
    ).communicate()

def get_hash_file(path, filename):
    try:
        os.mkdir(path)
    except:
        pass
    file_and_hash = {}
    file = subprocess.Popen(
    ["git", "ls-files", "-s", filename],
    cwd = path,
    stdout = subprocess.PIPE,
    stderr = subprocess.PIPE,
    shell = False
    ).communicate()
    position = file[0].find(filename)
    hash = file[0][:position].strip()
    file = file[0][position:].strip()
    file_and_hash[file] = hash
    return file_and_hash

#https://help.github.com/articles/remove-sensitive-data

#init("/Users/samportnow/Documents/Git")
#add("/Users/samportnow/Documents/Git",".")
#commit("/Users/samportnow/Documents/Git", "Sam Portnow", "samson91787@gmail.com", "Made some changes")
print get_hash_commit("/Users/samportnow/Documents/Git")
print get_hash_file("/Users/samportnow/Documents/Git","test_git.py")
# def commit
# def init
# def add

# def get_file ... this will be a special function
# def file_delete ... this will be a special function
#def file_versions
