# -*- coding:utf-8 -*-
##  @package public
#
##  @brief  导出摄像机
##  @author 桔
##  @version 1.0
##  @date  12:13 2020/7/3
#  History:  

import maya.OpenMaya as om
import maya.cmds as cmds
#edo_renameDefualtRenderLayerName()
def J_exportCamera(outType='fbx'):
    selectPath=cmds.internalVar(userWorkspaceDir=True)
    if cmds.optionVar( query= "RecentFilesList")!=0:
        selectPath='/'.join(cmds.optionVar( query= "RecentFilesList")[0].split('/')[0:-1])
    mayaFilePath = cmds.fileDialog2(fileMode=3, caption="open maya file without script",startingDirectory=selectPath)
    if mayaFilePath==None:return
    res=''
    message=''
    bakeFrame=False
    if cmds.confirmDialog( title='到摄像机要烘焙关键帧么？', message='到摄像机要烘焙关键帧么？', button=['要','雅蠛蝶'], dismissString='No' ) ==u'\u8981':
        bakeFrame=True
        
    count = 0
    cmds.progressWindow(title='Doing Nothing',
                    progress=count,
                    status='running: 0%',
                    isInterruptable=True )
    fileCount=0
    for item in os.walk(mayaFilePath[0]):
        for i in item[2]:
            if i.lower().endswith(".mb") or i.lower().endswith(".ma"):
                fileCount+=1
    for item in os.walk(mayaFilePath[0]):
        for i in item[2]:
            count=count+1
            if cmds.progressWindow( query=True, isCancelled=True ) :
                break
            cmds.progressWindow( edit=True, progress=(count*100/fileCount), status=('running: ' + str(count*100/fileCount) + '%' ) )
            cmds.pause( seconds=3 )
            if i.lower().endswith(".mb") or i.lower().endswith(".ma"):    
                mayaFile=(item[0].replace('\\','/')+'/'+i)
                cmds.file(mayaFile,open=True , force=True,ignoreVersion=True,executeScriptNodes=False,o=1, prompt=0)    
                J_excuteExport(mayaFile,outType,bakeFrame)

    cmds.progressWindow(endProgress=1)   
    cmds.confirmDialog( title='执行结果', message="导出完成", button=['好'], dismissString='No' )
def J_excuteExport(fileName,outType,bakeFrame):
    cmds.loadPlugin ( "fbxmaya")
    allCam=cmds.ls(type='camera')
    allCam.remove(u'frontShape')
    allCam.remove(u'perspShape')
    allCam.remove(u'sideShape')
    allCam.remove(u'topShape')
    for cam in allCam:
        if bakeFrame:
            camTransform=cmds.listRelatives(cam,p=True)
            start=cmds.playbackOptions(query=True,minTime=True)
            end=cmds.playbackOptions(query=True,maxTime=True)
            cmds.bakeSimulation( camTransform[0], t=(start,end), sb=1, at=["rx","ry","rz","tx","ty","tz"], hi="below" )
        cmds.select(cam)
        cmds.file((fileName[0:-3]+"_"+cam.replace(':','_')+'.fbx'), force=True ,options= "fbx" ,type ="FBX export" ,es=True )
    
if __name__ == '__main__':
    J_exportCamera()