#-----------------------------------------------------------------------------
# Copyright (c) 2012 - 2017, Anaconda, Inc. All rights reserved.
#
# Powered by the Bokeh Development Team.
#
# The full license is in the file LICENSE.txt, distributed with this software.
#-----------------------------------------------------------------------------
''' Helper functions for applying client-side computations such as
transformations to data fields or ``ColumnDataSource`` expressions.

'''

#-----------------------------------------------------------------------------
# Boilerplate
#----------------------------------------------------------------------------
from __future__ import absolute_import, division, print_function, unicode_literals

import logging
log = logging.getLogger(__name__)

from bokeh.util.api import public, internal ; public, internal

#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

# Standard library imports

# External imports

# Bokeh imports
from .core.properties import expr, field
from .models.expressions import Stack
from .models.mappers import CategoricalColorMapper, LinearColorMapper, LogColorMapper
from .models.transforms import Dodge, Jitter

#-----------------------------------------------------------------------------
# Globals and constants
#-----------------------------------------------------------------------------

__all__ = (
    'dodge',
    'factor_cmap',
    'jitter',
    'linear_cmap',
    'log_cmap',
    'stack',
    'transform',
)

#-----------------------------------------------------------------------------
# Public API
#-----------------------------------------------------------------------------

@public((1,0,0))
def dodge(field_name, value, range=None):
    ''' Create a ``DataSpec`` dict to apply a client-side ``Jitter``
    transformation to a ``ColumnDataSource`` column.

    Args:
        field_name (str) : a field name to configure ``DataSpec`` with

        value (float) : the fixed offset to add to column data

        range (Range, optional) : a range to use for computing synthetic
            coordinates when necessary, e.g. a ``FactorRange`` when the
            column data is categorical (default: None)

    Returns:
        dict

    '''
    return field(field_name, Dodge(value=value, range=range))

@public((1,0,0))
def factor_cmap(field_name, palette, factors, start=0, end=None, nan_color="gray"):
    ''' Create a ``DataSpec`` dict to apply a client-side
    ``CategoricalColorMapper`` transformation to a ``ColumnDataSource``
    column.

    Args:
        field_name (str) : a field name to configure ``DataSpec`` with

        palette (seq[color]) : a list of colors to use for colormapping

        factors (seq) : a sequences of categorical factors corresponding to
            the palette

        start (int, optional) : a start slice index to apply when the column
            data has factors with multiple levels. (default: 0)

        end (int, optional) : an end slice index to apply when the column
            data has factors with multiple levels. (default: None)

        nan_color (color, optional) : a default color to use when mapping data
            from a column does not succeed (default: "gray")

    Returns:
        dict

    '''
    return field(field_name, CategoricalColorMapper(palette=palette,
                                                    factors=factors,
                                                    start=start,
                                                    end=end,
                                                    nan_color=nan_color))

@public((1,0,0))
def jitter(field_name, width, mean=0, distribution="uniform", range=None):
    ''' Create a ``DataSpec`` dict to apply a client-side ``Jitter``
    transformation to a ``ColumnDataSource`` column.

    Args:
        field_name (str) : a field name to configure ``DataSpec`` with

        width (float) : the width of the random distribition to apply

        mean (float, optional) : an offset to apply (default: 0)

        distribution (str, optional) : ``"uniform"`` or ``"normal"``
            (default: ``"uniform"``)

        range (Range, optional) : a range to use for computing synthetic
            coordinates when necessary, e.g. a ``FactorRange`` when the
            column data is categorical (default: None)

    Returns:
        dict

    '''
    return field(field_name, Jitter(mean=mean,
                                    width=width,
                                    distribution=distribution,
                                    range=range))

@public((1,0,0))
def linear_cmap(field_name, palette, low, high, low_color=None, high_color=None, nan_color="gray"):
    ''' Create a ``DataSpec`` dict to apply a client-side ``LinearColorMapper``
    transformation to a ``ColumnDataSource`` column.

    Args:
        field_name (str) : a field name to configure ``DataSpec`` with

        palette (seq[color]) : a list of colors to use for colormapping

        low (float) : a minimum value of the range to map into the palette.
            Values below this are clamped to ``low``.

        high (float) : a maximum value of the range to map into the palette.
            Values above this are clamped to ``high``.

        low_color (color, optional) : color to be used if data is lower than
            ``low`` value. If None, values lower than ``low`` are mapped to the
            first color in the palette. (default: None)

        high_color (color, optional) : color to be used if data is higher than
            ``high`` value. If None, values higher than ``high`` are mapped to
            the last color in the palette. (default: None)

        nan_color (color, optional) : a default color to use when mapping data
            from a column does not succeed (default: "gray")

    '''
    return field(field_name, LinearColorMapper(palette=palette,
                                               low=low,
                                               high=high,
                                               nan_color=nan_color,
                                               low_color=low_color,
                                               high_color=high_color))

@public((1,0,0))
def log_cmap(field_name, palette, low, high, low_color=None, high_color=None, nan_color="gray"):
    ''' Create a ``DataSpec`` dict to apply a client-side ``LogColorMapper``
    transformation to a ``ColumnDataSource`` column.

    Args:
        field_name (str) : a field name to configure ``DataSpec`` with

        palette (seq[color]) : a list of colors to use for colormapping

        low (float) : a minimum value of the range to map into the palette.
            Values below this are clamped to ``low``.

        high (float) : a maximum value of the range to map into the palette.
            Values above this are clamped to ``high``.

        low_color (color, optional) : color to be used if data is lower than
            ``low`` value. If None, values lower than ``low`` are mapped to the
            first color in the palette. (default: None)

        high_color (color, optional) : color to be used if data is higher than
            ``high`` value. If None, values higher than ``high`` are mapped to
            the last color in the palette. (default: None)

        nan_color (color, optional) : a default color to use when mapping data
            from a column does not succeed (default: "gray")

    '''
    return field(field_name, LogColorMapper(palette=palette,
                                            low=low,
                                            high=high,
                                            nan_color=nan_color,
                                            low_color=low_color,
                                            high_color=high_color))

@public((1,0,0))
def stack(*fields):
    ''' Create a Create a ``DataSpec`` dict to generate a ``Stack`` expression
    for a ``ColumnDataSource``.

    Examples:

        .. code-block:: python

            p.vbar(bottom=stack("sales", "marketing"), ...

        will generate a ``Stack`` that sums the ``"sales"`` and ``"marketing"``
        columns of a data source, and use those values as the ``top``
        coordinate for a ``VBar``.

    '''
    return expr(Stack(fields=fields))

@public((1,0,0))
def transform(field_name, transform):
    ''' Create a ``DataSpec`` dict to apply an arbitrary client-side
    ``Transform`` to a ``ColumnDataSource`` column.

    Args:
        field_name (str) : A field name to configure ``DataSpec`` with

        transform (Transform) : A transforms to apply to that field

    Returns:
        dict

    '''
    return field(field_name, transform)

#-----------------------------------------------------------------------------
# Internal API
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Private API
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Code
#-----------------------------------------------------------------------------
