"""
GUISCRCPY by srevinsaju
Get it on : https://github.com/srevinsaju/guiscrcpy
Licensed under GNU Public License

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import sys
import uuid

from PyQt5 import QtCore
from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QMainWindow

from guiscrcpy.lib.toolkit import UXMapper
from guiscrcpy.ui.toolkit import Ui_ToolbarPanel


class InterfaceToolkit(QMainWindow, Ui_ToolbarPanel):
    def __init__(self, ux_mapper=None, parent=None, frame=False):
        """
        Side panel toolkit for guiscrcpy main window
        :param ux_mapper:
        :param parent:
        :param frame:
        """
        QMainWindow.__init__(self)
        Ui_ToolbarPanel.__init__(self)
        self.name = "toolkit"
        self.uid = uuid.uuid4()
        self.setupUi(self)
        self.parent = parent
        self.oldPos = None
        self.ux = None
        if not frame:
            self.setWindowFlags(
                QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint
            )
        if ux_mapper:
            self.ux = ux_mapper
        else:
            self.ux = UXMapper()

    def init(self):
        self.clipD2PC.clicked.connect(self.ux.copy_devpc)
        self.clipPC2D.clicked.connect(self.ux.copy_pc2dev)
        self.back.clicked.connect(self.ux.key_back)
        self.screenfreeze.clicked.connect(self.quit_window)
        self.appswi.clicked.connect(self.ux.key_switch)
        self.menuUI.clicked.connect(self.ux.key_menu)
        self.home.clicked.connect(self.ux.key_home)
        self.notif_pull.clicked.connect(self.ux.expand_notifications)
        self.notif_collapse.clicked.connect(self.ux.collapse_notifications)
        self.fullscreenUI.clicked.connect(self.ux.fullscreen)
        self.powerUI.clicked.connect(self.ux.key_power)
        self.vup.clicked.connect(self.ux.key_volume_up)
        self.vdown.clicked.connect(self.ux.key_volume_down)
        self.potraitUI.clicked.connect(self.ux.reorientP)
        self.landscapeUI.clicked.connect(self.ux.reorientL)
        self.colorize()  # give a unique color for each device
        self.show()

    def colorize(self):
        hexdigest = self.ux.get_sha()[:6]
        self.tk_device_id.setStyleSheet(f"background-color: #{hexdigest};")

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        try:
            delta = QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()
        except (TypeError, AttributeError):
            pass

    def quit_window(self):
        for instance in self.parent.child_windows:
            # We are checking for any more windows running before killing
            # the main window. self.child_windows has the list of all
            # objects spawned by the main window ui
            # This method checks if we are the last member of the windows
            # spawned and we ourselves are not a member of ourself by
            # checking the uuid generated on creation
            if not instance.isHidden() \
                    and instance.name != "swipe" and instance.uid != \
                    self.uid:
                self.hide()
                break
        else:
            sys.exit()
