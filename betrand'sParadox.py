import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.lines import Line2D

# Constants
TAU = 2 * np.pi
GREY_COLOR = (0.2, 0.2, 0.2)
NUM_CHORDS_TO_PLOT = 1000

# Number of chords and the length of the chord
num_chords = 10000
circle_radius = 1  
chord_length = circle_radius * np.sqrt(3) 

# Function to set up the axes for plotting
def setup_axes():
    """Set up the two Axes with the circle and correct limits, aspect."""
    fig, axes = plt.subplots(nrows=1, ncols=2, subplot_kw={'aspect': 'equal'})
    for ax in axes:
        circle = Circle((0, 0), circle_radius, facecolor='none')
        ax.add_artist(circle)
        ax.set_xlim((-circle_radius, circle_radius))
        ax.set_ylim((-circle_radius, circle_radius))
        ax.axis('off')
    return fig, axes

# Method 1: Generate random chords and midpoints using "Randomly selected chords by endpoints on circle"
def generate_chords_method1():
    """Generate random chords and midpoints using "Randomly selected chords by endpoints on circle".

    Method 1 selects pairs of uniformly-distributed random points on the unit circle
    and joins them as chords.
    """
    angles = np.random.random((num_chords, 2)) * TAU
    chords = np.array((circle_radius * np.cos(angles), circle_radius * np.sin(angles)))
    chords = np.swapaxes(chords, 0, 1)
    # Calculate midpoints of the chords
    midpoints = np.mean(chords, axis=2).T
    return chords, midpoints

# Method 2: Generate random chords and midpoints using "Distance to the center"
def generate_chords_method2():
    """Generate random chords and midpoints using "Distance to the center".

    Method 2 first selects a random radius of the circle, then chooses a point
    at random (uniformly-distributed) on this radius to be the midpoint of the chord.
    """
    angles = np.random.random(num_chords) * TAU
    radii = np.random.random(num_chords) * circle_radius
    midpoints = np.array((radii * np.cos(angles), radii * np.sin(angles)))
    chords = get_chords_from_midpoints(midpoints)
    return chords, midpoints

# Method 3: Generate random chords and midpoints using "Midpoint of chord"
def generate_chords_method3():
    """Generate random chords and midpoints using "Midpoint of chord".

    Method 3 selects a point at random (uniformly distributed) within the circle
    and considers this point to be the midpoint of the chord.
    """
    angles = np.random.random(num_chords) * TAU
    radii = np.sqrt(np.random.random(num_chords)) * circle_radius
    midpoints = np.array((radii * np.cos(angles), radii * np.sin(angles)))
    chords = get_chords_from_midpoints(midpoints)
    return chords, midpoints

# Helper function to get chords from midpoints for Method 2 and Method 3
def get_chords_from_midpoints(midpoints):
    """Return the chords with the provided midpoints."""
    chords = np.zeros((num_chords, 2, 2))
    for i, (x0, y0) in enumerate(midpoints.T):
        # Equation of the chord: y = mx + c
        m = -x0 / y0
        c = y0 + x0**2 / y0
        # Solve the quadratic equation to find chord endpoints
        A, B, C = m**2 + 1, 2 * m * c, c**2 - circle_radius**2
        d = np.sqrt(B**2 - 4 * A * C)
        x = np.array(((-B + d), (-B - d))) / 2 / A
        y = m * x + c
        chords[i] = (x, y)
    return chords

# Dictionary to store different methods
chord_generation_methods = {
    1: generate_chords_method1,
    2: generate_chords_method2,
    3: generate_chords_method3
}

# Function to get method name
def get_method_name(method_number):
    if method_number == 1:
        return "Randomly selected chords by endpoints on circle"
    elif method_number == 2:
        return "Distance to the center"
    elif method_number == 3:
        return "Midpoint of chord"

# Function to plot chords and midpoints based on selected method
def plot_chords(method_number):
    """Plot the chords and their midpoints for the selected method."""
    chords, midpoints = chord_generation_methods[method_number]()

    # Track chords longer than chord_length
    success = [False] * num_chords

    fig, axes = setup_axes()
    for i, chord in enumerate(chords):
        x, y = chord
        if np.hypot(x[0] - x[1], y[0] - y[1]) > chord_length:
            success[i] = True
        if i < NUM_CHORDS_TO_PLOT:
            line = Line2D(*chord, color=GREY_COLOR, alpha=0.1)
            axes[0].add_line(line)
    axes[1].scatter(*midpoints, s=0.2, color=GREY_COLOR)
    fig.suptitle('Method {}'.format(method_number))

    # Calculate probability of chords longer than chord_length
    prob = np.sum(success) / num_chords
    method_name = get_method_name(method_number)
    print(f'Probability of chords longer than chord length, {method_name}: {prob}')
    plt.savefig(f'chords_{method_name.replace(" ", "_").lower()}.png')
    plt.show()

# Plot for each method
plot_chords(1)
plot_chords(2)
plot_chords(3)
