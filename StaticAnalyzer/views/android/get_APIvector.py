#coding=gbk
import os
import traceback
#该脚本将解码后的xml对应的权限写入数据集，每个程序对应数据集中的一个文件，每个文件只有一行，为布尔向量，共有97维，对应权限列表的97个不同权限

def getAPIVector(File_Name,Target_path):

    try:
        PermissionList_Path = "/home/m34/Mobile-Security-Framework-MobSF/StaticAnalyzer/views/android/APIlists.txt"
        PermissionList = []

        for line in open(PermissionList_Path):
            PermissionList.append(line[:-1])
#        print(PermissionList)
#        print(len(PermissionList))
        PermissionTuple = tuple(PermissionList)
        PermissionExistList=[0]*len(PermissionTuple)

        #创建API对应的字典
        PermissionDictionary=dict(zip(PermissionTuple,PermissionExistList))


        #存储得到的API矩阵，每一行对应一个文件
        ResultList=[]
        ResultList.append(PermissionList)

        i=0
        for line_target in open(File_Name,encoding='utf-8'):
            for key in PermissionDictionary:
                if key in line_target:
                    PermissionDictionary[key]+=1

        TempList=[]
        #    TempList.append(apkName)
        for key in PermissionList:
                TempList.append(int(PermissionDictionary[key]>0))
                PermissionDictionary[key]=0
        #        if PermissionDictionary[key]:
        #            print(apkName)
        #            print("具有权限：",key)

        with open(Target_path, 'w') as f:
            f.write(str(TempList))
        #    i+=1
    except(Exception,BaseException) as e:       
        print(e)
        return False

    return True
