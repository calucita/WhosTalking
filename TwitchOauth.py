import AppInfo

#  Copyright (c) 2020. Lena "Teekeks" During <info@teawork.de>
import urllib.parse
import uuid
from typing import Union
from json import JSONDecodeError
from aiohttp.web import Request
import webbrowser
from aiohttp import web
import asyncio
from threading import Thread
from time import sleep
from os import path
import requests
from concurrent.futures._base import CancelledError
from logging import getLogger, Logger

class TwitchOauth:

    port: int = 17563
    host: str = '0.0.0.0'
    __state: str = ''

    __server_running: bool = False
    __loop: Union['asyncio.AbstractEventLoop', None] = None
    __runner: Union['web.AppRunner', None] = None
    __thread: Union['threading.Thread', None] = None

    __user_token: Union[str, None] = None

    __can_close: bool = False

    def __build_runner(self):
        app = web.Application()
        app.add_routes([web.get('/', self.__handle_callbackGet)])
        app.add_routes([web.post('/', self.__handle_callbackPost)])
        return web.AppRunner(app)

    async def __run_check(self):
        while not self.__can_close:
            try:
                await asyncio.sleep(1)
            except (CancelledError, asyncio.CancelledError):
                pass
        for task in asyncio.Task.all_tasks(self.__loop):
            task.cancel()

    def __run(self, runner: 'web.AppRunner'):
        self.__runner = runner
        self.__loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.__loop)
        self.__loop.run_until_complete(runner.setup())
        site = web.TCPSite(runner, self.host, self.port)
        self.__loop.run_until_complete(site.start())
        self.__server_running = True
        try:
            self.__loop.run_until_complete(self.__run_check())
        except (CancelledError, asyncio.CancelledError):
            pass

    def __start(self):
        self.__thread = Thread(target=self.__run, args=(self.__build_runner(),))
        self.__thread.start()

    def stop(self):
        """Manually stop the flow
        :rtype: None
        """
        self.__can_close = True


    async def __handle_callbackGet(self, request: 'web.Request'):
        # Assume that everything is fine and verify in the post.
        fn = path.join(path.dirname(__file__), 'Success.html')
        fd = ''
        with open(fn, 'r') as f:
            fd = f.read()

        return web.Response(text=fd, content_type='text/html')


    async def __handle_callbackPost(self, request: 'web.Request'):
        val = str(request.content._buffer)
        val = val.split("#")[1].split("\\r\\n")[0].split("&")
        
        # invalid state!
        if val[2].split("=")[1] != self.__state:
            return web.Response(status=401)
        
        self.__user_token = val[0].split("=")[1]
        if self.__user_token is None:
            # must provide code
            return web.Response(status=400)

        fn = path.join(path.dirname(__file__), 'Success.html')
        fd = ''
        with open(fn, 'r') as f:
            fd = f.read()

        return web.Response(text=fd, content_type='text/html')

    def authenticate(self):
        self.__start()
        # wait for the server to start up
        while not self.__server_running:
            sleep(0.01)

        self.__state = str(uuid.uuid4())
        url = ("https://id.twitch.tv/oauth2/authorize?"
                + "response_type=token"
                + "&client_id=" + AppInfo.ClientId
                + "&redirect_uri=" + AppInfo.RedirectUri
                + "&scope=chat:read chat:edit"
                + "&force_verify=true"
                + "&state="+self.__state)
        # open in browser

        webbrowser.open(url, new=2)
        while self.__user_token is None:
            sleep(0.01)

        self.stop()
        self.__state = ''
        return self.__user_token


