
# SwitchBotLockManager
AppDaemon app to integrate SwitchBot Smart Lock into Home Assistant. For this to work, you need to enable Cloud Services for the lock after connecting a SwitchBot Hub-mini in your network.

 1. Installl AppDaemon Addon on Home assistant
 2. Create a long-lived Access Token on HA, then add it in the **secrets.yaml** as: ***appdaemon_token***
 3. to Get the ***switchbot_api_token*** and ***switchbot_api_secret***, follow the instructions in: https://github.com/OpenWonderLabs/SwitchBotAPI#getting-started
 4. Modify the **/CONFIG/secret.yaml** by adding the conetnts from this repo.
 5. Modify the **/CONFIG/appdaemon/appdaemon.yaml** by using the conetnts from this repo.
 6. install the python-switchbot library : 
    - *Go to Settings --> Addons--> AppDaemon --> Configurations*
     - *In Options right top corner (...) select (Edit in YAML):*
```
    init_commands: []
    python_packages:
      - python-switchbot
    system_packages: []
    log_level: info
```

 7. Add the HA entities into **/CONFIG/configuration.yaml** by adding the conetnts from this repo.
 8. modify **/CONFIG/appdaemon/apps/apps.yaml** by adding the conetnts from this repo.
 9. create **/CONFIG/appdaemon/apps/switchbotlockmanager.py** by using the conetnts from this repo.
 10. to get the ***switchbot_smartlock_deviceId***, uncomment the lines below in **switchbotlockmanager.py**, and the AppDaemon add-on logs will show all your devises with devecieid for each.

 **Lines to uncomment:**
```
    #devices = self.switchbot.devices()   
    #for device in devices:   
    #print(device)
```


**Sample logs :**
```
    2022-12-07 11:53:30.445887 INFO AppDaemon: Reloading Module: /config/appdaemon/apps/switchbotlockmanager.py
    2022-12-07 11:53:30.453879 INFO AppDaemon: Initializing app switchbot using class SwitchBotLockManager from module switchbotlockmanager
    HubMini(id=XXXXXXXXXX)
    SmartLock(id=YYYYYYYYYY)
```
