import appdaemon.plugins.hass.hassapi as hass
import uuid
from switchbot import SwitchBot

class SwitchBotLockManager(hass.Hass):

  def initialize(self):
    self.log('----------------------initialize')
    self.log("Switchbot initialized in AppDaemon...")
    
    self.boolean_lock_deviceid = self.args["boolean_lock_deviceid"]
    self.log("boolean_lock_deviceid= " + self.boolean_lock_deviceid)

    self.status_update_interval_minutes = self.args["status_update_interval_minutes"]
    self.log("status_update_interval_minutes= " + str(self.status_update_interval_minutes))

    self.status_update_interval_seconds = self.status_update_interval_minutes * 60
    self.log("status_update_interval_seconds= " + str(self.status_update_interval_seconds))

    self.push_notifiy_intity = self.args["push_notifiy_intity"]
    self.log("push_notifiy_intity= " + str(self.push_notifiy_intity))
    
    self.lock_name = self.boolean_lock_deviceid
    self.lock_name = self.lock_name.split('.')[1]
    self.log("lock_name= " + self.lock_name)

    #self.switchbot = SwitchBot(token=self.args["api_token"], secret=self.args["api_secret"], nonce=str(uuid.uuid4()))
    #devices = self.switchbot.devices()
    #for device in devices:
    #  print(device)

    self.listen_state(self.state_change, self.boolean_lock_deviceid)
    self.run_every(self.pull_status_update, "now", self.status_update_interval_seconds)
  
  def state_change(self, entity, attribute, old, new, kwargs):
    self.log('----------------------state_change')
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
      self.call_service(self.push_notifiy_intity, message="Lock ["+self.lock_name+"] Locked")
    elif new == "off" and lockstatus["lock_state"] == "locked":
      self.log("Attempting to UnLock...")
      self.lock.unlock()
      self.turn_off(self.boolean_lock_deviceid )
      self.log("...Done Unlocking")
      self.call_service(self.push_notifiy_intity, message="Lock ["+self.lock_name+"] UnLocked")
    else:
      self.log("Nothing Done...")
      self.call_service(self.push_notifiy_intity, message="Nothing done, Lock ["+self.lock_name+"] is already: "+lockstatus["lock_state"] )

  def pull_status_update(self, kwargs):
    self.log('----------------------pull_status_update')
    self.log("Executing periodic update....")
    self.switchbot = SwitchBot(token=self.args["api_token"], secret=self.args["api_secret"], nonce=str(uuid.uuid4()))
    self.lock = self.switchbot.device(id=self.args["smartlock_deviceid"])
    lockstatus = self.lock.status()
    self.log("lock_state= " + lockstatus["lock_state"])
    self.log("door_state= " + lockstatus["door_state"])
    self.log("calibrate= " + str(lockstatus["calibrate"]))

    boolean_lock_device_state = self.get_state(self.boolean_lock_deviceid)
    self.log("boolean_lock_device_state= " + boolean_lock_device_state)

    if lockstatus["lock_state"] == "unlocking" or lockstatus["lock_state"] == "locking":
      self.log("Nothing to update. lock_state: " +lockstatus["lock_state"])
    elif lockstatus["lock_state"] == "locked" and boolean_lock_device_state == "off":
      self.turn_on(self.boolean_lock_deviceid)
      self.log("status updated to: " +lockstatus["lock_state"])
    elif lockstatus["lock_state"] == "unlocked" and boolean_lock_device_state == "on":
      self.turn_off(self.boolean_lock_deviceid)
      self.log("status updated to: " +lockstatus["lock_state"])
    elif  lockstatus["lock_state"] == "locked" or lockstatus["lock_state"] == "unlocked":
      self.log("Nothing to update. lock_state: " +lockstatus["lock_state"])
    else:
      self.log("Periodic update, Unknown lock_state: "+lockstatus["lock_state"])
      self.call_service(self.push_notifiy_intity, message="Periodic update, Unknown lock_state: "+lockstatus["lock_state"])

