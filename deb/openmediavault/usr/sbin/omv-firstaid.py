#!/usr/bin/env python3
#
# This file is part of OpenMediaVault.
#
# @license   http://www.gnu.org/licenses/gpl.html GPL Version 3
# @author    Volker Theile <volker.theile@openmediavault.org>
# @copyright Copyright (c) 2009-2016 Volker Theile
#
# OpenMediaVault is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# OpenMediaVault is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with OpenMediaVault. If not, see <http://www.gnu.org/licenses/>.
import os
import sys
import dialog
import openmediavault as omv

def load_plugins():
	plugins = []
	path = omv.getenv("OMV_FIRSTAID_MODULES_DIR",
		"/usr/share/openmediavault/firstaid/modules.d");
	sys.path.insert(0, path)
	for name in os.listdir(path):
	    modname, ext = os.path.splitext(name)
	    if ext == ".py":
	        mod = __import__(modname)
	        plugins.append(mod.Plugin())
	sys.path.pop(0)
	return plugins

def main():
	rc = 1
	pi = omv.ProductInfo();
	# Load the plugins.
	plugins = load_plugins()
	# Fill the menu choices.
	choices = []
	for idx, plugin in enumerate(plugins):
		choices.append([ str(idx + 1), plugin.get_description() ])
	# Show the available plugins.
	d = dialog.Dialog(dialog="dialog")
	while 1:
		(code, tag) = d.menu("Please select a menu:",
			title="First aid", no_cancel=True, clear=True,
			backtitle="{} - {}".format(pi.get_name(), pi.get_copyright()),
			height=15, width=65, menu_height=8, choices=choices)
		if code in (d.CANCEL, d.ESC):
			rc = 0; break
		elif code == d.OK:
			d.clear()
			plugin = plugins[int(tag) - 1]
			rc = plugin.execute()
			break
	return rc

if __name__ == "__main__":
	sys.exit(main())