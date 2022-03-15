import colorama
import requests 
import vlc
import time
yamete = vlc.MediaPlayer("usm.mp3")
colorama.init(autoreset=True)

def ProxiesGrabbering(type,timeout):
 try: 
   r =  requests.get(f"https://api.proxyscrape.com/v2/?request=getproxies&protocol={type}&timeout={timeout}&country=all&ssl=all&anonymity=all")
   proxies = r.text.split("\n")
   with open("Proxies.txt", 'w') as file:
       file.write("".join(proxies))
       print(colorama.Fore.GREEN + f"Done i have Saved {len(proxies)} of {type} proxy\nYou Can Exit By Enter Any Press")
       yamete.play()
       time.sleep(3.5)
       yamete.stop()
       input("> ")
 except Exception as Errors:
    print(Errors)
    print(colorama.Fore.RED + "There are some problems with Proxyscrape, please try again later") 
if __name__ == '__main__': 
    print(colorama.Fore.RED + """
    
    
       ,/%%%%(,                           *#%%%%*.                  
             (##################%              .%##################*            
          %#########################        *#########################(         
        ##############################,   %#############################(       
      /#################################/#################################      
     *#####################################################################     
     ######################################################################%    
    .######################################################################%    
    .######################################################################%    
     ######################################################################%    
     %#####################################################################,    
      #####################################################################     
      /###################################################################      
       *#################################################################       
         ##############################################################(        
           ###########################################################          
             ######################################################(            
               /#################################################.              
                  ############################################/                 
                    .######################################%                    
                       .#################################                       
                          ,###########################                          
                             /#####################.                            
                                ################.                               
                                   %#########/                                  
                                      #####  
    Github: 9de
    Discord: Paula#0001
    Instagram: ljzb
    Twitter: DVHS
    """) 
    try:
        print("Proxyscrape Grabbering Proxies")
        print(colorama.Fore.YELLOW + "[1] http, [2] Socks4, [3] Socks5: ")
        proxiestype = int(input(": "))
        print(colorama.Fore.BLUE + "Please write the timeout Time: ")
        timeout = int(input(": "))
        if proxiestype == 1:
            ProxiesGrabbering("http", timeout)
        elif proxiestype == 2:
             ProxiesGrabbering("socks4", timeout)
        elif proxiestype == 3:
          ProxiesGrabbering("socks4", timeout)
        else:
            input("Can't Find Number Try Again!\n")
                 
    except ValueError:
            input("> Please Type Number Not String\n")