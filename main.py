'''
??? ffmpeg 不清楚：
1.'-nal-hrd cbr' 去掉后 Encoding 变成 'abr'，用旧版本 EasyICE 码率变成一个数?
2.'-bluray-compat 1' 可以锁住帧率，但什么是蓝光兼容?
3.'itsoffset 0.06' 音视频偏移的其它办法?
'''

# python3.9 ffmpeg4.3

import os
from tkinter import *
from tkinter import ttk,scrolledtext,font
from tkinter.filedialog import askopenfilename,asksaveasfilename
#from PIL import Image,ImageTk

# extra modules
import pyhoconConfig
import about
import convert


#### GUI 控件大小
containerpadx=10
containerpady=5

labelWidth=18
comboboxWidth=12
entryWidth=15

gridPadx=5
gridPady=3

buttonWidth=9

# 默认参数
softwareName='ConvertToMPEGTS'


#### 默认配置按键
def defaultParam():
    [i.current(1) for i in allComboboxControl]
    # [i.set('') for i in allEntryControlVar]
    ## 覆盖
    videoScanType.current(0) 
    ffmpegPathVar.set(os.getcwd()+r'\ffmpeg.exe')
    serviceNameVar.set('TThunderAnimation')
    ffmpegExtraParamVar.set('')
    encoderExtraParamVar.set('force-cfr=1')
def clearParam():
    [i.current(0) for i in allComboboxControl]
    [i.set('') for i in allEntryControlVar]

#### 菜单栏定义
def openConfigFile(openGUIRead=False):
    if openGUIRead==False:selectPathFileExt=askopenfilename(filetypes=[("Config File","*.txt")],title="Open preset",initialdir=currentPresetsPath())
    else:selectPathFileExt=convert.createAppDataPath(softwareName,'presets')+'/history.txt'
    try:hoconConfig=pyhoconConfig.openHoconFile(selectPathFileExt) # askopenfilename鼠标点取消打开的窗口会报错
    except:pass
    #### 设置参数
    configDict={
    containerFormat:'Container.Format',containerBit:'Container.OverallBitRate',
    videoEncoder:'Video.Encoder',videoEntropy:'Video.Entropy',videoBitRate:'Video.BitRate',videoCBR:'Video.Constant',videoSize:'Video.Size',videoAspect:'Video.Aspect',videoProfile:'Video.Profile',videoLevel:'Video.Level',videoFrameRate:'Video.FrameRate',videoGOP:'Video.GOP',videoReference:'Video.ReferenceFrames',videoBFrames:'Video.B-Frames',videoPixelFormat:'Video.PixelFormat',videoColorSpace:'Video.ColorSpace',videoScanType:'Video.ScanType',
    audioFormat:'Audio.Format',audioBitRate:'Audio.BitRate',audioChannel:'Audio.Channels',audioSample:'Audio.SampleRate'
    }
    for k,v in configDict.items():
        try:k.set(hoconConfig.get_string(v))
        except:pass
    try:
        ## StringVar 不能用上面for循环set参数，要单独try set，待优化
        serviceNameVar.set(hoconConfig.get_string('Container.ServiceName'))
        ffmpegExtraParamVar.set(hoconConfig.get_string('Extra.FFmpegParameters'))
        encoderExtraParamVar.set(hoconConfig.get_string('Extra.EncoderParameters'))
        ## 以下会出现异常，最后再try
        ffmpegPathVar.set(hoconConfig.get_string('IOPath.ffmpegPath'))
        inputVideosVar.set(hoconConfig.get_string('IOPath.videosPath'))
        outputPathVar.set(hoconConfig.get_string('IOPath.outputPath'))
    except:pass
def saveConfigFile():
    pathFileExt=asksaveasfilename(filetypes=[("Config File","*.txt")],title="Save preset",initialdir=currentPresetsPath())
    if 'txt' not in pathFileExt[-3:].lower(): pathFileExt+='.txt'
    pyhoconConfig.saveHoconFile(pathFileExt,allConfigParam(writeIOData=False))
def currentPresetsPath():
    currentPath=os.getcwd()
    presetsPath=os.path.normpath(currentPath+'/presets')
    return presetsPath if os.path.exists(presetsPath) else currentPath
