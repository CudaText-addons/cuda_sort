import os
import cudatext
from cudatext import *

fn_ini = os.path.join(app_path(APP_DIR_SETTINGS), 'cuda_sort.ini')
section = 'op'

def do_sort(is_reverse, is_nocase, del_dups, del_blanks,
            offset1, offset2):
    nlines = ed.get_line_count()
    line1, line2 = ed.get_sel_lines()
    if line1>=line2:
        msg_status('Sort: needed multiline selection')
        return
        
    #add last empty line
    if ed.get_text_line(nlines-1) != '':
        ed.set_text_line(-1, '')
        
    lines = [ed.get_text_line(i) for i in range(line1, line2+1)]
    
    if del_blanks:
        lines = [s for s in lines if s.strip()]
    if del_dups:
        lines = list(set(lines))

    is_new_api = hasattr(cudatext, 'CONVERT_LINE_TABS_TO_SPACES')
    def _key(item):
        s = item
        if is_nocase: s = s.lower()

        if (offset1>=0) or (offset2>=0):
            if is_new_api:
                s = ed.convert(CONVERT_LINE_TABS_TO_SPACES, 0, 0, s)
            if offset2>=0: s = s[:offset2]
            if offset1>=0: s = s[offset1:]
            
        return s
    
    lines = sorted(lines, key=_key, reverse=is_reverse)
        
    ed.delete(0, line1, 0, line2+1)
    ed.insert(0, line1, '\n'.join(lines)+'\n')
    ed.set_caret(0, line2+1, 0, line1)
    
    count = (line2-line1+1)
    text = 'Sorted %d lines'%count \
        + (', ignore-case' if is_nocase else '') \
        + (', desc.' if is_reverse else ', asc.') \
        + (', offsets %d..%d' % (offset1, offset2) if (offset1>=0) or (offset2>=0) else '')
    msg_status(text)


def do_dialog():
    size_x = 330
    size_y = 220
    id_rev = 0
    id_nocase = 1
    id_del_dup = 2
    id_del_sp = 3
    id_offset1 = 6
    id_offset2 = 8
    id_ok = 9
    
    op_rev = ini_read(fn_ini, section, 'rev', '0')
    op_nocase = ini_read(fn_ini, section, 'nocase', '0')
    op_del_dup = ini_read(fn_ini, section, 'del_dup', '1')
    op_del_sp = ini_read(fn_ini, section, 'del_sp', '1')
    
    c1 = chr(1)
    text = '\n'.join([
      c1.join(['type=check', 'pos=6,6,300,0', 'cap=&Sort descending (reverse)', 'val='+op_rev]),
      c1.join(['type=check', 'pos=6,30,300,0', 'cap=&Ignore case', 'val='+op_nocase]),
      c1.join(['type=check', 'pos=6,54,300,0', 'cap=Delete d&uplicate lines', 'val='+op_del_dup]),
      c1.join(['type=check', 'pos=6,78,300,0', 'cap=Delete &blank lines', 'val='+op_del_sp]),
      c1.join(['type=label', 'pos=6,106,300,0', 'cap=Sort only by substring, offsets 0-based:']),
      c1.join(['type=label', 'pos=30,128,130,0', 'cap=&From:']),
      c1.join(['type=spinedit', 'pos=30,146,110,0', 'props=-1,1000,1', 'val=-1']),
      c1.join(['type=label', 'pos=120,128,230,0', 'cap=&To:']),
      c1.join(['type=spinedit', 'pos=120,146,200,0', 'props=-1,1000,1', 'val=-1']),
      c1.join(['type=button', 'pos=60,190,160,0', 'cap=OK']),
      c1.join(['type=button', 'pos=164,190,264,0', 'cap=Cancel']),
      ])
    
    res = dlg_custom('Sort lines', size_x, size_y, text)
    if res is None: return
    btn, text = res
    if btn != id_ok: return
    text = text.splitlines()
    
    ini_write(fn_ini, section, 'rev', text[id_rev])
    ini_write(fn_ini, section, 'nocase', text[id_nocase])
    ini_write(fn_ini, section, 'del_dup', text[id_del_dup])
    ini_write(fn_ini, section, 'del_sp', text[id_del_sp])
    
    is_rev = text[id_rev]=='1'
    is_nocase = text[id_nocase]=='1'
    is_del_dup = text[id_del_dup]=='1'
    is_del_sp = text[id_del_sp]=='1'
    offset1 = int(text[id_offset1])
    offset2 = int(text[id_offset2])
    
    if (offset1>=0) and (offset2>=0) and (offset1>=offset2):
        msg_box('Incorrect offsets: %d..%d' % (offset1, offset2), MB_OK + MB_ICONERROR)
        return
    
    return (is_rev, is_nocase, is_del_dup, is_del_sp, offset1, offset2)
    

class Command:
    def sort_asc(self):
        do_sort(False, True, False, True)
    def sort_desc(self):
        do_sort(True, True, False, True)
        
    def sort_asc_nocase(self):
        do_sort(False, False, False, True)
    def sort_desc_nocase(self):
        do_sort(True, False, False, True)

    def sort_dlg(self):
        res = do_dialog()
        if res is None: return
        do_sort(*res)
        