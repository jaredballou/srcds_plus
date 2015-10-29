#!/usr/bin/python
# This script will download and install both metamod and sourcemod
import os
import platform
import subprocess
import tarfile
import zipfile


def get_path():
  """
  get_path()

  prompts the user for the path to their steam server
  """
  game_path = None
  while not game_path:
    game_path = raw_input(
      'Where is your game installed? (eg. /home/steamuser/csgo_server): '
    ).strip()

    # Make sure this is a the correct folder
    if not os.path.exists("%s/cfg" % game_path):
      print "\nThat directory does not look like a source dedicated server, "\
        "are you sure this is correct?\nIt should be the same folder that has "\
        "maps and cfgs\n"

      game_path = None

  return game_path


def get_platform():
  """
  get_platform()

  Tells the script which build of the plugins to get, mac or linux
  """
  for platform_name, friendly_name in {
    'Darwin': 'mac',
    'Linux': 'linux',
  }.items():
    if platform_name in platform.platform():
      return friendly_name


def get_url(plugin, extension):

  download_url = {
    'metamod': "http://www.metamodsource.net/mmsdrop/1.10/mmsource-1.10.7-git948-%s.%s" % (get_platform(), extension),
    'sourcemod': "https://www.sourcemod.net/smdrop/1.7/sourcemod-1.7.3-git5272-%s.%s" % (get_platform(), extension),
  }

  return download_url[plugin]


def install_plugins(game_path):
  """
  install_plugins()

  wgets the plugins
  """
  platform = get_platform()
  file_extension = 'zip' if 'mac' in platform else 'tar.gz'

  for plugin_name in ['metamod', 'sourcemod']:
    url = get_url(plugin=plugin_name, extension=file_extension)
    downloaded_plugin = "%s/%s.%s" % (game_path, plugin_name, file_extension)

    print "Downloading %s from %s\n" % (plugin_name, url)
    subprocess.call(
      "wget --quiet -O %s %s" % (downloaded_plugin, url), shell=True
    )

    if os.path.exists(downloaded_plugin):
      print "Extracting %s to %s\n" % (plugin_name, game_path)
      # Use unzip for mac
      if get_platform() == 'mac':
        with zipfile.ZipFile(downloaded_plugin, "r") as z:
            z.extractall(path=game_path)
      else:
        # Assume the user is a superior linux user
        tar = tarfile.open(downloaded_plugin)
        tar.extractall(path=game_path)
        tar.close()

      print "Cleaning up\n"
      os.remove(downloaded_plugin)

      print "Done!\n"


if __name__ == '__main__':
  game_path = get_path()
  install_plugins(game_path)