def quitWindow():
    try:pyhoconConfig.saveHoconFile(convert.createAppDataPath(softwareName,'presets')+'/history.txt',allConfigParam(writeIOData=True))
    except:pass
    tk.quit()
    tk.destroy()
    exit()


tk=Tk()
tk.title('Convert to MPEG-TS')
# tk.iconbitmap('C:/aa.ico')
#### GUI 菜单栏
tk_Menu = Menu(tk)
tk.config(menu=tk_Menu)
# File
menu_file = Menu(tk_Menu,tearoff=0)
menu_file.add_command(label="Open Preset",command=lambda:[openConfigFile(),refreshParamPreview(tk)])
menu_file.add_command(label="Save Preset",command=saveConfigFile)
menu_file.add_separator()
menu_file.add_command(label="Exit",command=quitWindow)
# Help
menu_help = Menu(tk_Menu,tearoff=0)
menu_help.add_command(label="About",command=lambda:about.about())
# GUI 添加菜单栏
tk_Menu.add_cascade(label="File",menu=menu_file)
tk_Menu.add_cascade(label="Help",menu=menu_help)


### GUI框架 Frame
IOFrame = LabelFrame(tk,relief=FLAT)
IOFrame.grid(row=0,column=0,padx=containerpadx,pady=0,columnspan=2,sticky='WENS')
defaultButton = LabelFrame(tk,relief=FLAT)
defaultButton.grid(row=1,column=0,padx=containerpadx,pady=0,columnspan=2,sticky='WENS')
containerFrame = LabelFrame(tk,bd=2,text='Container')
containerFrame.grid(row=2,column=0,padx=containerpadx,pady=containerpady,columnspan=2,sticky='WENS')
videoFrame = LabelFrame(tk,bd=2,text='Video')
videoFrame.grid(row=3,column=0,padx=containerpadx,pady=containerpady,rowspan=2,sticky='WENS')
audioFrame = LabelFrame(tk, text='Audio')
audioFrame.grid(row=3,column=1,padx=containerpadx,pady=containerpady,sticky='WENS')
extraOptionsFrame = LabelFrame(tk, text='Extra Options')
extraOptionsFrame.grid(row=4,column=1,padx=containerpadx,pady=containerpady,sticky='WENS')
commandFrame = LabelFrame(tk, text='Command',relief=FLAT)
commandFrame.grid(row=5,column=0,padx=containerpadx,pady=containerpady,columnspan=2,sticky='WENS')
## GUI区域 最底下 Info 控件
Label(tk,text='',anchor=E,fg='green').grid(row=6,column=0,sticky='W')

### GUI区域 默认按钮 控件
defParams = Button(defaultButton,text='Default',width=buttonWidth,fg='green',font=('normal',9,'bold'),command=lambda:[defaultParam(),refreshParamPreview(tk)])
defParams.grid(row=0,column=0,padx=gridPadx,pady=gridPady)
clearParams = Button(defaultButton,text='Clear',width=buttonWidth,fg='green',font=('normal',9,'bold'),command=lambda:[clearParam(),refreshParamPreview(tk)])
clearParams.grid(row=0,column=1,padx=gridPadx,pady=gridPady)
howToButton = Button(defaultButton,text='How to...',width=buttonWidth,fg='green',font=('normal',9,'bold'),command=lambda:about.howto())
howToButton.grid(row=0,column=2,padx=gridPadx,pady=gridPady)

