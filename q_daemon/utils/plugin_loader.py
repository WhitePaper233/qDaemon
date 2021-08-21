# -*- coding:utf-8 -*-
import logging
import pkgutil
import yaml


def load():
    with open('./config.yaml') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    _on_message_func = dict()
    _on_message_func_max_time = dict()
    _on_start_func = list()
    for finder, name, ispck in pkgutil.walk_packages([config['PluginPath']]):
        loader = finder.find_module(name)
        plugin = loader.load_module(name)

        try:
            if not plugin.command_register:
                logging.error(f'Plugin {name} did not register any command.')
            else:
                for command in plugin.command_register:
                    _on_message_func[command['command']] = command['func']
                    _on_message_func_max_time[command['command']] = command['max_time']
        except AttributeError:
            pass

        try:
            _on_start_func.append(plugin.on_start)
        except AttributeError:
            pass

    return _on_message_func, _on_message_func_max_time, _on_start_func


if __name__ == '__main__':
    _plugin = load()
    _plugin[0]['test']()
    _plugin[1][0]()
