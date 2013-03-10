import benchmark
import gitsubprocess
import pygit2
import tempfile
import os

class Benchmark_Git(benchmark.Benchmark):

    each = 100 # allows for differing number of runs

    def setUp(self):
        self.git_sub_path = tempfile.mkdtemp()

        repository = gitsubprocess.GitRepo(self.git_sub_path)
        self.git_lib_path = tempfile.mkdtemp()
        pygit2.init_repository(self.git_lib_path, False)
        self.git_sub_counter = 1
        self.get_lib_counter = 1

    def test_git_sub(self):
        path = self.git_sub_path
        repository = gitsubprocess.GitRepo(self.git_sub_path)
        with open(os.path.join(path, 'test.txt'), 'w') as f:
            f.write('Hello, world')
        repository.add('./test.txt')
        repository.commit("Sam Portnow", "sam@gmail.com", "First commit")


    def test_py_git_2(self):
        path = self.git_lib_path
        repo = pygit2.Repository(path)
        with open(os.path.join(path, 'test.txt'), 'w') as f:
            f.write('Hello, world')


        author = pygit2.Signature("Sam Portnow", "samson91787@gmail.com" )
        committer = pygit2.Signature("Sam Portnow", "samson91787@gmail.com")
        tree = repo.TreeBuilder().write()
#        import pdb; pdb.set_trace()
        repo.create_commit('refs/heads/master', author, committer, 'this is the message', tree, [])



if __name__ == '__main__':
    benchmark.main(format="markdown", numberFormat="%.4g")
    # could have written benchmark.main(each=50) if the
    # first class shouldn't have been run 100 times.