### GUI区域 IO 控件
Label(IOFrame, text=r'ffmpeg.exe').grid(row=1,column=0,sticky='E',padx=gridPadx,pady=gridPady)
ffmpegPathVar = StringVar()
ffmpegPathEntry = Entry(IOFrame,textvariable=ffmpegPathVar)
ffmpegPathEntry.grid(row=1,column=1,sticky='W',ipadx=266,pady=gridPady)
ffmpegPathButton = Button(IOFrame, text='Select',command=lambda:convert.selectFFmpegPath(ffmpegPathVar))
ffmpegPathButton.grid(row=1,column=2,sticky='W')
Label(IOFrame, text='Input Videos/Path').grid(row=2,column=0,sticky='E',padx=gridPadx,pady=gridPady)
inputVideosVar = StringVar()
inputVideosEntry = Entry(IOFrame,textvariable=inputVideosVar)
inputVideosEntry.grid(row=2,column=1,sticky='W',ipadx=266,pady=gridPady)
inputVideosButton = Button(IOFrame, text='Select',command=lambda:convert.selectVideoFiles(inputVideosVar))
inputVideosButton.grid(row=2,column=2,sticky='W')
Label(IOFrame, text='Output Path').grid(row=3,column=0,sticky='E',padx=gridPadx,pady=gridPady)
outputPathVar = StringVar()
outputPathEntry = Entry(IOFrame,textvariable=outputPathVar)
outputPathEntry.grid(row=3,column=1,sticky='W',ipadx=266,pady=gridPady)
outputPathButton = Button(IOFrame,text='Select',command=lambda:convert.selectOutputPath(outputPathVar))
outputPathButton.grid(row=3,column=2,sticky='W')

### GUI区域 Container 控件
Label(containerFrame,text='Format',anchor=E,width=labelWidth).grid(row=0,column=0,sticky='E',padx=gridPadx,pady=gridPady)
containerFormat = ttk.Combobox(containerFrame,width=comboboxWidth)
containerFormat['values'] = ('','ts')
containerFormat.grid(row=0,column=1,padx=gridPadx,pady=gridPady)
Label(containerFrame,text='Overall Bit Rate (kbps)',anchor=E,width=labelWidth).grid(row=0,column=2,sticky='E',padx=gridPadx,pady=gridPady)
containerBit = ttk.Combobox(containerFrame,width=comboboxWidth)
containerBit['values'] = ('','9000','8000','7000','6000','5000','4000')
containerBit.grid(row=0,column=3,padx=gridPadx,pady=gridPady)
Label(containerFrame,text='Service Name',anchor=E,width=labelWidth).grid(row=0,column=4,sticky='E',padx=gridPadx,pady=gridPady)
serviceNameVar=StringVar()
serviceNameEntry = Entry(containerFrame,width=entryWidth+12,textvariable=serviceNameVar)
serviceNameEntry.grid(row=0,column=5,padx=gridPadx,pady=gridPady)

