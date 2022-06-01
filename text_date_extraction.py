#from dateutil import parser
from datetime import datetime
import re

def extract_date(text):

    #pattern = "([0-9]{0,2})[/.-]*\s*([0-9]{2,4})[/.-]*\s*([0-9]{2,4})" 

    # Detect dd.mm.yyyy, dd.mm.yy, dd/mm/yyyy, dd/mm/yy, dd-mm-yyyy, dd-mm-yy  
    pattern = "(([0-9]{2})?(\-|\.|\/)([0-9]{2})?(\-|\.|\/)([0-9]{2,4})?)"
    match_string = re.search(pattern, text)
    
    if match_string is None:
        # Detect mm.yyyy, mm.yy, mm/yy, mm/yyyy, mm-yy, mm-yyyy
        pattern = "(([0-9]{2})(\-|\.|\/)([0-9]{2,4})?)"
        match_string = re.search(pattern, text)
    
    if match_string is None:
        return False

    format = ["%d-%m-%Y", "%d/%m/%Y", "%d/ %m/ %Y", "%d.%m.%Y", "%d%m%Y", "%d %m %Y", "%d %b %Y", "%d-%m-%y", "%d/%m/%y", "%d/ %m/ %y", "%d.%m.%y", "%d%m%y", "%d %m %y", "%d %b %y", "%m %Y", "%m %y", "%m.%Y", "%m.%y", "%m/%Y", "%m/%y", "%m. %Y", "%m. %y"]  
    for fmt in format:
        try:
            res = datetime.strptime(match_string.group(), fmt).date()
            final_date = res.strftime('%d-%m-%Y')
            return final_date
        except ValueError:
            pass
    return False


text = extract_date("31-05-23")
print(text)