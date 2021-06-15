'''
得到ffmpeg参数、导入文件和导出路径，转换成发送到cmd的命令
'''

# python3.9 ffmpeg4.3

import os,subprocess
from tkinter import *
from tkinter.filedialog import askdirectory,askopenfilenames,askopenfilename
from tkinter.scrolledtext import ScrolledText

# extra modules
import about


# 当用户选择文件夹，用扩展名来过滤视频文件，可能有遗漏
videoExtLists=('.mov','.mp4','.mpg','.mpeg','.mxf','.mkv','.rmvb','.3gp','.m2v','.m4v','.wmv','.avi','.rm','.flv','.mpv','.ts')
videoExtAskOpenFileNames='*'+';*'.join(videoExtLists)

def filterFileExt(path=r'c:/a.txt', fileExt=['.txt','.mp4']):
    '''
    path是文件或文件夹，返回文件夹里一层(path)所有对应文件格式(fileExt)；是文件就判断文件名(path)是否对应fileExt
    Output: 文件全路径(list)
    '''
    if os.path.isdir(path):
        fileLists = [os.path.abspath(path)+'/'+i for i in os.listdir(path) if os.path.isfile(path+'/'+i)]
        files = [i for i in fileLists if os.path.splitext(i)[1] in fileExt]
        return files
    elif os.path.splitext(path)[1] in fileExt:
        file = []
        file.append(path)
        return file

def correctWinPath(path=r'c:/a.txt'):
    '''
    纠正路径错误：1反斜杠改成正斜杠；2带空格的目录加上双引号
    Output: path(string)
    '''
    absPath=os.path.abspath(path.strip())
    splitPath=absPath.split('\\')
    for i in range(len(splitPath)):
        if ' ' in splitPath[i]:
            splitPath[i] = '"' + splitPath[i] + '"'   # 双引号在文件路径有空格时出现问题 ??????
    windowsPath = '/'.join(splitPath)
    return windowsPath

def outputAllVideos(programPathNameExt='',importFiles=[],userCommand='',exportPath='',exportExt='ts',export=False):
    '''
    # tk获取GUI参数
    programPathNameExt: ffmpeg.exe的路径
    importFiles: 导入视频文件或者路径
    userCommand: 展示给用户看的ffmpeg参数
    exportPath: 导出路径
    exportExt: 导出视频扩展名
    operate: 打印还是发送到cmd
    '''
    programPath = os.path.dirname(programPathNameExt)
    programName=  os.path.basename(programPathNameExt)
    exportPath = correctWinPath(exportPath)
    
    # 过滤所有视频文件
    videoFilesFilterLists = importFiles.split(';')
    videoFiles=[]
    for i in videoFilesFilterLists:
        files = filterFileExt(i.strip(), videoExtLists)
        if files:
            [videoFiles.append(j) for j in files]
    # 修正每个视频文件路径
    videoFiles = [correctWinPath(i) for i in videoFiles]
    # 循环每个视频文件发到cmd执行
    command = userCommand.strip().replace('\n', ' ').replace('\r', ' ')
    for i in videoFiles:
        videoName = os.path.splitext(i)[0].split('/')[-1].lstrip('"')
        videoExt = os.path.splitext(i)[1].rstrip('"')
        cmd = f'''{programName} -hide_banner -y -i {os.path.dirname(i)}/"{videoName}{videoExt}" {command} {exportPath}/"{videoName}.{exportExt}"'''
        subprocess.run(cmd,cwd=programPath,shell=True,encoding="utf-8",check=True) if export == True else print(cmd)
        # os.system(cmd) if export == True else print(cmd) 


# tk窗口要选择的文件或文件夹
def selectFFmpegPath(tkVar):
    selectPath = askopenfilename(filetypes=[('Executable File','*.exe')],title="Select ffmpeg.exe",initialdir=os.getcwd())
    tkVar.set(selectPath)
def selectVideoFiles(tkVar):
    selectFiles = askopenfilenames(filetypes=[('Video Files',videoExtAskOpenFileNames)],title="Import Multiple Videos")
    tkVar.set('; '.join(selectFiles))
def selectOutputPath(tkVar):
    selectPath = askdirectory(title="Output Path")
    tkVar.set(selectPath)



