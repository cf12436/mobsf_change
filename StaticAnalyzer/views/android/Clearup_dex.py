#coding=utf-8
import os

#本脚本将FilePath下的smali文件中的API调用命令整理到TargetPath中对应APK的文本文档中，降低后面查找的时间


def clear_up(FilePath):
    TargetString = ";->"
    try:
        newPath = FilePath
        newName = FilePath + ".txt"
        f = open(newName,"w",encoding='utf-8')
        for root, dirs, files in os.walk(newPath, topdown=False):
            for name in files:
                for line in open(os.path.join(root, name),'r', encoding='UTF-8'):
                    if TargetString in line:
                        f.write(line)
        f.close()
    except:
        return False
    return True