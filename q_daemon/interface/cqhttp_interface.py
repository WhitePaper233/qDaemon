# -*- coding:utf-8 -*-

import logging
import threading

import websocket
import func_timeout

from q_daemon.utils import parser_loader
from q_daemon.utils import plugin_loader


class GroupClient(websocket.WebSocketApp):
    def __init__(self, react_group_id: int, ip: str = '127.0.100', port: int = 6700, token: str = ''):
        self.parser = parser_loader.load()
        self.ws_address = ip
        self.ws_port = port
        self.access_token = token
        self.react_group_id = react_group_id
        self.client_to_query_stats = '1'
        self.client_to_query_online = '2'
        websocket.enableTrace(True)
        url = f'ws://{self.ws_address}:{self.ws_port}/'
        if self.access_token != '':
            url += '?access_token={}'.format(self.access_token)
        logging.info(f'Now connecting to {url}')
        super().__init__(url, on_message=self.on_message)

        self._on_message_func, self._on_message_func_max_time, self._on_start_func = plugin_loader.load()

    def start(self):

        def plugin_thread(*args):
            args[0](args[1])

        for _on_start_func in self._on_start_func:
            thread = threading.Thread(target=plugin_thread, args=(_on_start_func, self))
            thread.setDaemon(True)
            thread.start()

        self.run_forever()

    def send_data(self, data):
        self.send(data)

    def on_message(self, message):
        try:
            formatted_msg, command_args = self.parser.parse(message)

            for on_message_func in self._on_message_func:
                if on_message_func == command_args[0]:
                    @func_timeout.func_set_timeout(self._on_message_func_max_time[on_message_func])
                    def run_command(_interface, _formatted_msg, _command_args):
                        self._on_message_func[on_message_func](_interface, _formatted_msg, _command_args)

                    try:
                        run_command(self, formatted_msg, command_args)
                    except func_timeout.exceptions.FunctionTimedOut:
                        logging.warning(f'[WatchDog]Killed processing command {on_message_func}')

        except TypeError:
            pass
