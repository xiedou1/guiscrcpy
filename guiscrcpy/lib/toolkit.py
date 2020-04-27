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
import hashlib
import logging
import os

from guiscrcpy.lib.check import adb

try:
    import pyautogui as auto
    from pygetwindow import getWindowsWithTitle
except Exception as e:
    logging.debug("pygetwindow, pyautogui failed with error code {}".format(e))
    auto = None
    getWindowsWithTitle = None


class UXMapper:
    def __init__(self, device_id=None):
        """
        The main class for UXMapper and adb shell spawn to device
        The guiscrcpy client passes information ot the UXMapper which
        spawns adb subprocesses to handle button and tap events
        :param device_id:
        """
        logging.debug("Launching UX Mapper")
        self.has_modules = getWindowsWithTitle and auto
        logging.debug("Calculating Screen Size")
        self.android_dimensions = adb.get_dimensions(
            adb.path, device_id=device_id)
        self.deviceId = device_id

        # each device connected is uniquely identified by the tools by
        # a salted hash. The toolkits are assigned colors based on the first
        # 6 colors and the stylesheet is derived from
        self.__sha = hashlib.sha256(str(self.deviceId).encode()).hexdigest()

    def get_sha(self):
        """
        A method which returns the unique UUID of the the device
        :return: The hexdigest of a salted hash
        """
        return self.__sha

    def do_swipe(self, x1=10, y1=10, x2=10, y2=10):
        """
        Performs a basic swipe operation
        :param x1: x1 coordinate
        :param y1: y1 coordinate
        :param x2: x2 coordinate
        :param y2: y2 coordinate
        :return: Boolean True, in success
        """
        adb.shell_input(adb.path, "swipe {} {} {} {}".format(
            x1, y1, x2, y2), device_id=self.deviceId)
        return True

    def do_keyevent(self, key):
        """
        Performs a key event on adb
        :param key: The ADB predefined keycode
        :return:
        """
        adb.shell_input(adb.path, "keyevent {}".format(key),
                        device_id=self.deviceId)
        return True

    def copy_devpc(self):
        if self.has_modules:
            scrcpywindow = getWindowsWithTitle("scrcpy")[0]
            scrcpywindow.focus()
            auto.hotkey("ctrl", "c")
        else:
            os.system(
                "wmctrl -x -a  scrcpy && xdotool key --clearmodifiers ctrl+c")

    def key_power(self):
        logging.debug("Passing POWER")
        self.do_keyevent(26)

    def key_menu(self):
        logging.debug("Passing MENU")
        self.do_keyevent(82)

    def key_back(self):
        logging.debug("Passing BACK")
        self.do_keyevent(4)

    def key_volume_up(self):
        logging.debug("Passing BACK")
        self.do_keyevent(24)

    def key_volume_down(self):
        logging.debug("Passing BACK")
        self.do_keyevent(25)

    def key_home(self):
        logging.debug("Passing HOME")
        self.do_keyevent(3)

    def key_switch(self):
        logging.debug("Passing APP_SWITCH")
        self.do_keyevent("KEYCODE_APP_SWITCH")

    def reorientP(self):
        logging.debug("Passing REORIENT [POTRAIT]")
        adb.shell(adb.path, 'settings put system accelerometer_rotation 0',
                  device_id=self.deviceId)
        adb.shell(adb.path, "settings put system rotation 1",
                  device_id=self.deviceId)

    def reorientL(self):
        logging.debug("Passing REORIENT [LANDSCAPE]")
        adb.shell(adb.path, 'settings put system accelerometer_rotation 0',
                  device_id=self.deviceId)
        adb.shell(adb.path, "settings put system rotation 1",
                  device_id=self.deviceId)

    def expand_notifications(self):
        logging.debug("Passing NOTIF EXPAND")
        self.do_swipe(0, 0, 0, int(self.android_dimensions[1]) - 1)

    def collapse_notifications(self):
        logging.debug("Passing NOTIF COLLAPSE")
        self.do_swipe(0, int(self.android_dimensions[1]) - 1, 0, 0)

    def copy_pc2dev(self):
        if self.has_modules:
            scrcpywindow = getWindowsWithTitle("scrcpy")[0]
            scrcpywindow.focus()
            auto.hotkey("ctrl", "shift", "c")
            logging.warning("NOT SUPPORTED ON WINDOWS")
        else:
            os.system(
                "wmctrl -x -a  scrcpy && xdotool key --clearmodifiers ctrl+shift+c")

    def fullscreen(self):
        if self.has_modules:
            scrcpywindow = getWindowsWithTitle("scrcpy")[0]
            scrcpywindow.focus()
            auto.hotkey("ctrl", "f")
        else:
            os.system(
                "wmctrl -x -a  scrcpy && xdotool key --clearmodifiers ctrl+f")
