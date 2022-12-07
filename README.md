# SwitchBotLockManager
AppDaemon app to integrate SwitchBot Smart Lock into Home Assistant

 1. Installl AppDaemon Addon on Home assistant
 2. Create a long-lived Access Token on HA, then add it in the **secrets.yaml** as: ***appdaemon_token***
 3. to Get the ***switchbot_api_token*** and ***switchbot_api_secret*** follow the instructions in: https://github.com/OpenWonderLabs/SwitchBotAPI#getting-started
 4. Modify the **/CONFIG/secret.yaml** 
 5. Modify the **/CONFIG/appdaemon/appdaemon.yaml**
 6. install the python-switchbot library : 
 Go to Settings --> Addons--> AppDaemon --> Configurations
in Options right top corner (...) select (Edit in YAML):
      init_commands: []
      python_packages:
      - python-switchbot
      system_packages: []
      log_level: info
 7. Add the HA entities into **/CONFIG/configuration.yaml**
 8. modify **/CONFIG/appdaemon/apps/apps.yaml**
 9. create **/CONFIG/appdaemon/apps/switchbotlockmanager.py**
 10. to get the ***switchbot_smartlock_deviceId***, uncomment the lines below in **switchbotlockmanager.py**, and the logs will show all your devises with devecieid for each.

    #devices = self.switchbot.devices()   
    #for device in devices:   
    #print(device)

