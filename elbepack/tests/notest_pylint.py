# ELBE - Debian Based Embedded Rootfilesystem Builder
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2020 Linutronix GmbH

import os

from elbepack.commands.test import ElbeTestCase, ElbeTestException, system
from elbepack.directories import elbe_dir, elbe_exe, pack_dir
from elbepack.shellhelper import system_out


class TestPylint(ElbeTestCase):
    global elbe_dir

    elbe_dir = os.path.join(os.path.dirname(__file__), '../..')

    pylint_opts = ['--reports=n',
                   '--score=n',
                   f"--rcfile={os.path.join(elbe_dir, '.pylintrc')}",
                   '--disable=W0511,R0801']

    failure_set = {os.path.join(pack_dir, path)
                   for path
                   in [
                       'daemons/soap/esoap.py',

                       # FIXME: This one is an actual bug to be fixed
                       # 274:30: W0631: Using possibly undefined loop variable
                       # 'entry' (undefined-loop-variable)
                       # 276:26: W0631: Using possibly undefined loop variable
                       # 'entry' (undefined-loop-variable)
                       'hdimg.py',

                       'initvmaction.py',
                       'log.py',
                       'pbuilderaction.py',
                       'repomanager.py',
                       'rfs.py',
                       'rpcaptcache.py',
                   ]}

    @staticmethod
    def params():
        files = system_out(f"find {pack_dir} -iname '*.py'").splitlines()
        files.append(elbe_exe)
        return files

    def test_lint(self):

        try:
            system(f"pylint {' '.join(self.pylint_opts)} {self.param}")
        except ElbeTestException as e:
            if self.param in TestPylint.failure_set:
                self.stdout = e.out
                self.skipTest(
                    f'Pylint test for {self.param} is expected to fail')
            else:
                raise
        else:
            if self.param in TestPylint.failure_set:
                raise Exception(f'Pylint test for {self.param} is expected to fail, but did not !')
