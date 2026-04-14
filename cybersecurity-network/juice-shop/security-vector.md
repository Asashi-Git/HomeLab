# JuiceShop security leak

## Dirb

Using Dirb I have found many page that must be hidden by the web server
theses file a listed bellow:

``` bash
dirb http://juiceshop-1.homelab.local:3000/ -z 50 -o dirb_output.txt

-----------------
DIRB v2.22    
By The Dark Raver
-----------------

OUTPUT_FILE: dirb_output.txt
START_TIME: Tue Apr 14 00:24:52 2026
URL_BASE: http://juiceshop-1.homelab.local:3000/
WORDLIST_FILES: /usr/share/dirb/wordlists/common.txt
SPEED_DELAY: 50 miliseconds

-----------------

GENERATED WORDS: 4612                                                          

---- Scanning URL: http://juiceshop-1.homelab.local:3000/ ----
+ http://juiceshop-1.homelab.local:3000/assets (CODE:301|SIZE:156)                                       
+ http://juiceshop-1.homelab.local:3000/ftp (CODE:200|SIZE:11308)                                        
+ http://juiceshop-1.homelab.local:3000/media (CODE:301|SIZE:155)                                        
+ http://juiceshop-1.homelab.local:3000/profile (CODE:500|SIZE:1055)                                     
+ http://juiceshop-1.homelab.local:3000/promotion (CODE:200|SIZE:6459)                                   
+ http://juiceshop-1.homelab.local:3000/redirect (CODE:500|SIZE:3207)                                    
+ http://juiceshop-1.homelab.local:3000/robots.txt (CODE:200|SIZE:28)                                    
+ http://juiceshop-1.homelab.local:3000/video (CODE:200|SIZE:10075518)                                   
+ http://juiceshop-1.homelab.local:3000/Video (CODE:200|SIZE:10075518)                                   
                                                                                                         
-----------------
END_TIME: Tue Apr 14 00:29:47 2026
DOWNLOADED: 4612 - FOUND: 9
```

By adding a WAF inside the web server
we can easily correct this kind of cybersecurity basic mistake.


```bash
http://juiceshop-1.homelab.local:3000/#/score-board
```


