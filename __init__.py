from cudatext import *

def do_sort(is_reverse, is_case_sens, del_dups, del_blanks):
    line1, line2 = ed.get_sel_lines()
    if line1>=line2:
        msg_status('Sort: needed multiline selection')
        return
        
    nlines = ed.get_line_count()
    if nlines<2:
        msg_status('Sort: too less lines')
        return
        
    #add last empty ln
    if ed.get_text_line(nlines-1) != '':
        ed.set_text_line(-1, '')
        
    lines = [ed.get_text_line(i) for i in range(line1, line2+1)]
    
    if del_blanks:
        lines = [s for s in lines if s.strip()]
    if del_dups:
        lines = list(set(lines))
    
    key_func = None if is_case_sens else str.lower
    lines = sorted(lines, key=key_func, reverse=is_reverse)
        
    ed.delete(0, line1, 0, line2+1)
    ed.insert(0, line1, '\n'.join(lines)+'\n')
    ed.set_caret(0, line2+1, 0, line1)
    
    count = (line2-line1+1)
    text = 'Sorted %d lines'%count \
        + (', ignore-case' if not is_case_sens else '') \
        + (', desc.' if is_reverse else ', asc.')
    msg_status(text)


def do_dialog():
    size_x = 330
    size_y = 150
    id_rev = 0
    id_nocase = 1
    id_del_dup = 2
    id_del_sp = 3
    id_ok = 4
    
    c1 = chr(1)
    text = '\n'.join([
      c1.join(['type=check', 'pos=6,6,300,0', 'cap=Sort descending (reverse)']),
      c1.join(['type=check', 'pos=6,32,300,0', 'cap=Ignore case']),
      c1.join(['type=check', 'pos=6,58,300,0', 'cap=Delete duplicate lines', 'val=1']),
      c1.join(['type=check', 'pos=6,84,300,0', 'cap=Delete blank lines', 'val=1']),
      c1.join(['type=button', 'pos=60,120,160,0', 'cap=OK']),
      c1.join(['type=button', 'pos=164,120,264,0', 'cap=Cancel']),
      ])
    
    res = dlg_custom('Sort lines', size_x, size_y, text)
    if res is None: return
    btn, text = res
    if btn != id_ok: return
    text = text.splitlines()
    
    is_rev = text[id_rev]=='1'
    is_nocase = text[id_nocase]=='1'
    is_del_dup = text[id_del_dup]=='1'
    is_del_sp = text[id_del_sp]=='1'
    return (is_rev, not is_nocase, is_del_dup, is_del_sp)
    

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
        