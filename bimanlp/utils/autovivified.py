# From http://stackoverflow.com/questions/635483/what-is-the-best-way-to-implement-nested-dictionaries-in-python
class AutoVivification(dict):
    """Implementation of perl's autovivification feature."""
    ## a[1][2][3] = 4
    ## a[1][3][3] = 5
    ## a[1][2]['test'] = 6
    ## Output:
    ## {1: {2: {'test': 6, 3: 4}, 3: {3: 5}}}
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value
