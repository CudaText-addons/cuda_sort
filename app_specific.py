from cudatext import *

def ed_insert_to_lines(lines, line1, line2):
    ed.delete(0, line1, 0, line2+1)
    ed.insert(0, line1, '\n'.join(lines)+'\n')
    ed.set_caret(0, line2+1, 0, line1)

def ed_set_tab_title(s):
    ed.set_prop(PROP_TAB_TITLE, s)

def ed_convert_tabs_to_spaces(s):
    return ed.convert(CONVERT_LINE_TABS_TO_SPACES, 0, 0, s)
   
def msg_show_error(s):
    msg_box(s, MB_OK+MB_ICONERROR)
