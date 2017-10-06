import socket


class InternetKommunikation:
    """
        Hanterar kommunikation med internet
    """
    
    def isAnslutenTillInternet(self, host="8.8.8.8", port=53, timeout=3):
        """Undersök om man är ansluten till internet"""
        
        try:
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
            return True
        except Exception as ex:
            #errno, strerror = ex.args
            print(ex.args)
            return False


if __name__ == '__main__':
    i = InternetKommunikation();
    if i.isAnslutenTillInternet():
        print("Ansluten till internet")
    else:
        print("Inte ansluten till internet")
