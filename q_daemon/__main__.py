# -*- coding:utf-8 -*-
import yaml

from q_daemon.interface import cqhttp_interface


def run():
    with open('./config.yaml', 'r', encoding='utf8') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    if config['qDeamonMode'] == "Group":
        client = cqhttp_interface.GroupClient(react_group_id=config['GroupConfig']['ReactGroup'],
                                              ip=config['cqhttpConfig']['IpAddress'],
                                              port=config['cqhttpConfig']['Port'],
                                              token=config['cqhttpConfig']['Token'])
        client.start()
