# README #

This abomination of python was created because I used to host steam dedicated servers, took a break, and when I wanted to host one again, I had forgotten how to get everything set up.

This will take care of installing SteamCMD, installing a dedicated server, and installing sourcemod + metamod (you still have to install plugins)

My Goal with this was to avoid using any third party python libraries in order to
speed up the 0 to play pipeline if you are running this on a fresh linux install

#### Dependencies ####
* Wget and python. Thats it baby

#### Usage ####
List of supported games:
* 1. Counter-Strike Global Offensive
* 2. Counter-Strike Source
* 3. Day of Defeat Source
* 4. Garrys Mod
* 5. Insurgency
* 6. Left 4 Dead 2
* 7. Left 4 Dead
* 8. Team Fortress 2

To install Insurgency for example:
```python srcds_plus.py --path /home/steamuser/games --game 5 --sourcemod```

### Things I'd like to add ###

* Add more options to the dedicated server list, right now its just a few popular games
* ~~Pass commands to the script~~
* Handle the case where steamcmd is already installed (perhaps write to a config file ```~/.srcds_plus_configs)```
* ~~Scrape the metamod/sourcemod webapges for the latest version numbers instead of hardcoding the URLs~~
* ~~Something to assist with installing steamcmd or maybe even a source dedicated server~~
* Windows support (probably not though)

### Who do I talk to? ###

* Repo owner or admin
* I'm usually always available on [Steam](http://steamcommunity.com/profiles/76561198002556086)