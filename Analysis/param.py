"""For obtainnig different paramter endoint to 
check for IODR's and Fuzzinf"""
import os
import threading



class para_finder:

    def __init__(self,filename,sitename):
        self.file = filename
        self.site = sitename
    
    #filtering endpoints having "="

    def filter(self):
        print("[*] Filtering Js files")
        cmd = f"grep '=' {self.file} | anew param.txt"
        os.system(cmd)


    #running arjun scanner 

    def arjun(self):
        print("[+]Running Arjun scan")

        cmd = f'arjun -u {self.site} | anew param.txt'
        os.system(cmd)


    
    def run_js(self):
        print('[*] Starting para finder')

        
        methods = [self.arjun,self.filter]  # add more here later
        threads = [threading.Thread(target=m) for m in methods]

        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        print('[+] Parameter are now stored to param.txt')

if __name__ == "__main__":

    run = para_finder('_LiveUrls_.txt','https://abc.com')
    run.run_js()

