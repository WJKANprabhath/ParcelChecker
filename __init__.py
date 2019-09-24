# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ParcelChecker
                                 A QGIS plugin
 To convert cad plan to shapfile
                             -------------------
        begin                : 2019-09-23
        copyright            : (C) 2019 by Prabhath W.J.K.A.N. Survey Dept. of Sri Lanka
        email                : npjasinghe@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load ParcelChecker class from file ParcelChecker.

    :param iface: A QGIS interface instance.
    :type iface: QgisInterface
    """
    #
    from .Parcel_Checker import ParcelChecker
    return ParcelChecker(iface)
