# WhosTalking
Needs Python 3.9

Twitch bot to keep track of who is actually talking.

- Based on the work of https://github.com/BadNidalee/ChatBot
- Based on pyTwitchAPI https://github.com/Teekeks/pyTwitchAPI

# Download
If you just want to use the bot go to Releases (https://github.com/calucita/WhosTalking/releases) and download the executable that suits you best. 

# Usage
To get a list of the users talking. 
 
- Add the name of your bot and the name of the channel you want to connect to.
- Click on the connect button. It should open a twitch authentication site for you to authorize the app.

- Press start and the 1st message of every user in chat along with the username will be logged in a list.
- Press stop to stop reading and logging chat. 
- Press clear to empty the log list. 

Use responsibly. 

Let me know of bugs... I might be interested in fixing them... 

the code is fugly as heck. I know. shhhhhhh

# Info for devs
## Necessary libraries (pip install)
- keyring
- keyrings.alt
- aiohttp
- requests

## Others
You will need to create an AppInfo.py file with the Url and Client Ids as registered in your twitch developers page. 
