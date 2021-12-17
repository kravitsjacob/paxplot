"""Core parapy functions"""

import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import cm
import numpy as np


def scale_val(val, minimum, maximum):
    """
    Scale a value linearly between a minimum and maximum value

    :param val: numeric
        Numeric value to be scaled
    :param minimum: numeric
        Minimum value to linearly scale between
    :param maximum: numeric
        Maximum value to lineraly scale between
    :return: val_scaled:numeric
        Scale `val`
    """
    try:
        val_scaled = (val-minimum)/(maximum-minimum)
    except ZeroDivisionError:
        val_scaled = 0.5
    return val_scaled


def get_data_lims(data, cols):
    """
    Get minimum and maximum value for each column

    :param data: list
        List of dictionaries containing the contents of data from `parallel`
    :param cols: list
        Columns to be plotted from `parallel`
    :return: cols_lims: dict
        Dictionary of column limits corresponding to columns in `cols` in form:
        {
            col1: [lower, upper],
            col2: [lower, upper],
            ...
        }
    """
    cols_lims = {}
    for col in cols:
        col_data = [row[col] for row in data]
        cols_lims[col] = [min(col_data), max(col_data)]

    return cols_lims


def get_color_gradient(data, color_col, colormap):
    """
    Get color gradient values for the `color_col` in `data` based on the
    `colormap` specification.

    :param data: list
        List of dictionaries containing the contents of data from `parallel`
    :param color_col: str
        Column in `data` to use for coloring
    :param colormap: str
        Matplotlib colormap to use for coloring
    :return: data_color: list
        List of hex values corresponding to each row in `data`
    """
    # Get Data
    color_cor_data = [row[color_col] for row in data]

    # Scale Data and get color
    minimum = min(color_cor_data)
    maximum = max(color_cor_data)
    data_color = [
        mpl.colors.rgb2hex(cm.get_cmap(colormap)(
            scale_val(i, minimum, maximum))[:3]
        ) for i in color_cor_data
    ]

    return data_color


def create_colorbar(fig, cols_lims, color_col, color_col_colormap):
    """
    Create and add colorbar to plot

    :param fig: matplotlib.figure.Figure
        Matplotlib figure
    :param cols_lims: dict
        Dictionary of column limits corresponding to columns in `cols` in form:
        {
            col1: [lower, upper],
            col2: [lower, upper],
            ...
        }
    :param color_col: str
        Column in `data` to use for coloring
    :param color_col_colormap: str
        Matplotlib colormap to use for coloring

    :return: fig: matplotlib.figure.Figure
        Matplotlib figure
    """
    # Adjusting bounds automatically (based of previous axes)
    colorbar_bounds = list(fig.axes[-2].get_position().bounds)
    colorbar_bounds[0] = colorbar_bounds[0] + 0.1  # Left starting
    colorbar_bounds[2] = colorbar_bounds[2] / 5  # Width

    # Create colorbar
    colorbar_ax = plt.axes(colorbar_bounds)
    cmap = cm.get_cmap(color_col_colormap)
    norm = mpl.colors.Normalize(
        vmin=cols_lims[color_col][0],
        vmax=cols_lims[color_col][1]
    )
    mpl.colorbar.ColorbarBase(
        colorbar_ax,
        cmap=cmap,
        norm=norm,
        orientation='vertical',
        label=color_col
    )

    # Add colorbar
    fig.axes[-1] = colorbar_ax

    return fig


def format_axes(
        ax,
        labs,
        minimum,
        maximum,
        invert=False,
        n_ticks=10,
        precision=2,
        last=False
):
    """
    Format AxesSubplot objects. This includes changing limit, ticks, and other
    various formatting quantities.

    :param ax: matplotlib.axes._subplots.AxesSubplot
        AxesSubplot to be modified
    :param labs: list
        List of labels for y axis. If last column this will be a list of length
        two.
    :param minimum: numeric
        Minimum value in column
    :param maximum: numeric
        Maximum value in column
    :param invert: boolean
        Whether or not column is inverted
    :param n_ticks: int
        Number of ticks
    :param precision: int
        Number of decimal places for rounding
    :param last: boolean
        Is this the last axes?
    """
    # Remove axes frame
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    # Set limits
    ax.set_ylim([0, 1])
    ax.set_xlim([0, 1])

    # Change ticks to reflect scaled data
    if maximum == minimum:
        ax.set_yticks(ticks=[0.5], labels=[maximum])
    else:
        # Get tick locations
        if invert:
            ticks = np.linspace(1, 0, num=n_ticks + 1)
        else:
            ticks = np.linspace(0, 1, num=n_ticks + 1)

        # Get tick labels
        tick_labels = np.linspace(
            minimum,
            maximum,
            num=n_ticks + 1
        )
        tick_labels = tick_labels.round(precision)

        # Set Ticks
        ax.set_yticks(ticks=ticks, labels=tick_labels)

    if not last:
        # Set Label
        ax.set_xticks([0], [labs])
    else:
        # Set Label
        ax.set_xticks([0, 1], labs)


