"""this is to fingerprint the subdomain and get vluable info"""

import os
import threading


print('Hi')
class fingerprinting:
    
    def __init__(self,target):
        self.target = target


    """To gather intell in a different folder"""

    def __storing__(self):
        try :
            os.makedirs("Fingerprint")
        except Exception as e:
            print(f"unable to create Folder: {e}")
        finally:
            os.chdir(path='Fingerprint')

    """General stack fingerprinting """

    def whatweb(self):
        print('[*]Running what web')
        cmd = f"whatweb -a 3 {self.target} --log-json=whatweb.txt"

        os.system(cmd)
        print("[+]What web scan done")

    """using HTTPX"""

    def httpx(self):
        print("[*]Running HTTPX scan")
        cmd = f"httpx -u {self.target} -title -server -tech-detect -status-code -o httpx.txt"
        
        os.system(cmd)
        print("[+]httpx scan complete")

    
    """service/version detection"""
    def nmap(self):
        print('[*]Running Nmap')
        cmd = f'nmap -sC -sV {self.target} -oN nmap.txt'

        os.system(cmd)
        print("[+]Nmap scan Done")

    
    """Waf detection"""
    def wafwoof(self):
        print('[*]Scanning the Firewall')
        cmd = f'wafw00f {self.target} -o firewall.txt'

        os.system(cmd)
        print('[+]Firewall scan Done')
    
    
    """Raw headers"""

    def curl(self):
        print("[+]Getting Raw headers")
        cmd = f"curl -I {self.target} -o headers.txt"

        print('[+]header collected and stored to headers.txt')

    
    """Using Wappalyzer"""

    def Wappalyzer(self):
        print('[*]Using wappalyzer CLI')
        cmd = f'wappalyzer --target {self.target} --disable-ssl --output wappalyzer.txt --json '
        os.system(cmd)

        print("[+]Wappalyzer scan Done")

    
    def run_all(self):

        self.__storing__()
        print("[+]Directory Created and Changed")

        methods = [self.curl,self.httpx,self.nmap,self.wafwoof,self.Wappalyzer,self.whatweb]
        threads = [threading.Thread(target=m) for m in methods]

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        print('[+] Fingerprinting Done :)')


