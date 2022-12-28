
# This file contains the functions available in the Library.
# Part of this code was taken and modified from 
#   - https://qiskit.org/documentation/_modules/qiskit/visualization/state_visualization.html#plot_state_qsphere
#   - https://qiskit.org/documentation/_modules/qiskit/visualization/state_visualization.html#n_choose_k
#   - https://qiskit.org/documentation/_modules/qiskit/visualization/state_visualization.html#bit_string_index
#   - https://qiskit.org/documentation/_modules/qiskit/visualization/state_visualization.html#lex_index
#   - https://qiskit.org/documentation/_modules/qiskit/visualization/state_visualization.html#phase_to_rgb
# This code is part of Qiskit.
#
# (C) Copyright IBM 2017, 2018, 2021.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

# Import necessary libraries

from qiskit.visualization.matplotlib import HAS_MATPLOTLIB
from qiskit.quantum_info import Statevector
from qiskit.visualization import VisualizationError
import os


from functools import reduce
import colorsys
from qiskit.quantum_info.states import DensityMatrix
import numpy as np
from scipy import linalg


import cv2
from math import floor

################### This section corresponds to code taken from qiskit.visualizations.state_visualization. ###################

if HAS_MATPLOTLIB:
    from matplotlib import get_backend
    from matplotlib import pyplot as plt
    from matplotlib.patches import FancyArrowPatch
    import matplotlib.gridspec as gridspec
    from mpl_toolkits.mplot3d import proj3d
if HAS_MATPLOTLIB:
    class Arrow3D(FancyArrowPatch):
        """Standard 3D arrow."""

        def __init__(self, xs, ys, zs, *args, **kwargs):
            """Create arrow."""
            FancyArrowPatch.__init__(self, (0, 0), (0, 0), *args, **kwargs)
            self._verts3d = xs, ys, zs

        def draw(self, renderer):
            """Draw the arrow."""
            xs3d, ys3d, zs3d = self._verts3d
            xs, ys, _ = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
            self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
            FancyArrowPatch.draw(self, renderer)

def n_choose_k(n, k):
    """Return the number of combinations for n choose k.

    Args:
        n (int): the total number of options .
        k (int): The number of elements.

    Returns:
        int: returns the binomial coefficient
    """
    if n == 0:
        return 0
    return reduce(lambda x, y: x * y[0] / y[1],
                  zip(range(n - k + 1, n + 1),
                      range(1, k + 1)), 1)

def bit_string_index(s):
    """Return the index of a string of 0s and 1s."""
    n = len(s)
    k = s.count("1")
    if s.count("0") != n - k:
        raise VisualizationError("s must be a string of 0 and 1")
    ones = [pos for pos, char in enumerate(s) if char == "1"]
    return lex_index(n, k, ones)

def lex_index(n, k, lst):
    """Return  the lex index of a combination..

    Args:
        n (int): the total number of options .
        k (int): The number of elements.
        lst (list): list

    Returns:
        int: returns int index for lex order

    Raises:
        VisualizationError: if length of list is not equal to k
    """
    if len(lst) != k:
        raise VisualizationError("list should have length k")
    comb = list(map(lambda x: n - 1 - x, lst))
    dualm = sum([n_choose_k(comb[k - 1 - i], i + 1) for i in range(k)])
    return int(dualm)

def phase_to_rgb(complex_number):
    """Map a phase of a complexnumber to a color in (r,g,b).

    complex_number is phase is first mapped to angle in the range
    [0, 2pi] and then to the HSL color wheel
    """
    angles = (np.angle(complex_number) + (np.pi * 4)) % (np.pi * 2)
    rgb = colorsys.hls_to_rgb(angles / (np.pi * 2), 0.5, 0.5)
    return rgb

################### This section corresponds to Qiskit code modified by the Qpi team. ###################

