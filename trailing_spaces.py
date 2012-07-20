'''
Changed to trim trailing spaces on save command

@author: Jean-Denis Vauguet <jd@vauguet.fr>, Oktay Acikalin <ok@ryotic.de>
@license: MIT (http://www.opensource.org/licenses/mit-license.php)
@since: 2011-02-25
'''

import sublime
import sublime_plugin


# Highlight matching regions.
class TrailingSpacesDeleteListener(sublime_plugin.EventListener):
    def on_pre_save(self, view):
        view.run_command('delete_trailing_spaces')


# Allows to erase matching regions.
class DeleteTrailingSpacesCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        regions = self.view.find_all('[ \t]+$')
        if regions:
            # deleting a region changes the other regions positions, so we
            # handle this maintaining an offset
            offset = 0
            for region in regions:
                r = sublime.Region(region.a + offset, region.b + offset)
                self.view.erase(edit, sublime.Region(r.a, r.b))
                offset -= r.size()

            msg_parts = {"nbRegions": len(regions),
                         "plural":    's' if len(regions) > 1 else ''}
            msg = "Deleted %(nbRegions)s trailing spaces region%(plural)s" % msg_parts
        else:
            msg = "No trailing spaces to delete!"

        sublime.status_message(msg)
