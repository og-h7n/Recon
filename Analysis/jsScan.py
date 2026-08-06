"""Created for scanning api keys and leaked credentials
in Js files 
Files are obtained from the geturls.py and then 
filtered through grep"""

import os
import threading



class Js_scanner:

    def __init__(self,filename):
        self.file = filename

    def filter(self):
#Endpoint extraction from file
        print("[*] Filtering Js files")
        cmd = f"grep '\\.js' {self.file} | anew js_files.txt"
        os.system(cmd)


    #running mantra scanner 

    def mantra_scan(self):
        print("[+]Running Mantra scan")

        cmd = f'cat js_files.txt| mantra'
        os.system(cmd)

    #running jsecret scanner
    def jsecret_scan(self):
        print("[+]Running Jsecret")

        cmd = f'cat js_files.txt | jsecret'
        os.system(cmd)
    
    def run_js(self):
        print('[*] Starting js scanner')
        print('[*]Filtering for js files')
        self.filter()

        
        methods = [self.mantra_scan,self.jsecret_scan]  # add more here later
        threads = [threading.Thread(target=m) for m in methods]

        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        print('[+]js scan completed')