def plot_state_qsphere_mod(quantum_circuit, figsize=None, ax=None, show_state_labels=True,
                       show_state_phases=False, use_degrees=False, *,side="FRONT"):
    """Plot the qsphere representation of a quantum state.
    Here, the size of the points is proportional to the probability
    of the corresponding term in the state and the color represents
    the phase.

    Args:
        quantum_circuit (QuantumCircuit): a quantum circuit.
        figsize (tuple): Figure size in inches.
        ax (matplotlib.axes.Axes): An optional Axes object to be used for
            the visualization output. If none is specified a new matplotlib
            Figure will be created and used. Additionally, if specified there
            will be no returned Figure since it is redundant.
        show_state_labels (bool): An optional boolean indicating whether to
            show labels for each basis state.
        show_state_phases (bool): An optional boolean indicating whether to
            show the phase for each basis state.
        use_degrees (bool): An optional boolean indicating whether to use
            radians or degrees for the phase values in the plot.
        side (str): It's the side of the qsphere to be graphed. It can either be "FRONT", "RIGHT", "LEFT" or "BACK"

    Returns:
        Figure: A matplotlib figure instance if the ``ax`` kwag is not set

    Raises:
        ImportError: Requires matplotlib.
        VisualizationError: if input is not a valid N-qubit quantum circuit.


    Example:
        .. jupyter-execute::

        import qpi_lib
        from qpi_lib.qsphere_funcs import plot_state_qsphere_mod
        from qiskit import QuantumCircuit

        qc = QuantumCircuit(2)
        qc.h(0)
        qc.cx(0, 1)

        plot_state_qsphere_mod(quantum_circuit=qc, show_state_labels=False,side="BACK")
    """
    if not HAS_MATPLOTLIB:
        raise ImportError('Must have Matplotlib installed. To install, run "pip install '
                          'matplotlib".')
      
    state = Statevector.from_instruction(quantum_circuit) # Extract the quantum state
    rho = DensityMatrix(state)
    num = rho.num_qubits
    if num is None:
        raise VisualizationError("Input is not a multi-qubit quantum circuit.")
    # get the eigenvectors and eigenvalues
    eigvals, eigvecs = linalg.eigh(rho.data)
    
    plt.style.use('dark_background') # Use a dark background for better hologram visualization

    if figsize is None:
        figsize = (7, 7)

    if ax is None:
        return_fig = True
        fig = plt.figure(figsize=figsize)
    else:
        return_fig = False
        fig = ax.get_figure()

    gs = gridspec.GridSpec(nrows=3, ncols=3)

    ax = fig.add_subplot(gs[0:3, 0:3], projection='3d')
    ax.axes.set_xlim3d(-0.6, 0.6)
    ax.axes.set_ylim3d(-0.6, 0.6)
    ax.axes.set_zlim3d(-0.6, 0.6)
    ax.axes.grid(False)
    ax.view_init(elev=5, azim=275)

    # Force aspect ratio
    # MPL 3.2 or previous do not have set_box_aspect
    if hasattr(ax.axes, 'set_box_aspect'):
        ax.axes.set_box_aspect((1, 1, 1))

    # start the plotting
    # Plot semi-transparent sphere
    u = np.linspace(0, 2 * np.pi, 25)
    v = np.linspace(0, np.pi, 25)
    x = np.outer(np.cos(u), np.sin(v))
    y = np.outer(np.sin(u), np.sin(v))
    z = np.outer(np.ones(np.size(u)), np.cos(v))
    ax.plot_surface(x, y, z, rstride=1, cstride=1, color=plt.rcParams['grid.color'],
                    alpha=0.2, linewidth=0)

    # Get rid of the panes
    ax.w_xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.w_yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.w_zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))

    # Get rid of the spines
    ax.w_xaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
    ax.w_yaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
    ax.w_zaxis.line.set_color((1.0, 1.0, 1.0, 0.0))

    # Get rid of the ticks
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])

    # traversing the eigvals/vecs backward as sorted low->high
    for idx in range(eigvals.shape[0]-1, -1, -1):
        if eigvals[idx] > 0.001:
            # get the max eigenvalue
            state = eigvecs[:, idx]
            loc = np.absolute(state).argmax()
            # remove the global phase from max element
            angles = (np.angle(state[loc]) + 2 * np.pi) % (2 * np.pi)
            angleset = np.exp(-1j * angles)
            state = angleset * state
            
            d = num
            for i in range(2 ** num):
                # get x,y,z points
                element = bin(i)[2:].zfill(num)
                weight = element.count("1")
                zvalue = -2 * weight / d + 1
                number_of_divisions = n_choose_k(d, weight)
                weight_order = bit_string_index(element)
                angle = (float(weight) / d) * (np.pi * 2) + \
                        (weight_order * 2 * (np.pi / number_of_divisions))

                if (weight > d / 2) or ((weight == d / 2) and
                                        (weight_order >= number_of_divisions / 2)):
                    angle = np.pi - angle - (2 * np.pi / number_of_divisions)

                xvalue = np.sqrt(1 - zvalue ** 2) * np.cos(angle)
                yvalue = np.sqrt(1 - zvalue ** 2) * np.sin(angle)

                # get prob and angle - prob will be shade and angle color
                prob = np.real(np.dot(state[i], state[i].conj()))
                if prob > 1:  # See https://github.com/Qiskit/qiskit-terra/issues/4666
                    prob = 1
                colorstate = phase_to_rgb(state[i])

                

                if not np.isclose(prob, 0) and show_state_labels:
                    rprime = 1.3
                    angle_theta = np.arctan2(np.sqrt(1 - zvalue ** 2), zvalue)
                    xvalue_text = rprime * np.sin(angle_theta) * np.cos(angle)
                    yvalue_text = rprime * np.sin(angle_theta) * np.sin(angle)
                    zvalue_text = rprime * np.cos(angle_theta)
                                        
                    element_text = '$\\vert' + element + '\\rangle$'
                    if show_state_phases:
                        element_angle = (np.angle(state[i]) + (np.pi * 4)) % (np.pi * 2)
                        if use_degrees:
                            element_text += '\n$%.1f^\\circ$' % (element_angle * 180/np.pi)
                        else:
                            element_angle = pi_check(element_angle, ndigits=3).replace('pi', '\\pi')
                            element_text += '\n$%s$' % (element_angle)
                    ax.text(xvalue_text, yvalue_text, zvalue_text, element_text,
                            ha='center', va='center', size=12)
                    
                # Calculate the new x, y, and z values after rotation
                news = rotate(xvalue, yvalue, zvalue, side)
                xvalue = news[0]
                yvalue = news[1]
                zvalue = news[2]
                
                # alfa defines the transparency of the dots
                alfa = 1 #alfa=1 means no transparency
                if yvalue >= 0.1:
                    alfa = 1.0 - yvalue
                    
                ax.plot([xvalue], [yvalue], [zvalue],
                        markerfacecolor=colorstate,
                        markeredgecolor=colorstate,
                        marker='o', markersize=np.sqrt(prob) * 40, alpha=alfa)
                
                

                a = Arrow3D([0, xvalue], [0, yvalue], [0, zvalue],
                            mutation_scale=20, alpha=prob, arrowstyle="-",
                            color=colorstate, lw=3)
                ax.add_artist(a)

            # add weight lines
            for weight in range(d + 1):
                theta = np.linspace(-2 * np.pi, 2 * np.pi, 100)
                z = -2 * weight / d + 1
                r = np.sqrt(1 - z ** 2)
                x = r * np.cos(theta)
                y = r * np.sin(theta)
                ax.plot(x, y, z, color=(.5, .5, .5), lw=1, ls=':', alpha=.5)

            # add center point
            ax.plot([0], [0], [0], markerfacecolor=(.5, .5, .5),
                    markeredgecolor=(.5, .5, .5), marker='o', markersize=3,
                    alpha=1)
        else:
            break

    n = 64
    theta = np.ones(n)

    if return_fig:
        dir = 'figures/'
        if not os.path.exists(dir):
            os.makedirs(dir)
        plt.savefig(dir + side + '.jpg',format='jpg',dpi=250.0)
        
        if get_backend() in ['module://ipykernel.pylab.backend_inline',
                             'nbAgg']:
            plt.close(fig)
        return fig