### GUI区域 Video 控件
Label(videoFrame,text='Encoder',anchor=E,width=labelWidth).grid(row=0,column=0,sticky='E',padx=gridPadx,pady=gridPady)
videoEncoder = ttk.Combobox(videoFrame,width=comboboxWidth)
videoEncoder['values'] = ('','libx264','libx265')
videoEncoder.grid(row=0,column=1,padx=gridPadx,pady=gridPady)
Label(videoFrame,text='Entropy',anchor=E,width=labelWidth).grid(row=0,column=2,sticky='E',padx=gridPadx,pady=gridPady)
videoEntropy = ttk.Combobox(videoFrame,width=comboboxWidth)
videoEntropy['values'] = ('','cabac','cavlc')
videoEntropy.grid(row=0,column=3,padx=gridPadx,pady=gridPady)
Label(videoFrame,text='Bit Rate (kbps)',anchor=E,width=labelWidth).grid(row=1,column=0,sticky='E',padx=gridPadx,pady=gridPady)
videoBitRate = ttk.Combobox(videoFrame,width=comboboxWidth)
videoBitRate['values'] = ('','8000','7000','6000','5000')
videoBitRate.grid(row=1,column=1,padx=gridPadx,pady=gridPady)
Label(videoFrame,text='Constant',anchor=E,width=labelWidth).grid(row=1,column=2,sticky='E',padx=gridPadx,pady=gridPady)
videoCBR = ttk.Combobox(videoFrame,width=comboboxWidth)
videoCBR['values'] = ('','cbr','vbr')
videoCBR.grid(row=1,column=3,padx=gridPadx,pady=gridPady)
Label(videoFrame,text='Size',anchor=E,width=labelWidth).grid(row=2,column=0,sticky='E',padx=gridPadx,pady=gridPady)
videoSize = ttk.Combobox(videoFrame,width=comboboxWidth)
videoSize['values'] = ('','1920x1080','1280x720')
videoSize.grid(row=2,column=1,padx=gridPadx,pady=gridPady)
Label(videoFrame,text='Aspect',anchor=E,width=labelWidth).grid(row=2,column=2,sticky='E',padx=gridPadx,pady=gridPady)
videoAspect = ttk.Combobox(videoFrame, width=comboboxWidth)
videoAspect['values'] = ('','16:9','4:3')
videoAspect.grid(row=2,column=3,padx=gridPadx,pady=gridPady)
Label(videoFrame,text='Profile',anchor=E,width=labelWidth).grid(row=3,column=0,sticky='E',padx=gridPadx,pady=gridPady)
videoProfile = ttk.Combobox(videoFrame,width=comboboxWidth)
videoProfile['values'] = ('','high','main')
videoProfile.grid(row=3,column=1,padx=gridPadx,pady=gridPady)
Label(videoFrame,text='Level',anchor=E,width=labelWidth).grid(row=3,column=2,sticky='E',padx=gridPadx,pady=gridPady)
videoLevel = ttk.Combobox(videoFrame,width=comboboxWidth)
videoLevel['values'] = ('','4.2','4.1','4.0')
videoLevel.grid(row=3,column=3,padx=gridPadx,pady=gridPady)
Label(videoFrame,text='Frame Rate',anchor=E,width=labelWidth).grid(row=4,column=0,sticky='E',padx=gridPadx,pady=gridPady)
videoFrameRate = ttk.Combobox(videoFrame,width=comboboxWidth)
videoFrameRate['values'] = ('','25','30')
videoFrameRate.grid(row=4,column=1,padx=gridPadx,pady=gridPady)
Label(videoFrame,text='GOP',anchor=E,width=labelWidth).grid(row=4,column=2,sticky='E',padx=gridPadx,pady=gridPady)
videoGOP = ttk.Combobox(videoFrame,width=comboboxWidth)
videoGOP['values'] = ('','25')
videoGOP.grid(row=4,column=3,padx=gridPadx,pady=gridPady)
Label(videoFrame,text='Reference Frames',anchor=E,width=labelWidth).grid(row=5,column=0,sticky='E',padx=gridPadx,pady=gridPady)
videoReference = ttk.Combobox(videoFrame,width=comboboxWidth)
videoReference['values'] = ('','3')
videoReference.grid(row=5,column=1,padx=gridPadx,pady=gridPady)
Label(videoFrame,text='B-Frames',anchor=E,width=labelWidth).grid(row=5,column=2,sticky='E',padx=gridPadx,pady=gridPady)
videoBFrames = ttk.Combobox(videoFrame,width=comboboxWidth)
videoBFrames['values'] = ('','2')
videoBFrames.grid(row=5,column=3,padx=gridPadx,pady=gridPady)
Label(videoFrame,text='Pixel Format',anchor=E,width=labelWidth).grid(row=6,column=0,sticky='E',padx=gridPadx,pady=gridPady)
videoPixelFormat = ttk.Combobox(videoFrame,width=comboboxWidth)
videoPixelFormat['values'] = ('','yuv420p','yuv422p10')
videoPixelFormat.grid(row=6,column=1,padx=gridPadx,pady=gridPady)
Label(videoFrame,text='Color Space',anchor=E,width=labelWidth).grid(row=6,column=2,sticky='E',padx=gridPadx,pady=gridPady)
videoColorSpace = ttk.Combobox(videoFrame,width=comboboxWidth)
videoColorSpace['values'] = ('','bt709')
videoColorSpace.grid(row=6,column=3,padx=gridPadx,pady=gridPady)
Label(videoFrame,text='Scan Type',anchor=E,width=labelWidth).grid(row=7,column=0,sticky='E',padx=gridPadx,pady=gridPady)
videoScanType = ttk.Combobox(videoFrame,state='readonly',width=comboboxWidth)
videoScanType['values'] = ('','Top Field','Bottom Field','Deinterlace')
videoScanType.grid(row=7,column=1,padx=gridPadx,pady=gridPady)
Label(videoFrame,text='???Delay to Video',anchor=E,width=labelWidth).grid(row=8,column=0,sticky='E',padx=gridPadx,pady=gridPady)
videoDelaytoVideo = ttk.Combobox(videoFrame,width=comboboxWidth)
videoDelaytoVideo['values'] = ('')
videoDelaytoVideo.grid(row=8,column=1,padx=gridPadx,pady=gridPady)

