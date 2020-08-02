# python3.7 ffmpeg4.3
import os
from tkinter import *
from tkinter.filedialog import askdirectory,askopenfilenames

def exportAllABC():
    # 获取GUI参数
    ffmpegEXE = mayaInstPath.get()
    ffmpegEXEPath = correctWinPath(ffmpegEXE)

    convertPath = abcPathEntry.get()
    exportPath = correctWinPath(convertPath)
    
    # 得到所有视频文件
    mayaFilesJudge = mayaFilesEntry.get()
    mayaFilesJudgeLists = mayaFilesJudge.split(',')
    mayaFiles=[]
    for i in mayaFilesJudgeLists:
        files = filterFileExt(i.strip(), ['.mov','.mp4'])
        if files:
            [mayaFiles.append(j) for j in files]
    # 修正每个视频文件路径格式
    mayaFiles = [correctWinPath(i) for i in mayaFiles]


    # 循环每个maya文件发到cmd执行
    for i in mayaFiles:
        videoName = os.path.splitext(i)[0].split('/')[-1]
        videoExt = os.path.splitext(i)[1]
        command = '-f mpegts -muxrate 8M -c:v libx264 -profile:v high -level:v 4.2 -pix_fmt yuv420p -sc_threshold 0 -g 25 -b:v 7M -maxrate:v 7M -bufsize:v 7M -r 25 -refs 3 -x264-params bframes=2:b-adapt=0:force-cfr=1:b-pyramid=0:nal-hrd=cbr -c:a mp2 -ar 48000 -b:a 192k -ac 2'
        cmd = ffmpegEXEPath+' -y -i '+os.path.dirname(i)+'/'+videoName+videoExt+' '+command+' '+exportPath+'/'+videoName+'.ts'
        #os.system(cmd)
        print(cmd)

def correctWinPath(path=r'c:/a.txt'):
    '''
    纠正路径错误：1反斜杠改成正斜杠；2带空格的目录加上双引号
    Output: path(string)
    '''
    absPath = os.path.abspath(path.strip())
    splitPath = absPath.split('\\')
    for i in range( len(splitPath)):
        if ' ' in splitPath[i]:
            splitPath[i] = '"' + splitPath[i] + '"'
    windowsPath = '/'.join(splitPath)
    return windowsPath

def filterFileExt(path=r'c:/a.txt', fileExt=['.mov','.mp4']):
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

def about():
    tk = Tk()
    tk.title('关于')
    tkWinWidth = 330
    tkWinHeigth = 100
    screenWidth = tk.winfo_screenwidth()
    screenHeight = tk.winfo_screenheight()
    tkWinXPos = (screenWidth - tkWinWidth) / 2
    tkWinYPos = (screenHeight - tkWinHeigth) / 2
    tk.geometry( "%dx%d+%d+%d" % (tkWinWidth,tkWinHeigth,tkWinXPos,tkWinYPos))
    Label(tk,text='制作：天雷动漫').grid(row=0,sticky='w')
    Label(tk,text='测试环境：python3.7 ffmpeg4.3').grid(row=1,sticky='w')
    Label(tk,text='源码：https://github.com/HandierChan').grid(row=2,sticky='w')


# 窗口
tk = Tk()
tk.title('To mpeg-ts')
#tk.iconbitmap('C:/aa.ico')
tk.resizable(0,0)
tkWinWidth = 700
tkWinHeigth = 150
screenWidth = tk.winfo_screenwidth()
screenHeight = tk.winfo_screenheight()
tkWinXPos = (screenWidth - tkWinWidth) / 2
tkWinYPos = (screenHeight - tkWinHeigth) / 2
tk.geometry( "%dx%d+%d+%d" % (tkWinWidth,tkWinHeigth,tkWinXPos,tkWinYPos))


# 初始变量
currentPath = os.path.dirname(__file__)
VarMayaInstPath = StringVar(tk, value=currentPath+r'\ffmpeg.exe')
VarmayaFiles = StringVar(tk)
VarabcPath = StringVar(tk)
def selectMayaInstPath():
    select_path = askopenfilenames()
    VarMayaInstPath.set(select_path)
def selectMayaFiles():
    select_files = askopenfilenames()
    # a=tk.splitlist(select_files)
    VarmayaFiles.set(', '.join(select_files))
def selectABCPath():
    select_path = askdirectory()
    VarabcPath.set(select_path)


# 界面元素
mayaInstPathLabel = Label(tk, text=r'ffmpeg.exe')
mayaInstPath = Entry(tk, textvariable=VarMayaInstPath)
mayaInstPathButton = Button(tk, text='Select', command=selectMayaInstPath)

mayaFileLabel = Label(tk, text='Videos or Path')
mayaFilesEntry = Entry(tk, textvariable=VarmayaFiles)
mayaFilesButton = Button(tk, text='Select', command=selectMayaFiles)

abcPathLabel = Label(tk, text='Convert Path')
abcPathEntry = Entry(tk, textvariable=VarabcPath)
abcPathButton = Button(tk, text='Select', command=selectABCPath)

#noticeLabel = Label(tk, text='(路径目前不支持带空格)',fg='green')

convertButton = Button(tk, text='Start', command = exportAllABC)
aboutLabel = Button(tk,text='关于',command=about)


# 界面布局
mayaInstPathLabel.grid(row=0, column=0, sticky='e',ipadx=10)
mayaInstPath.grid(row=0, column=1, sticky='w',ipadx=100)
mayaInstPathButton.grid(row=0, column=2, sticky='w')

mayaFileLabel.grid(row=1, column=0, sticky='e',ipadx=10)
mayaFilesEntry.grid(row=1, column=1, sticky='w',ipadx=200)
mayaFilesButton.grid(row=1, column=2, sticky='w')

abcPathLabel.grid(row=2, column=0, sticky='e',ipadx=10)
abcPathEntry.grid(row=2, column=1, sticky='w',ipadx=200)
abcPathButton.grid(row=2, column=2, sticky='w')

#noticeLabel.grid(row=3, column=1, sticky='w')

convertButton.grid(row=4, column=1, sticky='w', ipadx=20)
aboutLabel.grid(row=4, column=2, sticky='e')


tk.mainloop()
