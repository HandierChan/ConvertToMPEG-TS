'''用pyhocon导入导出tkGUI各参数的预设文件
'''

# extra modules
from pyhocon import ConfigFactory
from pyhocon import HOCONConverter

import os

def saveHoconFile(pathFileNameExt, parameterDict):
    paramHocon = ConfigFactory.from_dict(parameterDict)
    paramStr = HOCONConverter.to_hocon(paramHocon,indent=4)
    with open(pathFileNameExt, "w", encoding='utf-8') as fd:
        fd.write(paramStr)

def openHoconFile(pathFileNameExt):
    if os.path.exists(pathFileNameExt):
        return ConfigFactory.parse_file(pathFileNameExt)

def createAppDataPath(softwareName='',dataFolder=''):
    # win10 %appdata% 创建文件夹，放用户数据
    appdataPath=os.getenv('appdata')
    fullPath=os.path.normpath(f'{appdataPath}/{softwareName}/{dataFolder}')
    if not os.path.exists(fullPath):
        try:os.makedirs(fullPath)
        except:pass
    else:return fullPath

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
    configPathFileNameExt = f'{currentPath}/{fileExt}'

    # save to current path
    # saveHoconFile(configPathFileNameExt,parameterDict)
    # open aa.txt
    read=openHoconFile(configPathFileNameExt)
    print(read.get_int('Container.Muxrate'))