################### This section corresponds to the functions created by the Qpi team. ###################

#side (RIGHT, LEFT , FRONT, BACK)
def rotate(x,y,z,side="FRONT"):
    
    """ Creates the right, left and back views of the qsphere by rotating the position of the state circles.
    Args:
        x (float): x-coordinate of current point in the qsphere
        y (float): y-coordinate of current point in the qsphere
        z (float): z-coordinate of current point in the qsphere
        side (str): side. Can be "RIGHT", "LEFT" , "FRONT" or "BACK"

    Returns:
        If side is not "FRONT":
            nuevo x (float): new x-coordinate of point in the qsphere
            nuevo y (float): new y-coordinate of point in the qsphere
            nuevo z (float): new z-coordinate of point in the qsphere
        Else if side is "FRONT":
            x (float): x-coordinate of current point in the qsphere
            y (float): y-coordinate of current point in the qsphere
            z (float): z-coordinate of current point in the qsphere
    """

    newx = y
    newy = x
    newz = z
    if side != "FRONT":
        if x == 0.0 or y == 0.0:  #If x or y are zero it's because they're on the axis.
            if side == "LEFT":
                if y == 0:  newy = newy * (-1)
            if side == "RIGHT":
                if x == 0:  newx = newx * (-1)
            if side == "BACK":
                newx = x
                newy = y
                if y == 0:  newx = newx * (-1)
                if x == 0:  newy = newy * (-1)
            return [newx,newy,newz]
        else:
            
            if side == "LEFT":
                if (x > 0 and y > 0) or (x < 0 and y < 0): 
                    newy = newy * (-1)
                if x < 0 and y > 0:  #2nd Quadrant
                    newy = newy * (-1)
                if x > 0 and y < 0:  #4th Quadrant
                    newx = newx * (-1)
            if side == "RIGHT":
                if (x > 0 and y > 0) or (x < 0 and y < 0): 
                    newx = newx * (-1)
                if x < 0 and y > 0:  #2nd Quadrant
                    newx = newx * (-1)
                if x > 0 and y < 0:  #4th Quadrant
                    newy = newy * (-1)
            if side == "BACK":
                newx = x
                newy = y
                if (x > 0 and y > 0) or (x < 0 and y < 0): 
                    newx = newx*(-1)
                    newy = newy*(-1)
                if (x > 0 and y < 0) or (x < 0 and y > 0):
                    newx = newx * (-1)
                    newy = newy * (-1)                    
                
            return [newx,newy,newz]
    else:
        return [x,y,z]

