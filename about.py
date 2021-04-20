import tkinter as tk

def about():
    root = tk.Tk()
    root.title('关于')

    tkWinWidth = 330
    tkWinHeigth = 120
    screenWidth = root.winfo_screenwidth()
    screenHeight = root.winfo_screenheight()
    tkWinXPos = (screenWidth - tkWinWidth) / 2
    tkWinYPos = (screenHeight - tkWinHeigth) / 2
    root.geometry( "%dx%d+%d+%d" % (tkWinWidth,tkWinHeigth,tkWinXPos,tkWinYPos))

    tk.Label(root,text='制作：天雷动漫').grid(row=0,sticky='w')
    tk.Label(root,text='测试环境：python3.9 ffmpeg4.3').grid(row=1,sticky='w')
    tk.Label(root,text='源码：https://github.com/HandierChan').grid(row=2,sticky='w')
    tk.Button(root,text="Close",command=lambda:root.destroy()).grid(row=3,sticky='w')

    root.mainloop()

def howto():
    root = tk.Tk()
    root.title('How to...')

    tkWinWidth = 470
    tkWinHeigth = 170
    screenWidth = root.winfo_screenwidth()
    screenHeight = root.winfo_screenheight()
    tkWinXPos = (screenWidth - tkWinWidth) / 2
    tkWinYPos = (screenHeight - tkWinHeigth) / 2
    root.geometry( "%dx%d+%d+%d" % (tkWinWidth,tkWinHeigth,tkWinXPos,tkWinYPos))

    tk.Label(root,text='1. 最底下 Command 为最终输出命令，受其它参数修改而自动更新，可单独编辑').grid(row=0,sticky='w')
    tk.Label(root,text='2. 最底下 Command 内容不能保存成预设文件').grid(row=1,sticky='w')
    tk.Label(root,text='3. 软件会记录上一次关闭时的历史参数').grid(row=2,sticky='w')
    tk.Label(root,text='4. 输出音频 AAC(CBR) 需要安装编译库 libfdk_aac').grid(row=3,sticky='w')
    tk.Label(root,text='5. "Delay to Video" 目前是无效').grid(row=4,sticky='w')
    tk.Button(root,text="Close",command=lambda:root.destroy()).grid(row=5,sticky='w')

    root.mainloop()

if __name__ == "__main__":
    # about()
    howto()