from subprocess import Popen, PIPE

def is_class(file):
    return file.endswith(".class") and not file.startswith("META-INF")

def modified_paths(patch):
    p = Popen(["jar", "-tf", patch], stdout=PIPE)
    output, _ = p.communicate()
    return filter(is_class, [file.decode() for file in output.split(b"\n")])


def path_to_class(path):
    if "$" in path:
        return path.split("$")[0]
    else:
        return path.replace(".class", "")

def modified_classes(patch):
    classes = map(path_to_class, modified_paths(patch))
    return list(set(classes))