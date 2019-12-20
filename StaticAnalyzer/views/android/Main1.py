#coding=gbk
import os
import zipfile
import sys
import shutil
import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox
import Decode_dex
import Clearup_dex
import get_APIvector
import time
import API_Test_Single
import matplotlib
APIvector_Path = "./API_vector/"
file_path="./apk"
def main(file_path):
    matplotlib.use('Agg')
    #创建工作目录，如果已经存在同名目录，会删除掉同名目录，注意这里
    print("start:",os.path.basename(file_path))
    target_path = file_path[:-4]
    if os.path.exists(target_path):
 #       if tk.messagebox.askyesno("警告","发现存在同名文件夹，即将删除，是否继续"):
        if 1:
            try:
                shutil.rmtree(target_path)
                print("     已删除同名文件夹")
                time.sleep(1)
            except:
                print("     删除失败，已跳过该文件")
                return False
        else:
            print("     跳过该文件")
            return False
    os.mkdir(target_path)

    #读取apk文件并解压缩其中的关键文档
    try:
        z = zipfile.ZipFile(file_path, 'r')
    except:
        return False
    a_name=z.namelist()
    for name in a_name:
        if name == "classes.dex":
            try:
                z.extract(name,target_path)
                print("     成功解压缩class.dex，开始解码")
            except:
                return False
    z.close()

    #调用jar解码文档
    DexPath = os.path.join(target_path,"classes.dex")
    if Decode_dex.Decode(DexPath) == False:
        print("     解码时发生错误，已跳过该文件")
        return False
    else:
        print("     成功解码dex，下面进行整理")

    #整理解码出来的smali
    SmaliPath = DexPath[:-4]

    if not Clearup_dex.clear_up(SmaliPath):
        print("     整理时发生错误，已跳过该文件")
        return False
    else:
        print("     API整理完毕，下面提取向量")

    #从整理好的文档之中获得特征向量
    DextxtPath = SmaliPath + ".txt"
    Target_Path = APIvector_Path + os.path.basename(file_path)[:-4]+".txt"
    print("######################################################################")
    print(file_path)
    print(Target_Path)
    print("######################################################################")
    if not get_APIvector.getAPIVector(DextxtPath,Target_Path):
        print("     提取向量时发生错误，跳过该文件")
        return False
    else:
        print("     向量提取完毕，下面删除临时文件")

    #删除临时文件
    try:
        shutil.rmtree(target_path)
        print("     已删除临时文件夹")
        time.sleep(1)
    except:
        print("     删除失败，已跳过该文件")
        return False

    return True

def output_result(input):
    if input[0]>=input[1]:
        return 0      #"正常程序"
    else:
        return 1      #"恶意程序"

if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    Filepath = filedialog.askopenfilenames(filetypes={('APK', '*.*')},initialdir="./",title="选择一些apk文件以进行后续的操作")
    print("######################################################################")
    print("Firepath:", Filepath)
    ErrorList = []
    for Filename in Filepath:
        if not main(Filename):
            ErrorList.append(Filename)
    print(ErrorList)
    is_good=0
    detection_result = API_Test_Single.detection(APIvector_Path)
    for index,key in enumerate(os.listdir(APIvector_Path)):
        if output_result(detection_result[index])=="恶意程序":
            print("######################################################################")
            print(key[:-4],"程序评分：",detection_result[index],"  参考结果为：",output_result(detection_result[index]))
            print("######################################################################")
            is_good+=1
    if(is_good):
        print("恶意程序")
    else:
        print("良性程序")    