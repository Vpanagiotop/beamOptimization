import numpy as np
class Element:
    def __init__(self, tag, E, A, startNode, endNode):
        self.tag = tag
        self.startNode = startNode
        self.endNode = endNode
        self.E = E
        self.A = A
        self.nodeTag = [startNode.tag, endNode.tag]
        self.dof = np.array([startNode.dof, endNode.dof]).reshape(1,6)[0]
        self.length, self.cos, self.sin = getElementInfo(startNode, endNode)
        self.nominalStiffness = getNominalStiffness(self.length, self.cos, self.sin, E, A)
        self.stiffness = self.nominalStiffness.copy()

def getElementInfo(startNode, endNode):
    length = np.sqrt((startNode.x - endNode.x)**2 + (startNode.y - endNode.y)**2)
    Lx = endNode.x - startNode.x
    Ly = endNode.y - startNode.y
    cos = Lx/length
    sin = Ly/length
    return length, cos, sin

def getNominalStiffness(length, c, s, E, A):
    # A = A * 1.e-2
    I = A**2/4 / np.pi
    # I = A**2 / 12
    L = length
    E = 200000
    KN = np.array([
        [E*A/L, 0, 0],
        [0, 4*E*I/L, 2*E*I/L],
        [0, 2*E*I/L, 4*E*I/L,],
    ])
    be = np.array([
        [-c, -s/L, -s/L],
        [-s, c/L,  c/L ],
        [0.,  1.,   0. ],
        [c,  s/L,  s/L ],
        [s, -c/L, -c/L ],
        [0,  0.,  1.]
    ])
    return np.matmul(np.matmul(be, KN), be.T)