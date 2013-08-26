import collections
import os
import subprocess


from . import utils
from .files import File

__version__ = '0.0.0'


class Repository(object):

    repo_path = None

    def __init__(self, path):
        self.repo_path = path

    def clone_from(self, source_path):
        """ Clone the repository to the destination path """
        # Will raise an exception if unsuccessful
        utils.silence(
            subprocess.check_call,
            ('git', 'clone', source_path, self.repo_path)
        )
        return True

    def init(self):
        """ Creates a new git repository. """
        self._chdir()
        utils.silence(
            subprocess.call,
            ('git', 'init')
        )

    def _chdir(self):
        if not os.path.exists(self.repo_path):
            os.mkdir(self.repo_path)
        os.chdir(self.repo_path)

    # Manage pending commit
    #######################

    def add_file(self, file_path, commit_author, commit_message):
        """ Adds a new or changed file to the pending commit """
        self._stage_file(file_path)
        self.commit(
            author=commit_author,
            message=commit_message,
        )

    def delete_file(self, file_path, commit_author, commit_message):
        """ Deletes a file and marks it as deleted in the pending commit """
        self._rm_file(file_path)
        self.commit(
            author=commit_author,
            message=commit_message
        )

    def move_file(self, old_path, new_path, commit_author, commit_message):
        """ Moves a file and marks it as moved in the pending commit """
        self._mv_file(old_path, new_path)
        self.commit(
            author=commit_author,
            message=commit_message,
        )

    def _unstage_file(self, file_path):
        """ Removes a file from the pending commit """
        utils.silence(subprocess.call, ('git', 'rm', '--cached', file_path))

    def _stage_file(self, file_path):
        utils.silence(subprocess.call, ('git', 'add', file_path))

    def _rm_file(self, file_path):
        utils.silence(subprocess.call, ('git', 'rm', file_path))

    def _mv_file(self, old_path, new_path):
        subprocess.call(
            ('git', 'mv', os.path.abspath(old_path), os.path.abspath(new_path))
        )

    @property
    def staged_files(self):
        """ File staged in the pending commit"""
        return [x.path for x in self._parse_status() if x.index_state != '?']

    @property
    def unstaged_files(self):
        """ Files differing from the index, but not in the pending commit """
        return [x.path for x in self._parse_status() if x.index_state == '?']

    @property
    def untracked_files(self):
        """ Files not ignored or tracked in the index """
        return [x.path for x in self._parse_status() if x.working_state == '?']

    def _parse_status(self):
        FileStatus = collections.namedtuple(
            'FileStatus',
            ('path', 'index_state', 'working_state')
        )

        return tuple(
            FileStatus(x[3:],x[1], x[0])
            for x in subprocess.check_output(
                ('git', 'status', '--porcelain')
            ).strip().split('\n')
        )

    def commit(self, author, message):
        """ Perform the commit """
        # NOTE: user format: 'Lyndsy Simon <lyndsy@centerforopenscience.org'
        utils.silence(
            subprocess.call,
            (
                'git',
                'commit',
                '--author="{}"'.format(author),
                '-m "{}"'.format(message)
            ),
        )

    def _get_file_content(self, path, sha=None):
        # TODO: What happens if the file isn't present in HEAD?
        # g show HEAD~1:foo.txt
        return subprocess.check_output((
            'git',
            'show',
            '{ref}:{path}'.format(
                ref=sha or 'HEAD',
                path=path
            )
        ))

    def get_file(self, path):
        return File(self, path)







#
# my_repo = Repo('/path/to/repo')
# my_repo.add_file('/apath/to/file/')
# my_repo.commit()