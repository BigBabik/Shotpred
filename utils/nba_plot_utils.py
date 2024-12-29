import matplotlib.pyplot as plt
import matplotlib.lines as lines
import matplotlib.patches as patches


def draw_court():
    """
    The function draws an NBA basketball court.
    """
    fig, ax = plt.subplots(figsize=(12, 11))

    
    # court
    # court
    hoop = patches.Circle((0, 0), 7.5, linewidth=2, color="black", fill=False)
    backboard = patches.Rectangle((-30, -7.5), 60, -1, linewidth=2, color="black")
    outer_box = patches.Rectangle((-80, -47.5), 160, 190, linewidth=2, color="black", fill=False)
    free_throw = patches.Circle((0, 142.5), 60, linewidth=2, color="black", fill=False)
    restricted = patches.Circle((0, 0), 40, linewidth=2, color="black", fill=False)

    # add court elements
    ax.add_patch(hoop)
    ax.add_patch(backboard)
    ax.add_patch(outer_box)
    ax.add_patch(free_throw)
    ax.add_patch(restricted)

    # draw the half court line, baseline and side lines
    base_line = lines.Line2D([-250, 250], [-47.5, -47.5], color="black", linewidth=2)
    ax.add_line(base_line)  # קו תחתון
    left_line = lines.Line2D([-250, -250], [-47.5, 422.5], color="black", linewidth=2)
    ax.add_line(left_line) 
    right_line = lines.Line2D([250, 250], [-47.5, 422.5], color="black", linewidth=2)
    ax.add_line(right_line) 

    #set axis limits
    ax.set_xlim(-250, 250)
    ax.set_ylim(-50, 470)
    ax.set_aspect('equal')
    ax.axis('off')

    return fig, ax


def plot_shot_scatter(shot_data, court_fig=None, court_ax=None, plot_title=None):

    if court_fig is None or court_ax is None:
        court_fig, court_ax = draw_court()

    made_shots = shot_data[shot_data['SHOT_MADE_FLAG'] == 1]
    missed_shots = shot_data[shot_data['SHOT_MADE_FLAG'] == 0]

    court_ax.scatter(made_shots['LOC_X'], made_shots['LOC_Y'], c='green', label="Made", s=10)
    court_ax.scatter(missed_shots['LOC_X'], missed_shots['LOC_Y'], c='red', label="Missed", s=10)

    if plot_title:
        court_fig.suptitle(plot_title, fontsize=15)
    court_fig.legend(loc='upper right')

    return court_fig, court_ax
