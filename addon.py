import os,threading
import xbmc,xbmcgui,xbmcplugin,xbmcaddon

addon = xbmcaddon.Addon()
dimSetting = 60 * int('5' if addon.getSetting('dim_setting') == '' else addon.getSetting('dim_setting'))
img = xbmc.translatePath( os.path.join( addon.getAddonInfo('path'), 'rain.jpg' ) )
img_dim = xbmc.translatePath( os.path.join( addon.getAddonInfo('path'), 'rain-dim.jpg' ) )
url = ["http://rainymood.com/audio1110/" + str(i) + ".ogg" for i in range(1, 8)]
# short ogg file to test loop:
# url = "http://images.wikia.com/starwars/images/f/f5/A_little_short.ogg"

class MyPlayer(xbmc.Player):
  def __init__(self):
    self.noiseIndex = 0
    self.playNoise()

  def onPlayBackEnded(self):
    self.noiseIndex = 0 if self.noiseIndex >= 7 else self.noiseIndex + 1
    self.playNoise()

  def playNoise(self):
    self.play(url[self.noiseIndex])

class MyWindow(xbmcgui.WindowDialog):
  def __init__(self):
    self.dimTimer = threading.Timer(dimSetting, self.dimScreen)
    self.imgNormal = xbmcgui.ControlImage(1, 1, 1280, 720, img)
    self.imgDim = xbmcgui.ControlImage(1, 1, 1280, 720, img_dim)
    self.addControl(self.imgNormal)
    self.dimTimer.start()

  def dimScreen(self):
    self.removeControl(self.imgNormal)
    self.addControl(self.imgDim)

  def onAction(self, action):
    xbmc.log(str(action.getId()))
    # 10 = ACTION_PREVIOUS_MENU, 13 = ACTION_STOP, 93 = ACTION_NAV_BACK
    # see https://github.com/xbmc/xbmc/blob/master/xbmc/input/Key.h
    if action==10 or action==13 or action==92:
      xbmc.executebuiltin("PlayerControl(Stop)")
      self.close()

p = MyPlayer()
w = MyWindow()
w.doModal()
del w
