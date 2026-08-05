''' For finding hidden directories that may have been 
missed by other scanners which is not actively displayed 
in the website '''

import os
import threading


class dir_brtfrce:
    
    def __init__(self, target):
        self.target = target

    """using ferox buster """


    def ferox(self):
        print('[*]Running Ferox buster')


        cmd = f"feroxbuster -u {self.target} --rate-limit 5 -t 5 --random-agent -o ferox_results.txt"
        os.system(cmd)
        print('[+]Ferox Scan Done')


    
    """Using Dirsearch"""

    def dirsearch(self):
        print('[*]Running ferox buster')

        cmd = f"dirsearch -u {self.target} -i 403,401 --format plain -t 5 --delay=1 --random-agent -r -o Dirseach_results.txt"    
        os.system(cmd)
        print("[+]Dirsearch scan Done")


    def run_all(self):
        methods = [self.ferox,self.dirsearch]  # add more here later
        threads = [threading.Thread(target=m) for m in methods]

        for t in threads:
            t.start()

        for t in threads:
            t.join()

        print("Directory Bruteforce completed")



if __name__ == "__main__":
    obj = dir_brtfrce('abc.com')
    obj.run_all()
    


