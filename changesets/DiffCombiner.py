from changesets.ChangeSet import ChangeSet


class DiffCombiner:
    def combine(self, changesets, path):
        all_files = set()
        all_changes = []
        for change_set in changesets:
            for change in change_set.changes:
                file = change.path
                if file not in all_files:
                    all_files.add(file)
                    all_changes.append(change)
                else:
                    raise RuntimeError("duplicated entry")

        return ChangeSet(path, all_changes)
