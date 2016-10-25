import jira_version
import patch_applicable_version
import patch_conflicts
import argparse
import sys
import re


def parse_arguments():
    parser = argparse.ArgumentParser(description="Checks if there are conflicts between patches, " + 
        "if a patch is needed in a newer version, and if a patch is directly applicable in a newer version")
    parser.add_argument("--current_version", "-c", dest="current_version", help="Current installed version", required=True)
    parser.add_argument("--new_version", "-n", dest="new_version", help="Newer version you wish to migrate to", required=True)
    parser.add_argument("--repo_ce", "--ce", dest="repo_ce", help="Absolute or relative path to the CE Git Local Repository", required=True)
    parser.add_argument("--repo_ee", "--ee", dest="repo_ee", help="Absolute or relative path to the EE it Local Repository", required=True)
    parser.add_argument("SEs", metavar="SEs", help="List of all Patch SEs. Example: patches/SE-1234-3.7.1.jar patches/SE-4321-3.7.1.jar", nargs="+")

    args = parser.parse_args(sys.argv[1:])
    return args.current_version, args.new_version, args.repo_ce, args.repo_ee, args.SEs



def do_validations(cver, nver, repo_ce, repo_ee, ses):
    print("Checking wether the patch have conflicts with eachother")
    patch_conflicts.main(ses)
    print("\n")

    print("Checking if the patches are applicable to the new version")
    for se in ses:
        patch_applicable_version.main([se, repo_ce, repo_ee, nver, cver])
    print("\n")

    print("Checking which patches are not necessary any more in the newer version")
    jira_version.main([nver] + [re.search("SE-\d+", se).group(0) for se in ses])


if __name__ == "__main__":
    cver, nver, repo_ce, repo_ee, ses = parse_arguments()
    do_validations(cver, nver, repo_ce, repo_ee, ses)
    