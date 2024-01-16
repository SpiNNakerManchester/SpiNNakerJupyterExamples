# Copyright (c) 2024 The University of Manchester
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import platform
from shutil import copyfile
import sys


class BashBuilder(object):
    """
    This class will recreate the pylint.bash file
    """

    def add_scripts(self, a_dir, prefix_len, test_file, exceptions):
        """
        :param str a_dir:
        :param int prefix_len:
        :param io.TextIOBase test_file:
        :param dict(str,str) exceptions:
        """
        for a_script in os.listdir(a_dir):
            script_path = os.path.join(a_dir, a_script)
            if os.path.isdir(script_path) and not a_script.startswith("."):
                self.add_scripts(
                    script_path, prefix_len, test_file, exceptions)
            elif a_script.endswith(".ipynb") and a_script != "__init__.py":
                local_path = script_path[prefix_len:]
                # As the paths are written to strings in files
                # Windows needs help!
                if platform.system() == "Windows":
                    local_path = local_path.replace("\\", "/")
                if a_script not in exceptions:
                    test_file.write(local_path)
                    test_file.write(" ")

    def build_bash(self, exceptions):
        class_file = sys.modules[self.__module__].__file__
        integration_dir = os.path.dirname(class_file)
        repository_dir = os.path.dirname(integration_dir)

        test_script = os.path.join(integration_dir, "pytest.bash")
        header = os.path.join(integration_dir, "header.bash")
        copyfile(header, test_script)

        with open(test_script, "a", encoding="utf-8") as test_file:
            test_file.write("pytest --nbmake ")
            self.add_scripts(repository_dir, len(repository_dir) + 1,
                             test_file, exceptions)


if __name__ == '__main__':
    builder = BashBuilder()
    builder.build_bash(["task5-solutions.ipynb", "LiveInputAndOutput.ipynb"])
