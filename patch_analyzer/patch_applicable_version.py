import sys
import os
import patch_utils
from subprocess import Popen, PIPE

UTILITY_PATH = "src/main/java/"

def filter_starting_with(l, start):
    return filter(lambda path: path.startswith(start), l)

def add_java(c):
    return c + ".java"

def git_diff_files(git_source, v_origin, v_destination):
    working_dir = os.getcwd()
    try:
        os.chdir(git_source)
        p = Popen(["git", "diff", "--name-only", v_origin + ".." + v_destination], stdout=PIPE)
        output, _ = p.communicate()
        files = [file.decode() for file in output.split(b"\n")]
        return set(map(lambda file: file.split(UTILITY_PATH)[-1], filter(lambda file: UTILITY_PATH in file, files)))
    finally:
        os.chdir(working_dir)

class PatchDiffer:
    def __init__(self, mule_ce_path, mule_ee_path):
        self.ce = mule_ce_path
        self.ee = mule_ee_path


    @staticmethod
    def conflicts(files, diff_files):
        return list(set(files) & diff_files)

    def is_applicable(self, changed_classes, origin_version, destination_version):
        ce_files = map(add_java, filter_starting_with(changed_classes, "org"))
        ee_files = map(add_java, filter_starting_with(changed_classes, "com"))
        ce_diff = git_diff_files(self.ce, origin_version, destination_version)
        ee_diff = git_diff_files(self.ee, origin_version, destination_version)

        total_conflicts = self.conflicts(ce_files, ce_diff) + self.conflicts(ee_files, ee_diff)

        self.last_conflicts = total_conflicts
        return len(self.last_conflicts) == 0

    def get_conflicts(self):
        assert hasattr(self, "last_conflicts")
        return self.last_conflicts

def print_usage():
    print("Usage: ")
    print("python " + sys.argv[0] + " <patch-file> <ce-git-folder> <ee-git-folder> <destination-version> (<origin-version>)")
    print("If the origin version is not specified, it will be inferred from the Patch filename. Example:")
    print("\tpython " + sys.argv[0] + " SE-2618-3.7.3.jar ../Git/mule-ce ../Git/mule-ee 3.7.4")

if __name__ == "__main__":
    parameters = sys.argv[1:]
    if len(parameters) < 4 or len(parameters) > 5:
        print_usage()
        sys.exit(1)

    if len(parameters) == 4:
        version = os.path.basename(parameters[0]).replace(".jar", "").split("-")[-1]
        parameters.append(version)

    patch_source, ce_path, ee_path, v_dest, v_org = parameters
    v_dest = "mule-" + v_dest
    v_org = "mule-" + v_org
    p = PatchDiffer(ce_path, ee_path)
    classes = patch_utils.modified_classes(patch_source)
    if p.is_applicable(classes, v_org, v_dest):
        print("The patch is applicable to the " + parameters[3] + " version")
    else:
        print("There are conflicts in files:")
        for file in p.get_conflicts():
            print("\t- " + file)