def parallel(
        data,
        cols,
        cols_invert=(),
        color_col=None,
        color_col_colormap='viridis',
        custom_lims=None,
        colorbar=False,
        figsize=None
):
    """
    Create static parallel plot in Matplotlib.

    Shouts to Been Alex Keen for giving example of underlying logic on their
    website: https://benalexkeen.com/parallel-coordinates-in-matplotlib/

    :param data: list
        List of dictionaries containing the contents of data to be plotted.
        This has the form:
        [
            {col1: val1, col2: val1 ...},
            {col1: val2, col2: val2 ...}
            ...
        ]
    :param cols: list
        Columns to be plotted
    :param cols_invert: list
        Columns to invert in plotted. Must be a subset of cols.
    :param color_col: str
        Column in `data` to use for coloring
    :param color_col_colormap: str
        Matplotlib colormap to use for coloring
    :param custom_lims: dict
        Dictionary of custom column limits corresponding to columns in `cols`.
        Must be of the form:
        {
            col1: [lower, upper],
            col2: [lower, upper],
            ...
        }
    :param colorbar: boolean
        Should a colorbar be created?
    :param figsize: (float, float)
        Matplotlib figsize argument: width, height in inches.

    :return: fig: matplotlib.figure.Figure
        Matplotlib figure

    """

    # Input error checking

    # Getting color data
    if cols_invert is None:
        cols_invert = []
    if color_col is not None:
        data_color = get_color_gradient(data, color_col, color_col_colormap)

    # Setting automatic figsize
    if figsize is None:
        height = 4
        width = 2 * len(cols)
        figsize = (width, height)

    # Setting automatic column limits
    if custom_lims is not None:
        cols_lims = custom_lims
    else:
        cols_lims = get_data_lims(data, cols)

    # Initializing figures
    if colorbar:
        # Create extra axes for colorbar (creates space)
        fig, axes = plt.subplots(
            1,
            len(cols),
            sharey=False,
            figsize=figsize
        )
        fig.axes[-1].axis('off')  # Don't show axes though
        # Don't consider that axes for plotting
        axes = axes[:-1]

    else:
        fig, axes = plt.subplots(
            1,
            len(cols) - 1,
            sharey=False,
            figsize=figsize
        )
    if len(cols) == 2:  # If only two columns are plotted
        axes = [axes]

    # Plot each column pair at a time (axes)
    for ax_idx, ax in enumerate(axes):
        # Plot each line
        for row_idx, row in enumerate(data):
            # Scale the data
            y_0_scaled = scale_val(
                val=row[cols[ax_idx]],
                minimum=cols_lims[cols[ax_idx]][0],
                maximum=cols_lims[cols[ax_idx]][1]
            )
            if cols[ax_idx] in cols_invert:
                y_0_scaled = 0.5 - y_0_scaled + 0.5
            y_1_scaled = scale_val(
                val=row[cols[ax_idx + 1]],
                minimum=cols_lims[cols[ax_idx + 1]][0],
                maximum=cols_lims[cols[ax_idx + 1]][1]
            )
            if cols[ax_idx + 1] in cols_invert:
                y_1_scaled = 0.5 - y_1_scaled + 0.5

            # Line Coloring
            if color_col is not None:
                color = data_color[row_idx]
            else:
                color = ''

            # Plot the data
            x = [0, 1]  # Assume each axes has a length between 0 and 1
            y = [y_0_scaled, y_1_scaled]
            ax.plot(x, y, color)
        # Axes formatting
        if cols[ax_idx] in cols_invert:
            invert = True
        else:
            invert = False
        format_axes(
            ax=ax,
            labs=cols[ax_idx],
            minimum=cols_lims[cols[ax_idx]][0],
            maximum=cols_lims[cols[ax_idx]][1],
            invert=invert
        )

    # Last axes formatting
    last_ax = plt.twinx(axes[-1])
    format_axes(
        ax=last_ax,
        labs=cols[-2:],
        minimum=cols_lims[cols[-1]][0],
        maximum=cols_lims[cols[-1]][1],
        last=True

    )

    # Remove space between plots
    subplots_adjust_args = {
        'wspace': 0.0,
        'hspace': 0.0
    }
    fig.subplots_adjust(**subplots_adjust_args)

    # Add colorbar
    if colorbar:
        create_colorbar(fig, cols_lims, color_col, color_col_colormap)

    # Format ticks
    return fig
