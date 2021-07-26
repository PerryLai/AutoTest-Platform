#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import sup
import os
import shutil
import telnetlib
### Config Setting ###
# 設定檔位址
config_file = 'D:\\CN5SW1\\Desktop\\AutoTest Platform\\config.ini'
# 所有要在client做測試前設定的資訊，一次輸入一組
ip_list_file = sup.config_file(config_file, "Testcase and Analyzation Related Filepath", "ip_list_file")
# 要寄到client自動測試的檔案們
set_netns_net0 = sup.config_file(config_file, "Client", "set_netns_net0")
set_netns_net1 = sup.config_file(config_file, "Client", "set_netns_net1")
main = sup.config_file(config_file, "Client", "main")
test_program_path = sup.config_file(config_file, "Client", "test_program_path")
#壓縮
zip_dir_srcPath = sup.config_file(config_file, "Control Panel", "zip_dir_srcPath")
zip_dir_dstname = sup.config_file(config_file, "Control Panel", "zip_dir_dstname")
# 所有從client回傳的資料統整在這個資料夾
testcase_path = sup.config_file(config_file, "Testcase and Analyzation Related Filepath", "testcase_path")
# 把所有寫死的參數全部改成從config抓取變數，包含set_netns.sh(另寫一支子程式呼叫set_netns並修改參數)
HOST_net0 = sup.config_file(config_file, "Control Panel", "HOST_net0")
USER_net0 = sup.config_file(config_file, "Control Panel", "USER_net0")
PASSWORD_net0 = sup.config_file(config_file, "Control Panel", "PASSWORD_net0")
PORT_net0 = sup.config_file(config_file, "Control Panel", "PORT_net0")
HOST_net1 = sup.config_file(config_file, "Control Panel", "HOST_net1")
USER_net1 = sup.config_file(config_file, "Control Panel", "USER_net1")
PASSWORD_net1 = sup.config_file(config_file, "Control Panel", "PASSWORD_net1")
PORT_net1 = sup.config_file(config_file, "Control Panel", "PORT_net1")
### Client address ###
main_client = sup.config_file(config_file, "Control Panel", "main_client")
source_code_client = sup.config_file(config_file, "Control Panel", "source_code_client")
### Server address ###
main_local = sup.config_file(config_file, "Control Panel", "main_local")
source_code_local = sup.config_file(config_file, "Control Panel", "source_code_local")
result_client=sup.config_file(config_file, "Control Panel", "result_client") #/home/pi/Desktop/Result.zip
result_local=sup.config_file(config_file, "Control Panel", "result_local") #D:\CN5SW1\Desktop\\Result
### 解壓縮路徑 ###
unzip_dir_srcName = sup.config_file(config_file, "Control Panel", "unzip_dir_srcName")
unzip_dir_dstPath = sup.config_file(config_file, "Control Panel", "unzip_dir_dstPath")
### 外部程式 ###
analyze = sup.config_file(config_file, "Control Panel", "analyze")
cle = sup.config_file(config_file, "Control Panel", "cle")
### Switch ###
HOST = sup.config_file(config_file, "switch", "HOST")
USER = sup.config_file(config_file, "switch", "USER")
PASSWORD = sup.config_file(config_file, "switch", "PASSWORD")
PORT = sup.config_file(config_file, "switch", "PORT")
CP_normal = sup.config_file(config_file, "switch", "CP_normal")
CP_fixed = sup.config_file(config_file, "switch", "CP_fixed")
CP_forbidden = sup.config_file(config_file, "switch", "CP_forbidden")
PC1_vlan = sup.config_file(config_file, "switch", "PC1_vlan")
PC1_normal = sup.config_file(config_file, "switch", "PC1_normal")
PC1_fixed = sup.config_file(config_file, "switch", "PC1_fixed")
PC1_forbidden = sup.config_file(config_file, "switch", "PC1_forbidden")
PC2_vlan = sup.config_file(config_file, "switch", "PC2_vlan")
PC2_normal = sup.config_file(config_file, "switch", "PC2_normal")
PC2_fixed = sup.config_file(config_file, "switch", "PC2_fixed")
PC2_forbidden = sup.config_file(config_file, "switch", "PC2_forbidden")

# 設定fw
# 呼叫cle子程式
cmd = '''D: & \
cd %s & \
cle.exe spi erase all & \
cle.exe spi update fw_config.bin & \
''' %cle
os.system(cmd)

# 設定switch
sup.switch_portset(HOST,USER,PASSWORD,PORT,'1',CP_normal,CP_fixed,CP_forbidden) # switch 對 CP default 的 vlan 就是 1 
sup.switch_portset(HOST,USER,PASSWORD,PORT,PC1_vlan,PC1_normal,PC1_fixed,PC1_forbidden)
sup.switch_portset(HOST,USER,PASSWORD,PORT,PC2_vlan,PC2_normal,PC2_fixed,PC2_forbidden)

# 設定 set_netns
f = open(ip_list_file,'r')
lines = f.readlines()

num_files = len([name for name in os.listdir(testcase_path) if os.path.isdir(os.path.join(testcase_path, name))])

# 初始化所有資料夾
for i in range(num_files-1):
    i=i+1
    Result_dir = "%s\\testcase\\Result%r" %(sup.config_file(config_file, "Control Panel", "AutoTest_Path"),i)
    shutil.rmtree(Result_dir)
    if not os.path.isdir(Result_dir):
        os.mkdir(Result_dir)

# 主程式
for i in range(len(lines)):
    if i%2 == 0:                                       
        sup.alter_ip_to_config(config_file, ip_list_file, i) # 抓ip_list的資料到config
        sup.alter_config_to_set_netns_net0(config_file, set_netns_net0) # 抓config的資料到set_netns_net0
        sup.alter_config_to_set_netns_net1(config_file, set_netns_net1) # 抓config的資料到set_netns_net1
        sup.alter(test_program_path, 0, 0, config_file, "Client", "test_program") # 抓config的資料到test_program.txt
        # 將檔案壓縮存到特定位址
        sup.zip_dir(zip_dir_srcPath,zip_dir_dstname)
        # 將壓縮檔案傳送到client並進行指令控制
        sup.paramiko_net0(HOST_net0,USER_net0,PASSWORD_net0,PORT_net0,source_code_local,source_code_client)
        sup.paramiko_net1(HOST_net1,USER_net1,PASSWORD_net1,PORT_net1,source_code_local,source_code_client)
        sup.paramiko_link(HOST_net0,USER_net0,PASSWORD_net0,PORT_net0,main_local,main_client,source_code_local,source_code_client,result_client,result_local,i)
        # 解壓縮client蒐集到的封包
        sup.unzip_dir("%s\\Result%s.zip" %(sup.config_file(config_file, "Control Panel", "unzip_dir_srcName"),int(i/2)+1),"%s\\Result%s"%(sup.config_file(config_file, "Control Panel", "unzip_dir_dstPath"),int(i/2)+1))

# 呼叫fork子程式
commandText = "python "+'"' + analyze + '"'
os.system(commandText)