### GUI区域 Audio 控件
Label(audioFrame,text='Format',anchor=E,width=labelWidth).grid(row=0,column=0,sticky='E',padx=gridPadx,pady=gridPady)
audioFormat = ttk.Combobox(audioFrame,width=comboboxWidth)
audioFormat['values'] = ('','aac','mp3','mp2')
audioFormat.grid(row=0,column=1,padx=gridPadx,pady=gridPady)
Label(audioFrame,text='Bit Rate (kbps)',anchor=E,width=labelWidth).grid(row=1,column=0,sticky='E',padx=gridPadx,pady=gridPady)
audioBitRate = ttk.Combobox(audioFrame, width=comboboxWidth)
audioBitRate['values'] = ('','128','192','320')
audioBitRate.grid(row=1,column=1,padx=gridPadx,pady=gridPady)
Label(audioFrame,text='Channels',anchor=E,width=labelWidth).grid(row=2,column=0,sticky='E',padx=gridPadx,pady=gridPady)
audioChannel = ttk.Combobox(audioFrame,width=comboboxWidth)
audioChannel['values'] = ('','2','4')
audioChannel.grid(row=2,column=1,padx=gridPadx,pady=gridPady)
Label(audioFrame,text='Sample Rate (Hz)',anchor=E,width=labelWidth).grid(row=3,column=0,sticky='E',padx=gridPadx,pady=gridPady)
audioSample = ttk.Combobox(audioFrame,width=comboboxWidth)
audioSample['values'] = ('','48000','44100')
audioSample.grid(row=3,column=1,padx=gridPadx,pady=gridPady)

### GUI区域 ExtraOptions 控件
Label(extraOptionsFrame,text='FFmpeg Parameters:',anchor=W,width=labelWidth).grid(row=0,column=0,sticky='W',padx=gridPadx,pady=gridPady)
ffmpegExtraParamVar = StringVar()
ffmpegExtraParamEntry = ttk.Entry(extraOptionsFrame,width=45,textvariable=ffmpegExtraParamVar) 
ffmpegExtraParamEntry.grid(row=1,column=0,padx=gridPadx,pady=gridPady)
Label(extraOptionsFrame,text='Encoder Parameters (Separated by ":")',anchor=W).grid(row=2,column=0,sticky='W',padx=gridPadx,pady=gridPady)
encoderExtraParamVar = StringVar()
encoderExtraParamEntry = ttk.Entry(extraOptionsFrame,width=45,textvariable=encoderExtraParamVar) 
encoderExtraParamEntry.grid(row=3,column=0,padx=gridPadx,pady=gridPady)

### GUI区域 Command 控件
commandText = scrolledtext.ScrolledText(commandFrame,width=100,height=6,wrap=WORD)
commandText.grid(row=0, column=0, sticky='WE')
executeCmdButton = Button(commandFrame,text='Convert',width=buttonWidth,fg='green',font=('normal',9,'bold'),command=lambda: executeParamCmd())
executeCmdButton.grid(row=1, column=0,sticky='W',padx=gridPadx,pady=gridPady)




# 自动更新事件的控件列表，需要手动添加
allComboboxControl=[containerFormat,containerBit,videoEncoder,videoEntropy,videoBitRate,videoCBR,videoSize,videoAspect,videoProfile,videoLevel,videoFrameRate,videoGOP,videoReference,videoBFrames,videoPixelFormat,videoColorSpace,videoScanType,audioFormat,audioBitRate,audioChannel,audioSample]
allEntryControlVar=[serviceNameVar,ffmpegExtraParamVar,encoderExtraParamVar,ffmpegPathVar,inputVideosVar,outputPathVar]
allEntryControl=[serviceNameEntry,ffmpegExtraParamEntry,encoderExtraParamEntry]
# print(len(allComboboxControl)+len(allEntryControlVar)) # 检查数量



# 打开 tkGUI 窗口，读取默认参数 %appdata%/softwareName/presets
defaultParam()
openConfigFile(openGUIRead=True)



#### 定义自动化函数
def paramModifySimple(commandStr='',pKey='',suffix=''):
    # 输出 commandStr+pKey，pKey为空则输出空
    # suffix 是后缀
    commandStr=commandStr.strip()
    pKey=pKey.strip()
    if pKey == '': return ''
    else: return f'{commandStr} {pKey}{suffix}'
