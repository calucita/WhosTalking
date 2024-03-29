"""Oauth retriever"""
# Based on the work of Lena "Teekeks" <info@teawork.de>

import uuid
from typing import Union
import webbrowser
import asyncio
from threading import Thread
from time import sleep
from os import path
from aiohttp import web

import AppInfo


class TwitchOauth:
    """Twitch oauth retriever based on the work of Lena "Teekeks" <info@teawork.de>"""

    port: int = 17563
    host: str = "0.0.0.0"
    __state: str = ""

    __server_running: bool = False
    __loop: Union["asyncio.AbstractEventLoop", None] = None
    __thread: Union[Thread, None] = None

    __user_token: Union[str, None] = None

    __can_close: bool = False

    def __build_runner(self):
        app = web.Application()
        app.add_routes([web.get("/", self.__handle_callback_get)])
        app.add_routes([web.post("/", self.__handle_callback_post)])
        return web.AppRunner(app)

    async def __run_check(self):
        while not self.__can_close:
            try:
                await asyncio.sleep(1)
            except:
                self.__server_running = False

        for task in asyncio.all_tasks(self.__loop):
            task.cancel()
            self.__server_running = False

    def __run(self, runner: "web.AppRunner"):
        try:
            self.__loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.__loop)
            self.__loop.run_until_complete(runner.setup())
            site = web.TCPSite(runner, self.host, self.port)
            self.__loop.run_until_complete(site.start())
            self.__server_running = True
            self.__loop.run_until_complete(self.__run_check())
        except:
            self.__server_running = False

    def __start(self):
        self.__thread = Thread(target=self.__run, args=(self.__build_runner(),))
        self.__thread.start()

    def stop(self):
        """Manually stop the flow
        :rtype: None
        """
        self.__can_close = True
        self.__server_running = False

    async def __handle_callback_get(self, request: "web.Request"):
        fn = path.join(path.dirname(__file__), "Failed.html")
        val = str(request.message)
        if not str.__contains__(val, "access_denied"):
            # Assume that everything else is fine and verify in the post.
            fn = path.join(path.dirname(__file__), "Success.html")
        fd = ""
        with open(fn, "r") as f:
            fd = f.read()

        return web.Response(text=fd, content_type="text/html")

    async def __handle_callback_post(self, request: "web.Request"):
        val = str(request.content._buffer)
        fn = path.join(path.dirname(__file__), "Failed.html")
        if not str.__contains__(val, "access_denied"):
            val = val.split("#")[1].split("\\r\\n")[0].split("&")

            # invalid state!
            if val[2].split("=")[1] != self.__state:
                self.__server_running = False
                return web.Response(status=401)

            self.__user_token = val[0].split("=")[1]
            if self.__user_token is None:
                # must provide code
                self.__server_running = False
                return web.Response(status=400)

            fn = path.join(path.dirname(__file__), "Success.html")
        else:
            self.__user_token = "  "

        fd = ""
        with open(fn, "r") as f:
            fd = f.read()

        return web.Response(text=fd, content_type="text/html")

    def authenticate(self):
        """Starts the process to get a token"""
        self.__start()
        # wait for the server to start up
        while not self.__server_running:
            sleep(0.01)

        self.__state = str(uuid.uuid4())
        url = (
            "https://id.twitch.tv/oauth2/authorize?"
            + "response_type=token"
            + "&client_id="
            + AppInfo.CLIENTID
            + "&redirect_uri="
            + AppInfo.REDIRECTURI
            + "&scope=chat:read chat:edit"
            + "&force_verify=true"
            + "&state="
            + self.__state
        )
        # open in browser

        webbrowser.open(url, new=2)
        while self.__user_token is None and self.__server_running:
            sleep(0.1)
        self.stop()
        self.__state = ""
        return self.__user_token