def makeHologram(input_front,input_back,input_right,input_left,scale=0.5,scaleR=4,distance=0):
    '''
        Create 3D 4-sided hologram from 4 images (must have equal dimensions)
        Args:
            input_front (jpg, png, ...): frontal image
            input_back (jpg, png, ...): back-side image
            input_right (jpg, png, ...): right-side image
            input_left (jpg, png, ...): left-side image
            scale (float): scale up or down each input image by this factor
            scaleR (float): scales the size of the whole hologram
            distance (): 

        Returns: hologram as a numpy array
    '''
    
    height = int((scale*input_front.shape[0]))
    width = int((scale*input_front.shape[1]))
    
    input_front = cv2.flip(input_front, 1)
    input_back = cv2.flip(input_back, 1)
    input_right = cv2.flip(input_right, 1)
    input_left = cv2.flip(input_left, 1)
    
    input_front = cv2.resize(input_front, (width, height), interpolation = cv2.INTER_CUBIC)
    input_back = cv2.resize(input_back, (width, height), interpolation = cv2.INTER_CUBIC)
    input_right = cv2.resize(input_right, (width, height), interpolation = cv2.INTER_CUBIC)
    input_left = cv2.resize(input_left, (width, height), interpolation = cv2.INTER_CUBIC)
    
    up = input_front.copy()
    down = rotate_bound(input_back.copy(),180)
    right = rotate_bound(input_right.copy(), 90)
    left = rotate_bound(input_left.copy(), 270)
    
    hologram = np.zeros([ int(max(input_front.shape)*scaleR+distance),int(max(input_front.shape)*scaleR+distance),3], input_front.dtype)
    center_x = floor((hologram.shape[0])/2)
    
    vert_x = floor((up.shape[0])/2)
    hologram[0:up.shape[0], center_x-vert_x+distance:center_x+vert_x+distance] = up
    hologram[ hologram.shape[1]-down.shape[1]:hologram.shape[1] , center_x-vert_x+distance:center_x+vert_x+distance] = down
   
    hori_x = floor((right.shape[0])/2)
    hologram[ center_x-hori_x : center_x-hori_x+right.shape[0] , hologram.shape[1]-right.shape[0]+distance : hologram.shape[1]+distance] = right
    hologram[ center_x-hori_x : center_x-hori_x+left.shape[0] , 0+distance : left.shape[0]+distance ] = left

    return hologram

