""" This is used to get all the urls from the subdomain and make the 
process fast  , The Urls will then be further divided into specific endpoints 
in order to run analysis on them """

import subprocess 
import os
import concurrent.futures
from pathlib import Path
import threading

class GetAllUrls:

    def __init__(self,target):
        self.target = target

    #for creating folder if required
    def __make__folder(self):
        os.makedir(folder)

    
    #for creating files for the tools and store there output indivisually   
    def __make__file(self,tool):
        Path(f"{tool}.txt")

    #for runnning gau

    def run_gau(self):
        self.__make__file('_gau_')
        print(f'[+] File created _gau_.txt')
        

        cmd = (
            f"gau --threads 5 "
            f"--providers wayback,commoncrawl,otx,urlscan "
            f"--blacklist png,jpg,gif,svg,css,woff,ttf "
            f"{self.target} > _gau_.txt"
        )
        os.system(cmd)
        print(f'[+] GAU Scan done')
        print(f'[+] File saved to _gau_.txt')
        
        count = os.popen('wc -l < _gau_.txt').read().strip()
        print(f'[+] Gau found: {count}')

# for running katana
    def run_katana(self):
        self.__make__file('_katana_')
        print(f'[+] File created _katana_.txt')
        

        cmd = f'katana -u https://{self.target} -d 3 > _katana_.txt'

        os.system(cmd)
        print(f'[+] Katana Scan done')
        print(f'[+] File saved to _katana_.txt')
        
        count = os.popen('wc -l < _katana_.txt').read().strip()
        print(f'[+] Katana found: {count}')
#for spider
    def run_gospider(self):
        self.__make__file("_gospider_")
        print('[+]File created _gospider_.txt')


        cmd = (
            f'gospider -s "https://{self.target}" '
            f'-c 10 -d 5 --other-source --include-subs --include-other-source '
            f'--sitemap --robots -w -r -t 20 --js -a '
            f'-H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)" '
            f'--timeout 15 -q | anew _gospider_.txt'
        )
        os.system(cmd)

        count = os.popen('wc -l < _gospider_.txt').read().strip()
        print(f'[+] Gospider found {count} endpoints')
#Removing duplicates -> then checking for their live 
    def rm_junk(self): #removing duplicates
        self.__make__file('_LiveUrls_')
        print('[+]Removing duplicates and checking for liveness')
        
        cmd = 'cat _gau_.txt _katana_.txt _gospider_.txt | sort -u | httpx -mc 200,301,302,403 -silent  > _LiveUrls_.txt' #opening all the files
        print(f'[+]Process complete')
        print(f'[+]File saved to _LiveUrls_.txt')

        os.system(cmd)

        count = os.popen('wc -l < _LiveUrls_.txt').read().strip()
        print(f'[+]Current URls : {count}')

#Now running all with threads 

    def run_all(self):
        methods = [self.run_gau, self.run_katana,self.run_gau]  # add more here later
        threads = [threading.Thread(target=m) for m in methods]

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        print('[+] ALL scans are now completed')
        self.rm_junk()




tool = GetAllUrls('abc.com')
tool.run_all()