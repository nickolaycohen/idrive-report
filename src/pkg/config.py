from configparser import ConfigParser
import os

def load_config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    loc = '/src/pkg/'
    cwd = os.path.abspath(os.getcwd()).replace('\\','/')
    path = cwd+loc
    filename_ = path + filename
    parser.read(filename_)
    # print(parser.sections())

    # get section, default to postgresql
    config = {}
    if section in parser:
        for key in parser[section]:
            config[key] = parser[section][key]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    return config

if __name__ == '__main__':
    config = load_config()
    print(config)