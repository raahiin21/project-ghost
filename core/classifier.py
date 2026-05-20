#will be used to classify the errors for the user 

def classify_error(line):
    line_lower = line.lower()

    if "zerodivisionerror" in line_lower:
        return "RUNTIME"
    
    elif "syntaxerror" in line_lower:
        return "SYNTAX"
    
    elif "nameerror" in line_lower or "attributeerror" in line_lower:
        return "LOGICAL"
    
    elif "importerror" in line_lower or "modulenotfounderror" in line_lower:
        return "ENVIRONMENT"
    
    elif "permissionerror" in line_lower or "filenotfounderror" in line_lower:
        return "CONFIG"
    
    elif "typeerror" in line_lower:
        return "RUNTIME"
    
    else:
        return "UNKNOWN"