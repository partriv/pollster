'''
Created on Apr 25, 2009

@author: par
'''

def setup_page_hash(paginator, page_num, page_link_prefix):
    
    page = paginator.page(page_num)
    pageHash = {}
    pageHash["page_num"] = int(page_num)
    pageHash["has_other_pages"] = page.has_other_pages()
    pageHash["start_index"] = page.start_index()
    pageHash["end_index"] = page.end_index()
    pageHash["has_next"] = page.has_next()
    
    pageHash["next_page_number"] = page.next_page_number() if page.has_next() else None
    pageHash["has_previous"] = page.has_previous()

    pageHash["previous_page_number"] = page.previous_page_number() if page.has_previous() else None
    pageHash["page_link_prefix"] = page_link_prefix
    
    pageHash["last_page"] = len(paginator.page_range)
    
    return pageHash