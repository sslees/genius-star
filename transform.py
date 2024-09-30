from triangle import *


class Transform:
    def __init__(self, da, db, dc, dr, flip):
        assert valid(da, db, dc)
        assert dr % 120 == 0
        self.da = da
        self.db = db
        self.dc = dc
        self.dr = (dr % 360 + 360) % 360
        self.flip = flip
        self.conflicts = 0

    def __hash__(self):
        return hash((self.da, self.db, self.dc, self.dr, self.flip))

    def __eq__(self, value):
        return (
            self.da == value.da
            and self.db == value.db
            and self.dc == value.dc
            and self.dr == value.dr
            and self.flip == value.flip
        )
