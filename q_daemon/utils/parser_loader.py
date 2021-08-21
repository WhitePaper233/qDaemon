# -*- coding:utf-8 -*-

import pkgutil
import yaml


def load():
    with open('./config.yaml', 'r', encoding='utf8') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        if config['ParseConfig']['Parser'] == 'BuiltIn':
            from q_daemon.parser import builtin_parser
            parser = builtin_parser.Parser(config['ParseConfig']['CommandIdentifier'])
        else:
            for finder, name, ispck in pkgutil.walk_packages(['./q_daemon/parser/custom']):
                if name == config['ParseConfig']['Parser']:
                    loader = finder.find_module(name)
                    parser = loader.load_module(name).Parser(config['ParseConfig']['CommandIdentifier'])
                else:
                    from q_daemon.parser import builtin_parser
                    parser = builtin_parser.Parser(config['ParseConfig']['CommandIdentifier'])
    return parser
