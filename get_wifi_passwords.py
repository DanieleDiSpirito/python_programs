import subprocess
import re

command_output = subprocess.run(['netsh', 'wlan', 'show', 'profiles'], capture_output = True).stdout.decode()
print(command_output)
profile_names = (re.findall("Tutti i profili utente    : (.*)\r", command_output))

wifi_list = list()

if len(profile_names) != 0:
    for name in profile_names:
        wifi_profile = dict()
        profile_info = str(subprocess.run(['netsh', 'wlan', 'show', 'profiles', f'name={name}'], capture_output = True).stdout)
        #print(profile_info)
        if re.search("Chiave di sicurezza      : Presente", profile_info):
            wifi_profile['ssid'] = name
            profile_info_pass = str(subprocess.run(['netsh', 'wlan', 'show', 'profile', name, 'key=clear'], capture_output = True).stdout)
            #print(profile_info_pass)
            password = re.search("Contenuto chiave( )+:(.*)I", profile_info_pass)
            if password == None:
                wifi_profile['password'] = None
            else:
                #print(str(password).split('\\'))
                wifi_profile['password'] = str(password).split('\\')[0].split(':')[-1].strip()
            wifi_list.append(wifi_profile)
                                               
for wifi in wifi_list:
    print('------------------')
    print('SSID:', wifi['ssid'])
    print('Password:', wifi['password'])
    
input()
