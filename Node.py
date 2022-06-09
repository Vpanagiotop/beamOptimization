class Node:
    def __init__(
        self, tag,
        x:int, y:int,
        xFixed:bool = False,
        yFixed:bool = False,
        thetaFixed:bool = False,
        Px: int = 0, Py: int = 0
    ):
        self.tag = tag
        self.x = x
        self.y = y
        self.xFixed = xFixed
        self.yFixed = yFixed
        self.thetaFixed = thetaFixed
        self.Px = Px
        self.Py = Py
        self.elements = []