def paramModifySimple_metadata(commandStr='',pKey='',space=True):
    # 输出 commandStr+pKey，pKey为空则输出空
    # space 是用给"-metadata service_name"
    commandStr=commandStr.strip()
    pKey=pKey.strip()
    if pKey == '': return ''
    else: return f'{commandStr}"{pKey}"'
def paramModifySimple_videoBitRate(pKey,CBR='cbr',suffix=''):
    # 输出 commandStr+pKey，pKey为空则输出空
    # 只用于 videoBitRate tk控件
    pKey=pKey.strip()
    CBR=CBR.strip()
    if pKey == '': return ''
    elif CBR=='cbr': return f'-b:v {pKey}{suffix} -maxrate:v {pKey}{suffix} -bufsize:v {pKey}{suffix}'
    else: return f'-b:v {pKey}{suffix}'
def paramModifySimple_colorSpace(pKey):
    # 输出 commandStr+pKey，pKey为空则输出空
    # 只用于 ColorSpace tk控件
    pKey=pKey.strip()
    if pKey == '': return ''
    else: return f'-color_range tv -color_primaries {pKey} -color_trc {pKey} -colorspace {pKey}'
def paramModifySimple_encoderExtraParam(encoder='',pKey=''):
    # 输出 **+pKey，pKey为空则输出空
    # 只用于 encoderExtraParam tk控件
    encoder=encoder.strip()
    pKey=pKey.strip()
    if pKey == '': return ''
    elif encoder=='libx264': return f'-x264-params {pKey}'
    elif encoder=='libx265': return f'-x265-params {pKey}'
    else:return ''
def paramModifySimple_scanType(pKey):
    # 只用于 ScanType tk控件
    ScanTypeDict={'':'','Top Field':'-flags +ilme+ildct -top 1','Bottom Field':'-flags +ilme+ildct -top 0','Deinterlace':'-vf yadif=0:-1:0'}
    return ScanTypeDict.get(pKey)

# def test(p='',x=[]):
#     #-x264-params 里面':'内容，代码有问题
#     aa='force-cfr=1' if 'a' in x else ''
#     bb='b-pyramid=0' if 'b' in x else ''
#     cc='ccc' if 'c' in x else ''
#     zz=[aa,bb,cc]
#     z=':'.join(filter(None, zz))
#     return f'{p} {z}'
# print(m(p='-x264-params',x=['a','b','c']))

def refreshParamPreviewConfig():
    listParam = [paramModifySimple('-muxrate',containerBit.get(),suffix='k'),
                paramModifySimple_metadata('-metadata service_name=',serviceNameVar.get()),
                paramModifySimple('-c:v',videoEncoder.get()),
                paramModifySimple_videoBitRate(videoBitRate.get(),videoCBR.get(),suffix='k'),
                paramModifySimple('-nal-hrd',videoCBR.get()),
                paramModifySimple('-s',videoSize.get()),
                paramModifySimple('-aspect',videoAspect.get()),
                paramModifySimple('-r',videoFrameRate.get()), # '-bluray-compat 1'
                paramModifySimple('-profile:v',videoProfile.get()),
                paramModifySimple('-level:v',videoLevel.get()),
                paramModifySimple('-sc_threshold 0 -g',videoGOP.get()), # also closed GOP
                paramModifySimple('-b_strategy 0 -bf',videoBFrames.get()), # also constant B-frames
                paramModifySimple('-b-pyramid none -refs',videoReference.get()), # also strict B-frames as references 
                paramModifySimple('-pix_fmt',videoPixelFormat.get()),
                paramModifySimple_colorSpace(videoColorSpace.get()),
                paramModifySimple_scanType(videoScanType.get()),
                #
                paramModifySimple('-c:a',audioFormat.get()),
                paramModifySimple('-b:a',audioBitRate.get(),suffix='k'),
                paramModifySimple('-ac',audioChannel.get()),
                paramModifySimple('-ar',audioSample.get()),
                #
                ffmpegExtraParamVar.get().strip(),
                paramModifySimple_encoderExtraParam(videoEncoder.get(),encoderExtraParamVar.get()), 
                ]
    listParam = [i for i in listParam if i != '']
    return ' '.join(listParam)