def tkGUIPosition(tkinter,addWidth=10,addHight=10):
    tkinter.resizable(0,0)
    tkinter.update()
    tkGUIWidth = tkinter.winfo_width()
    tkGUIHeigth = tkinter.winfo_height()
    screenWidth = tkinter.winfo_screenwidth()
    screenHeight = tkinter.winfo_screenheight()
    tkinter.geometry("%dx%d+%d+%d"%(tkGUIWidth+addWidth,tkGUIHeigth+addHight,(screenWidth-tkGUIWidth)/2,(screenHeight-tkGUIHeigth)/2))


if __name__ == "__main__":
    tk = Tk()
    tk.title('Convert to MPEG-TS')

    #### 初始化变量
    currentPath = os.getcwd()
    tkVarFFmpegPath = StringVar(tk, value=currentPath+r'\ffmpeg.exe')
    tkVarVideoFiles = StringVar(tk, value=r'z:/a.mp4')
    tkVarOutputPath = StringVar(tk, value=r'z:/')

    #### tk界面元素
    ffmpegInstallPathLabel = Label(tk, text=r'ffmpeg.exe')
    ffmpegInstallPath = Entry(tk, textvariable=tkVarFFmpegPath)
    ffmpegInstallPathButton = Button(tk, text='Select', command=lambda:selectFFmpegPath(tkVarFFmpegPath))
    #
    videoFileLabel = Label(tk, text='Video(s) or Path')
    videoFilesEntry = Entry(tk, textvariable=tkVarVideoFiles)
    videoFilesButton = Button(tk, text='Select', command=lambda:selectVideoFiles(tkVarVideoFiles))
    #
    outputPathLabel = Label(tk, text='Output Path')
    outputPathEntry = Entry(tk, textvariable=tkVarOutputPath)
    outputPathButton = Button(tk, text='Select', command=lambda:selectOutputPath(tkVarOutputPath))
    #
    ffmpegLabel = Label(tk, text='FFmpeg Param')
    ffmpegParam = ScrolledText(tk,width='78',height='6',wrap='word')
    ffParam=r'-f mpegts -muxrate 9M -b:v 8M -maxrate:v 8M -bufsize:v 8M -profile:v high -level:v 4.0 -c:v libx264 -pix_fmt yuv420p -sc_threshold 0 -g 25 -r 25 -refs 3 -x264-params bframes=2:b-adapt=0:force-cfr=1:b-pyramid=0:nal-hrd=cbr -c:a aac -ar 48000 -b:a 128k -ac 2 -flags +ilme+ildct -top 1'
    ffmpegParam.insert(1.0,ffParam)
    ffmpegParam.focus()
    #
    ConvertButton=Button(tk,text='Start',fg='green',command=lambda:
        outputAllVideos(ffmpegInstallPath.get(),videoFilesEntry.get(),ffmpegParam.get(1.0,END),outputPathEntry.get(),'ts',export=1))
    AboutButton=Button(tk,text='About',command=lambda:about.about())

    #### tk界面布局
    ffmpegInstallPathLabel.grid(row=0,column=0,sticky='e',ipadx=10)
    ffmpegInstallPath.grid(row=0,column=1,sticky='w',ipadx=266,pady=5)
    ffmpegInstallPathButton.grid(row=0,column=2,sticky='w')
    #
    videoFileLabel.grid(row=1,column=0,sticky='e',ipadx=10)
    videoFilesEntry.grid(row=1,column=1,sticky='w',ipadx=266,pady=5)
    videoFilesButton.grid(row=1,column=2,sticky='w')
    #
    outputPathLabel.grid(row=2,column=0,sticky='e',ipadx=10)
    outputPathEntry.grid(row=2,column=1,sticky='w',ipadx=266,pady=5)
    outputPathButton.grid(row=2,column=2,sticky='w')
    #
    ffmpegLabel.grid(row=3,column=0,sticky='ne',ipadx=10)
    ffmpegParam.grid(row=3,column=1,sticky='w',ipadx=5,pady=5)
    #
    ConvertButton.grid(row=4,column=1,sticky='w',ipadx=20,pady=5)
    AboutButton.grid(row=4,column=1,sticky='e',ipadx=20)

    tkGUIPosition(tk,20,20)

    tk.mainloop()
