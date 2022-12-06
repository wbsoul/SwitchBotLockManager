import appdaemon.plugins.hass.hassapi as hass
import uuid
from switchbot import SwitchBot

class SwitchBotLockManager(hass.Hass):

  def initialize(self):
    self.log("Switchbot initialized in AppDaemon...")
    
    self.boolean_lock_deviceid = self.args["boolean_lock_deviceid"]
    #self.boolean_lock_deviceid = 'input_boolean.lock_1'
    self.log("boolean_lock_deviceid= " + self.boolean_lock_deviceid)
    
    self.switchbot = SwitchBot(token=self.args["api_token"], secret=self.args["api_secret"], nonce=str(uuid.uuid4()))
    #devices = self.switchbot.devices()
    #for device in devices:
    #  print(device)
    self.lock = self.switchbot.device(id=self.args["smartlock_deviceid"])
    lockstatus = self.lock.status()
    self.log("lock_state= " + lockstatus["lock_state"])
    self.log("door_state= " + lockstatus["door_state"])
    self.log("calibrate= " + str(lockstatus["calibrate"]))

    if lockstatus["lock_state"] == "locked":
      self.turn_on(self.boolean_lock_deviceid)
    else:
      if lockstatus["lock_state"] == "unlocked":
        self.turn_off(self.boolean_lock_deviceid)
      else:
        self.log("Unknown lock_state: " +lockstatus["lock_state"])
        self.call_service("notify/mobile_app_lya_l29", message="Initializing, Unknown lock_state: "+lockstatus["lock_state"])
    
    self.listen_state(self.state_change, self.boolean_lock_deviceid)
  
  def state_change(self, entity, attribute, old, new, kwargs):
    self.log('old= ' + old)
    self.log('new= ' + new)

    self.switchbot = SwitchBot(token=self.args["api_token"], secret=self.args["api_secret"], nonce=str(uuid.uuid4()))
    self.lock = self.switchbot.device(id=self.args["smartlock_deviceid"])
    lockstatus = self.lock.status()
    self.log("lock_state= " + lockstatus["lock_state"])
    self.log("door_state= " + lockstatus["door_state"])
    self.log("calibrate= " + str(lockstatus["calibrate"]))
    
    if new == "on" and lockstatus["lock_state"] == "unlocked":
      self.log("Attempting to Lock...")
      self.lock.lock()
      self.turn_on(self.boolean_lock_deviceid )
      self.log("...Done Locking")
      self.call_service("notify/mobile_app_lya_l29", message="Unit door Locked")
    else:
      if new == "off" and lockstatus["lock_state"] == "locked":
        self.log("Attempting to UnLock...")
        self.lock.unlock()
        self.turn_off(self.boolean_lock_deviceid )
        self.log("...Done Unlocking")
        self.call_service("notify/mobile_app_lya_l29", message="Unit door UnLocked")
      else:
        self.log("Nothing Done...")
        self.call_service("notify/mobile_app_lya_l29", message="Nothing done, Door is already: "+lockstatus["lock_state"])
