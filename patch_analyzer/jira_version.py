import sys
from jira import JIRA
import re

#FILL WITH USERNAME AND PASSWORD IN THAT FILE
with open("credentials.txt") as f:
    USERNAME, PASSWORD = [l.strip() for l in f.readlines()[0:2]]

def fix_versions(issue):
    jira = JIRA("https://www.mulesoft.org/jira", basic_auth=(USERNAME, PASSWORD))
    issue = jira.issue(issue, fields="fixVersions")
    return [re.search("\d+\.\d+\.\d", version.name).group(0) for version in issue.fields.fixVersions]


class MuleVersion:
    def __init__(self, version_str):
        self.version, self.mayor, self.minor = version_str.split(".")

    def __le__(self, other):
        if self.version != other.version: return False
        if self.mayor != other.mayor: return False
        return self.minor <= other.minor

    def __str__(self):
        return self.version + "." + self.mayor + "." + self.minor


def is_already_fixed(issue, new_version):
    fixed_versions = map(MuleVersion, fix_versions(issue))
    for fv in fixed_versions:
        if fv <= new_version:
            return True
    return False

def print_usage():
    print("python " + sys.argv[0] + " <new version> [List of SEs]. Example:")
    print("\tpython " + sys.argv[0] +  " 3.7.5 SE-2618 SE-1234")

def main(args):
    try:    
        version = MuleVersion(args[0])
    except ValueError:
        print("Invalid version: " + args[0] + ". Version should have the format: X.Y.Z")
        print_usage()
        sys.exit(2)

    unfixed = [issue for issue in args[1:] if not is_already_fixed(issue, version)]
    fixed = [issue for issue in args[1:] if is_already_fixed(issue, version)]

    if len(unfixed) > 0:
        print("The following issues are already solved in the " + str(version) + " release")
        for issue in fixed:
            print("\t- " + issue)
            
        print("The following issues are not solved in the " + str(version) + " release")
        for issue in unfixed:
            print("\t- " + issue)
    else:
        print("All the issues have been solved in the target version")

if __name__ == "__main__":
    if len(sys.argv) < 3: 
        print_usage()
        sys.exit(1)

    main(sys.argv[1:])



