# -*- coding: utf-8 -*-
"""
/***************************************************************************
 morph_live_viewDialog
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
"""

from PyQt4 import QtCore, QtGui
from ui_morph_live_view import Ui_morph_live_view
# create the dialog for zoom to point


class morph_live_viewDialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_morph_live_view()
        self.ui.setupUi(self)
