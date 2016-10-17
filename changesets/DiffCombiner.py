from changesets.ChangeSet import ChangeSet


class DiffCombiner:
    def combine(self, changesets):
        all_files = set()
        for change_set in changesets:
            for file in change_set.files:
                if file not in all_files:
                    all_files.add(file)
                else:
                    raise RuntimeError("duplicated entry")

        return ChangeSet("all", list(all_files))
