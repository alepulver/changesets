import sys
import os
import patch_utils
from subprocess import Popen, PIPE, call

UTILITY_PATH = "src/main/java/"
PREFIX_BRANCH = "refs/tags/mule-"

def filter_starting_with(l, start):
    return filter(lambda path: path.startswith(start), l)

def add_java(c):
    return c + ".java"

def git_diff_files(git_source, v_origin, v_destination):
    working_dir = os.getcwd()
    try:
        os.chdir(git_source)
        call(["git", "fetch", "--tags"])
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

def main(args):
    if len(args) < 4 or len(args) > 5:
        print_usage()
        sys.exit(1)

    if len(args) == 4:
        version = os.path.basename(args[0]).replace(".jar", "").split("-")[-1]
        args.append(version)

    patch_source, ce_path, ee_path, v_dest, v_org = args
    v_dest = PREFIX_BRANCH + v_dest
    v_org = PREFIX_BRANCH + v_org
    p = PatchDiffer(ce_path, ee_path)
    classes = patch_utils.modified_classes(patch_source)
    if p.is_applicable(classes, v_org, v_dest):
        print("The patch " + args[0] + " is applicable to the " + args[3] + " version")
    else:
        print("The patch " + args[0] + " has conflicts in files:")
        for file in p.get_conflicts():
            print("\t- " + file)


if __name__ == "__main__":
    main(sys.argv[1:])
