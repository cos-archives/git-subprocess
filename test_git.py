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
    ["git", "commit", fullname, email, "-m", message],
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

init("/Users/samportnow/Documents/Git")
add("/Users/samportnow/Documents/Git",".")
commit("/Users/samportnow/Documents/Git", "Sam Portnow", "samson91787@gmail.com", "Made some changes")
# def commit
# def init
# def add

# def get_file ... this will be a special function
# def file_delete ... this will be a special function

#def file_versions
