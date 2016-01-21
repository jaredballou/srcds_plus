#!/usr/bin/python
import os
import subprocess
import tarfile
import zipfile


def binary_prompt(prompt=None):
  if not prompt:
    prompt = "Do you want to proceed?"
  response = None
  responses = {"y": True, "n": False}
  while response not in responses:
    response = raw_input("%s [y/n]: " % prompt).strip().lower()
  return responses[response]


def extract_file(compressed_file, target_path):
  """
  extract_file(compressed_file, target_path)

  extracts the compressed_file to target_path
  """

  if os.path.exists(compressed_file):
    print "Extracting %s to %s\n" % (compressed_file, target_path)

    if zipfile.is_zipfile(compressed_file):
      with zipfile.ZipFile(compressed_file, "r") as z:
          z.extractall(path=target_path)

    if tarfile.is_tarfile(compressed_file):
      tar = tarfile.open(compressed_file)
      tar.extractall(path=target_path)
      tar.close()

    print "Cleaning up\n"
    os.remove(compressed_file)

    print "Done!\n"
  else:
    print "%s does not exist, cannot extract" % compressed_file


def get_existing_path(game_path=None):
  """
  get_existing_path()

  prompts the user for the path to their steam server
  """

  while not game_path:
    game_path = raw_input(
      'Where is your server going to be? (eg. /home/steamuser/csgo_server): '
    ).strip()

    # Make sure this is a the correct folder
    if not os.path.exists("%s/cfg" % game_path):
      print "\nThat directory does not look like a source dedicated server, "\
        "are you sure this is correct?\nIt should be the same folder that has "\
        "maps and cfgs\n"

      game_path = None

  return game_path


def get_url(plugin):
  """
  get_url(plugin)

  returns the download url for the specified plugin
  """
  sm_version = subprocess.check_output(
    'curl http://www.sourcemod.net/smdrop/1.7/sourcemod-latest-linux',
    shell=True,
  )

  download_url = {
    'metamod': 'http://www.metamodsource.net/mmsdrop/1.10/mmsource-1.10.7-git948-linux.tar.gz',
    'sourcemod': "http://www.sourcemod.net/smdrop/1.7/%s" % sm_version,
  }

  return download_url[plugin]


def install_dedicated_server(steam_path=None):
  """
  install_dedicated_server(steam_path=None)

  Executes the steamcmd script and begins downloading a dedicated server
  """

  server_names = [
      "1. Counter-Strike Global Offensive",
      "2. Counter-Strike Source ",
      "3. Day of Defeat Source",
      "4. Garrys Mod",
      "5. Insurgency",
      "6. Left 4 Dead 2",
      "7. Left 4 Dead",
      "8. Team Fortress 2",
    ]

  app_ids = {
      '1': 740,
      '2': 232330,
      '3': 232290,
      '4': 4020,
      '5': 237410,
      '6': 222860,
      '7': 22284,
      '8': 232250,
    }

  choice = None
  while not choice:
    print "\nSupported Dedicated Servers"
    for server_name in server_names:
      print server_name
    choice = int(
      raw_input("\nWhich dedicated server would you like to install?: ")
    )
    choice -= 1

    if binary_prompt(
      "You chose %s, is that correct?" % server_names[choice][3:]
    ):
      server_path = "%s dedicated-server" % server_names[choice][3:]
      subprocess.call(
        "%s/steamcmd.sh +login anonymous +force_install_dir \"%s/%s\" +app_update %s +quit" % (
          steam_path,
          steam_path,
          server_path,
          app_ids.values()[choice]
        ),
        shell=True)

      if os.path.exists("%s/srcds_run" % server_path):
        if binary_prompt(
          "\nInstallation Sucessful! Would you like to install sourcemod and metamod?"
        ):
          download_plugins(game_path=server_path)
        print "Enjoy!"
        return
    else:
      choice = None


def install_steamcmd():
  """
  install_steamcmd()

  Grabs the correct build of steamcmd for the paltform and unzips it
  """

  if binary_prompt('Would you like to install SteamCMD?'):
    steamcmd_path = None
    while not steamcmd_path:
      steamcmd_path = raw_input(
        'Where shall I install steamcmd? (eg. /home/steamuser/csgo_server): '
      ).strip()

    steamcmd_tar = 'https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz'

    downloaded_tar = "%s/steamcmd.tar.gz" % steamcmd_path

    print "Downloading steamcmd from %s. Saving to %s\n" % (steamcmd_tar, downloaded_tar)

    subprocess.call(
      "wget --quiet -O %s %s" % (downloaded_tar, steamcmd_tar),
      shell=True
    )

    extract_file(compressed_file=downloaded_tar, target_path=steamcmd_path)

    print "SteamCMD installed! You can find it at %s/steamcmd.sh\n" % steamcmd_path

  if binary_prompt('Would you like to install a game server now?'):
    install_dedicated_server(steam_path=steamcmd_path)

  return


def download_plugins(game_path):
  """
  download_plugins()

  wgets the plugins
  """
  for plugin_name in ['metamod', 'sourcemod']:
    url = get_url(plugin=plugin_name)
    downloaded_plugin = "%s/%s" % (game_path, plugin_name)

    print "\nDownloading %s from %s\n" % (plugin_name, url)
    subprocess.call(
      "wget --quiet -O %s %s" % (downloaded_plugin, url), shell=True
    )

    # Extract the files
    extract_file(compressed_file=downloaded_plugin, target_path=game_path)

if __name__ == '__main__':
  install_steamcmd()
