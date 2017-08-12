import LayoutBox as lb
import matplotlib
matplotlib.use('QT5Agg')
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec



def plot_children(ax, box, level=0):
    '''
    Simple plotting to show where boxes are
    '''
    import matplotlib.patches as patches
    colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]
    print("Level:", level)
    for child in box.children:
        rect = child.get_rect()
        print(child)
        ax.add_patch(
            patches.Rectangle(
                (child.left.value(), child.bottom.value()),   # (x,y)
                child.width.value(),          # width
                child.height.value(),          # height
                fc = 'none',
                ec = colors[level]
            )
        )
        if level%2 == 0:
            ax.text(child.left.value(), child.bottom.value(), child.name,
                   size=12-level, color=colors[level])
        else:
            ax.text(child.right.value(), child.top.value(), child.name,
                    ha='right', va='top', size=12-level, color=colors[level])

        plot_children(ax, child, level=level+1)

#### Main routine
fig0, axs = plt.subplots(2, 6)
try:
    axs = axs.flatten()
except:
    axs = np.array([axs])
axx = fig0.add_axes([0,0,1,1])
axx.set_zorder(-1000)
pcm = axs[0].pcolormesh(np.random.rand(32,32))
# place the colorbar.  This will change size, but a good approx size is useful
for ax in axs.flatten():
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('AX')
# now lets do layout
figlb = lb.LayoutBox(parent=None, name='figlb')
figlb.set_geometry(0.,0.,1.,1.)

# make a container for the full gridspec.   In this case it has the
# same size as the figure, but you can imagine cases where the parent
# is another layoutbox, and it has a smaller size
#
# We need this container so that all the axes inside the gridspec can
# be shrunk to make room for the colorbar.
gslb = lb.LayoutBox(parent=figlb, name='gslb')
# simplify this a level
#gslb = figlb
# works.  So issue is with gslb being child of figlb...

sss = []
sslbs = []
axlbs = []
axspinelbs = []
for n,ax in enumerate(axs):
    print(n)
    sss += [ax.get_subplotspec().get_topmost_subplotspec()]
    print(sss[-1])
    # this is the container for the axis and anything attached to it
    sslbs += [gslb.layout_from_subplotspec(sss[-1], name='sslb%d'%n)]
    # this is th contaier for the axis itself
    axlbs += [lb.LayoutBox(parent=sslbs[-1], name='axlb%d'%n)]
    # this is the location needed for the spine.
    axspinelbs += [lb.LayoutBox(parent=axlbs[-1], name='axspinelb%d'%n)]



# now place the axes splines:

# place axis spines lbs inside their layout boxes
for ax, axspinelb in zip(axs, axspinelbs):
    pos = ax.get_position()
    fig = ax.get_figure()
    renderer = fig.canvas.get_renderer()
    invTransFig = fig.transFigure.inverted().transform_bbox
    bbox = invTransFig(ax.get_tightbbox(renderer=renderer))
    leftpad = 0.0; rightpad=0.00; bottompad=0.00; toppad=0.00
    axspinelb.set_left_margin_min(-bbox.x0+pos.x0+leftpad)
    axspinelb.set_right_margin_min(bbox.x1-pos.x1+rightpad)
    axspinelb.set_bottom_margin_min(-bbox.y0+pos.y0+bottompad)
    axspinelb.set_top_margin_min(bbox.y1-pos.y1+toppad)

#lb.match_margins(axspinelbs)

figlb.update_variables()
plot_children(axx, figlb)

for ax, axspinelb in zip(axs, axspinelbs):
    ax.set_position(axspinelb.get_rect())