def rotate_bound(image, angle):
    '''
        Rotate an image clockwise by a certain angle (in degrees)
        Args:
            image (jpg, png, ...): image to be rotated
            angle (degrees): rotation angle

        Returns: 
    '''
    # Take the dimensions of the image and then determine the
    # center
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)
 
    # Take the rotation matrix (applying the negative of the
    # angle to rotate clockwise), then take the sine and cosine
    # (i.e., the rotation components of the matrix)
    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])
 
    # Compute the new bounding dimensions of the image
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))
 
    # Adjust the rotation matrix to take into account translation
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY
 
    # Perform the actual rotation and return the image
    return cv2.warpAffine(image, M, (nW, nH))
   
def join_images():
    # Joins the 4 images of the 4 sides, previously exported into the figures folder, into a single jpg image called hologram.
    # Returns: "hologram.jpg" image in the figures folder

    front = cv2.imread("figures/FRONT.jpg")
    back = cv2.imread("figures/BACK.jpg")
    right = cv2.imread("figures/RIGHT.jpg")
    left = cv2.imread("figures/LEFT.jpg")
    holo = makeHologram(front,back,right,left,scale=1.0,scaleR=2.52)
    cv2.imwrite("figures/hologram.jpg",holo)

def plot_qsphere_full(quantum_circuit):
    """
    Generate a jpg image of the qsphere hologram representation of a quantum state, generated by a quantum circuit.
    Here, the size of the points is proportional to the probability
    of the corresponding term in the state and the color represents
    the phase.

    Args:
        quantum_circuit (QuantumCircuit): a quantum circuit.

    Example:
        .. jupyter-execute::

        import qpi_lib
        from qpi_lib.qsphere_funcs import plot_qsphere_full
        from qiskit import QuantumCircuit

        qc = QuantumCircuit(2)
        qc.h(0)
        qc.cx(0, 1)

        plot_state_qsphere_full(qc)
    """
    plot_state_qsphere_mod(quantum_circuit=quantum_circuit, show_state_labels=True,side="FRONT") # Generate front image
    plot_state_qsphere_mod(quantum_circuit=quantum_circuit, show_state_labels=False,side="BACK") # Generate back image
    plot_state_qsphere_mod(quantum_circuit=quantum_circuit, show_state_labels=False,side="LEFT") # Generate left image
    plot_state_qsphere_mod(quantum_circuit=quantum_circuit, show_state_labels=False,side="RIGHT") # Generate right image
    join_images()

