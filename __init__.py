# -*- coding: utf-8 -*-
"""
/***************************************************************************
 morph_live_view
                                 A QGIS plugin
 MORPH live view
                             -------------------
        begin                : 2013-08-06
        copyright            : (C) 2013 by ecki
        email                : ecki@ecki-netz.de
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


def name():
    return "MORPH live view"


def description():
    return "MORPH live view"


def version():
    return "Version 0.1"


def icon():
    return "icon.png"


def qgisMinimumVersion():
    return "1.8"

def author():
    return "ecki"

def email():
    return "ecki@ecki-netz.de"

def classFactory(iface):
    # load morph_live_view class from file morph_live_view
    from morph_live_view import morph_live_view
    return morph_live_view(iface)
