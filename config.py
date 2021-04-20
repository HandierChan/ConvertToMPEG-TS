'''用pyhocon导入导出tkGUI各参数的预设文件
'''

# install extra modules
from pyhocon import ConfigFactory
from pyhocon import HOCONConverter

import os

def saveHoconFile(pathFileExt, parameterDict):
    paramHocon = ConfigFactory.from_dict(parameterDict)
    paramStr = HOCONConverter.to_hocon(paramHocon,indent=4)
    with open(pathFileExt, "w", encoding='utf-8') as fd:
        fd.write(paramStr)

def openHoconFile(pathFileExt):
    return ConfigFactory.parse_file(pathFileExt)

if __name__ == "__main__":
    ContainerFormat='mepgts'
    ContainerMuxrate=9000
    VideoFormat='libx264'

    parameterDict={
        'Container':{
            'Format':ContainerFormat,
            'Muxrate':ContainerMuxrate},
        'Video':{
            'Format':VideoFormat}}

    # current path
    currentPath = os.getcwd()
    fileExt = 'pyhocon.txt'
    configPathFileExt = f'{currentPath}/{fileExt}'

    # save to current path
    saveHoconFile(configPathFileExt,parameterDict)
    # open aa.txt
    read=openHoconFile(configPathFileExt)
    print(read.get_int('Container.Muxrate'))
