# -*- coding:utf-8 -*-
import json


A = 'hello'


def on_message(interface, formatted_msg, command_args):
    reply = {
            "action": "send_group_msg",
            "params": {
                "group_id": interface.react_group_id,
                "message": "qDaemon,基于go-cqhttp的QQ机器人实现"
                           +"\nPowered By WhitePaper233\n开源软件许可:GPL-3.0 License"
                           +"\n项目地址:https://github.com/AngelicaRoot/qDaemon"
                           +"\nTesting Reforged Version"
            }
        }
    interface.send(json.dumps(reply))


command_register = [
    {
        'command': 'info',
        'func': on_message,
        'max_time': 6
    },
]
