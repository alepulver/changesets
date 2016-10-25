import sys
import patch_utils

def conflicts(patches):
    patches_files = map(lambda x : (x, patch_utils.modified_classes(x)), patches)
    modified_classes = {}
    for name, classes in patches_files:
        for c in classes:
            modified_classes[c] = modified_classes.get(c, [])
            modified_classes[c].append(name)

    conflict_classes = {clave: valor for clave, valor in modified_classes.items() if len(valor) > 1}
    return conflict_classes


def main(args):
    all_conflicts = conflicts(args)
    if len(all_conflicts) > 0:
        for conflict, patches in all_conflicts.items():
            print(conflict)
            for patch in patches:
                print("\t- " + patch)
    else:
        print("There are no conflicts between those patches")

if __name__ == "__main__":
    main(sys.argv[1:])
    