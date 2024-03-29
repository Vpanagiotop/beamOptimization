import numpy as np
import matplotlib.pyplot as plt
from Generator import Generator
from designModel import designModel
from sizeOptimization import sizeOptimization
from Plotter import plotNodes, plotElement
from optimalityCriteria import optimalityCriteria
model = Generator(length=12, height=3, rmin = 3, mesh={'x':1, 'y':1}, pen=3)
volfrac = 0.5
for node in model.node:
    if node.x == model.length and node.y == 0:
        node.xFixed = True
        node.yFixed = True
        node.thetaFixed = True
    elif node.x == 0 and node.y == 0:
        node.xFixed = True
        node.yFixed = True
        node.thetaFixed = True
    if node.y == 0:
        node.Py = -100
model.format()
plotELe = []
fig1, ax1 = plt.subplots()
for node in model.node:
    ax1.scatter(node.x, node.y, color='black', s=10)
for element in model.element:
    plotELe.append( ax1.plot([element.startNode.x, element.endNode.x], [element.startNode.y, element.endNode.y], 'black'))
ax1.axis('equal')
g = 0
x=volfrac * np.ones(len(model.element),dtype=float)
xOld=x.copy()
xPhys=x.copy()
loop = 0
change = 1
while change>0.01 and loop<20:
    loop=loop+1
    model.modify(xPhys)
    u = model.solveFE()
    ce = np.array([])
    for ele in model.element:
        ce = np.append(ce, (np.dot(u[ele.dof].reshape(1,6), ele.nominalStiffness) * u[ele.dof].reshape(1,6)).sum())
    obj=((model.Amin + xPhys**model.pen * (model.Amax - model.Amin)) * ce).sum()
    dc = (-model.pen * xPhys**(model.pen-1)*(model.Amax-model.Amin))*ce
    dc[:] = np.asarray((x*dc)[np.newaxis].T)[:,0] / np.maximum(0.001,x)
    xOld[:] = x.copy()
    (x[:],g) = optimalityCriteria(x, dc, g)
    xPhys = x
    change = np.linalg.norm(x.reshape(len(x),1) - xOld.reshape(len(x),1),np.inf)
    for i in range(len(plotELe)):
        plotELe[i][0].set_linewidth(xPhys[i] * model.element[i].A * 5)
    fig1.canvas.draw()
    fig1.canvas.flush_events()
    plt.draw()
    plt.pause(0.001)
    # Write iteration history to screen (req. Python 2.6 or newer)
    print("it.: {0} , obj.: {1:.3f} Vol.: {2:.3f}, ch.: {3:.3f}".format(\
                loop,obj,(g+volfrac*len(x))/(len(x)),change))
model.xPhys = xPhys