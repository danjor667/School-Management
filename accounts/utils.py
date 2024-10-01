from email.headerregistry import Address

def get_username_from_email(email: str) -> str:
    """Get username from a given email address
    
    Args:
        email (str): Email address
    
    Returns:
        str: Username in alpha numeric format
    """
    return "".join(filter(str.isalnum, Address(addr_spec=email).username))