def refreshParamPreview(event):
    # ffmpeg参数插入到tkGUI最底部编辑
    commandText.delete('1.0', "end")
    commandText.insert('1.0', refreshParamPreviewConfig())
refreshParamPreview(tk)

def executeParamCmd():
    # 调用 convert.py 命令输出，export=1输出|0打印
    commandCmd = commandText.get('1.0', "end")
    convert.outputAllVideos(programPath=ffmpegPathEntry.get(),importFiles=inputVideosEntry.get(),userCommand=commandCmd,exportPath=outputPathEntry.get(),exportExt=containerFormat.get(),export=1)



##### 事件
# Button 颜色事件
def SetBGColor(event):
    event.widget.config(bg='White')
def ReturnBGColor(event):
    event.widget.config(bg='SystemButtonFace')
for i in [defParams,clearParams,executeCmdButton,ffmpegPathButton,inputVideosButton,outputPathButton,howToButton]:
    i.bind("<Enter>", SetBGColor)
    i.bind("<Leave>", ReturnBGColor)

# tk 控件事件更新
for i in allComboboxControl:
    i.bind('<KeyRelease>',refreshParamPreview)
    i.bind('<ButtonRelease>',refreshParamPreview)
    i.bind('<FocusIn>',refreshParamPreview)
for i in allEntryControl:
    i.bind('<KeyRelease>',refreshParamPreview)
    i.bind('<ButtonRelease>',refreshParamPreview)
    i.bind('<FocusIn>',refreshParamPreview)

# 禁止 Combobox 鼠标滑轮事件
tk.unbind_class("TCombobox", "<MouseWheel>")



#### 全部配置参数，导入导出 preset
def allConfigParam(writeIOData=False):
    mainParameter={
        'Container':{
            'Format':containerFormat.get().strip(),
            'OverallBitRate':containerBit.get().strip(),
            'ServiceName':serviceNameVar.get().strip()},
        'Video':{
            'Encoder':videoEncoder.get().strip(),
            'Entropy':videoEntropy.get().strip(),
            'BitRate':videoBitRate.get().strip(),
            'Constant':videoCBR.get().strip(),
            'Size':videoSize.get().strip(),
            'Aspect':videoAspect.get().strip(),
            'Profile':videoProfile.get().strip(),
            'Level':videoLevel.get().strip(),
            'FrameRate':videoFrameRate.get().strip(),
            'GOP':videoGOP.get().strip(),
            'ReferenceFrames':videoReference.get().strip(),
            'B-Frames':videoBFrames.get().strip(),
            'PixelFormat':videoPixelFormat.get().strip(),
            'ColorSpace':videoColorSpace.get().strip(),
            'ScanType':videoScanType.get().strip(),},
        'Audio':{
            'Format':audioFormat.get().strip(),
            'BitRate':audioBitRate.get().strip(),
            'Channels':audioChannel.get().strip(),
            'SampleRate':audioSample.get().strip()},
        'Extra':{
            'FFmpegParameters':ffmpegExtraParamVar.get().strip(),
            'EncoderParameters':encoderExtraParamVar.get().strip()}
    }
    IOParameter={
        'IOPath':{
            'ffmpegPath':ffmpegPathVar.get().strip(),
            'videosPath':inputVideosVar.get().strip(),
            'outputPath':outputPathVar.get().strip()}
    }
    allParameter={**mainParameter,**IOParameter}
    return allParameter if writeIOData==True else mainParameter


convert.tkGUIPosition(tk,addWidth=0,addHight=0)

# 鼠标点'X'窗口关闭时，执行程序
tk.protocol("WM_DELETE_WINDOW", quitWindow)

tk.mainloop()




# 进度条 Info控件
# python tkinter busybar
# https://www.geeksforgeeks.org/progressbar-widget-in-tkinter-python/
# progressbar.stop()

# from tkinter import *
# from tkinter import ttk
# root = Tk()
# progressbar = ttk.Progressbar(orient=HORIZONTAL, length=200, mode='determinate')
# progressbar.pack(side="bottom")
# progressbar.start()
# root.mainloop()


# 鼠标拖拽
