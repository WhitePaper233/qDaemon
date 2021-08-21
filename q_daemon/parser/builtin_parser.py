# -*- coding:utf-8 -*-
import json
from q_daemon.api import parser_api


class Parser:
    def __init__(self, command_identifier: list):
        self.command_identifier = command_identifier

    @staticmethod
    def format(msg: str, data: dict = None):
        if data is None:
            data = json.loads(msg)
        if data['anonymous'] is None:
            is_anonymous = False
        else:
            is_anonymous = True
        return {
            'is_anonymous': is_anonymous,
            'font': data['font'],
            'group_id': data['group_id'],
            'post_type': data['post_type'],
            'self_id': data['self_id'],
            'anonymous': data['anonymous'],
            'message': {
                'type': data['message_type'],
                'id': data['message_id'],
                'message_seq': data['message_seq'],
                'content': data['message'],
                'raw_content': data['raw_message'],
            },
            'sender': data['sender'],
            'sub_type': data['sub_type'],
            'time': data['time'],
            'user_id': data['user_id'],
        }

    def parse(self, msg: str):
        try:
            data = json.loads(msg)
            if data['post_type'] == 'message':
                identifier = parser_api.is_command(self.command_identifier, data['raw_message'])
                if identifier[0]:
                    args = data['raw_message'].replace(identifier[1], '', 1).split(' ')
                    return self.format(msg, data), args
        except:
            pass
