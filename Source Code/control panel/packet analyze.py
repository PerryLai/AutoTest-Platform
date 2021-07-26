#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import sup
import os.path
import shutil
# 設定檔位址
config_file = 'D:\\CN5SW1\\Desktop\\AutoTest Platform\\config.ini'
# 所有從client回傳的資料統整在這個資料夾
testcase_path = sup.config_file(config_file, "Testcase and Analyzation Related Filepath", "testcase_path")
output_icmp_dir = sup.config_file(config_file, "Testcase and Analyzation Related Filepath", "output_icmp_dir")
num_files = len([name for name in os.listdir(testcase_path) if os.path.isdir(os.path.join(testcase_path, name))])

# 初始化所有資料夾
for i in range(num_files-1):
    i=i+1
    output_dir = "%s\\Result%r" %(output_icmp_dir,i)
    shutil.rmtree(output_dir)
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

# 主要分析環節
for i in range(num_files-1):
    i=i+1
    # 回傳以日期為檔名的資料夾
    target_dir = os.listdir("%s\\Result%r\\Result"%(testcase_path,i))[0]
    # 以日期為檔名的資料夾底下有多少packet
    num_packet = sup.file_num("%s\\Result%r\\Result\\%s"%(testcase_path,i,target_dir))
    seq_icmp_file = "%s\\Result%r\\SeqNum.txt"%(sup.config_file(config_file, "Testcase and Analyzation Related Filepath", "output_icmp_file"),i)
    pair_icmp_file = "%s\\Result%r\\Pair.txt"%(sup.config_file(config_file, "Testcase and Analyzation Related Filepath", "output_icmp_file"),i)
    result_icmp_file = "%s\\Result%r\\Result.txt"%(sup.config_file(config_file, "Testcase and Analyzation Related Filepath", "output_icmp_file"),i)
    result_file = "%s\\Result%r\\Final.txt"%(sup.config_file(config_file, "Testcase and Analyzation Related Filepath", "output_icmp_file"),i)
    sup.remove_old_file(seq_icmp_file)
    sup.remove_old_file(pair_icmp_file)
    sup.remove_old_file(result_icmp_file)

    # 對同一包Result下的所有packet分析
    for j in range(num_packet):
        # 純粹回傳packet1~10檔名
        Read_in_File=[f for f in os.listdir("%s\\Result%r\\Result\\%s"%(testcase_path,i,target_dir)) if os.path.isfile(os.path.join("%s\\Result%r\\Result\\%s"%(testcase_path,i,target_dir),f))][j]
        # packet1~10 完整路徑
        Read_in_File_Path = ("%s\\Result%r\\Result\\%s\\%s"%(testcase_path,i,target_dir,Read_in_File))
        # packet1~10 的尺寸
        size = os.path.getsize(Read_in_File_Path)

        Data_Link_Layer_Distination = sup.field_define(Read_in_File_Path,1,12,1)                                                 # 1~12
        Data_Link_Layer_Source = sup.field_define(Read_in_File_Path,13,12,1)                                                     # 13~24
        VLAN_Layer_Type = sup.field_define(Read_in_File_Path,25,4,1)                                                             # 25~28
        if VLAN_Layer_Type == "8100":                                                                                       # 表示 vLan Type 是 802.1Q Virtual LAN
            Network_Layer_ID = sup.field_define(Read_in_File_Path,29,4,1)                                                        # 29~32
            Network_Layer_Type = sup.field_define(Read_in_File_Path,33,4,1)                                                      # 33~36
            if Network_Layer_Type == "0800":                                                                                # 表示 Network Layer Type 是 IPv4
                Network_Layer_Version = sup.field_define(Read_in_File_Path,37,1,1)                                               # 37
                Network_Layer_Header_Length = sup.field_define(Read_in_File_Path,38,1,1)                                         # 38
                Network_Layer_Differentiated_Services_Field = sup.field_define(Read_in_File_Path,39,2,1)                         # 39~40
                Network_Layer_Total_Length = sup.field_define(Read_in_File_Path,41,4,1)                                          # 41~44
                Network_Layer_Identification = sup.field_define(Read_in_File_Path,45,4,1)                                        # 45~48
                Network_Layer_Flags = sup.field_define(Read_in_File_Path,49,4,1)                                                 # 49~52
                Network_Layer_Time_to_live = sup.field_define(Read_in_File_Path,53,2,1)                                          # 53~54                                               
                Protocol = sup.field_define(Read_in_File_Path,55,2,1)                                                            # 55~56
                if Protocol == "01":                                                                                        # 表示 Transport Layer 是 ICMP
                    Protocol_name = "ICMP"
                    Network_Layer_Header_Checksum = sup.field_define(Read_in_File_Path,57,4,1)                                   # 57~60
                    Source = sup.field_define(Read_in_File_Path,61,8,1); Source_IP = sup.ip_addr(Source)                         # 61~68
                    Destination = sup.field_define(Read_in_File_Path,69,8,1); Destination_IP = sup.ip_addr(Destination)          # 69~76
                    Transport_Layer_Type = sup.field_define(Read_in_File_Path,77,2,1)                                            # 77~78
                    Transport_Layer_Code = sup.field_define(Read_in_File_Path,79,2,1)                                            # 79~80
                    Transport_Layer_Checksum = sup.field_define(Read_in_File_Path,81,4,1)                                        # 81~84
                    Transport_Layer_Identifier_BE = sup.field_define(Read_in_File_Path,85,4,1)                                   # 85~88
                    Transport_Layer_Sequence_Number_BE = sup.field_define(Read_in_File_Path,89,4,1)                              # 89~92
                    Transport_Layer_Timestamp = sup.field_define(Read_in_File_Path,93,16,1)                                      # 93~108
                    Data = sup.field_define(Read_in_File_Path,109, int(size)-1,1)                                                # 108~last

                    ### 分析時產出文件的位址 ###
                    output_icmp_file = "%s\\Result%r\\output%r.txt" %(sup.config_file(config_file, "Testcase and Analyzation Related Filepath", "output_icmp_dir"),i,j+1)
                    with open(seq_icmp_file, 'a') as fw:
                        fw.write (Transport_Layer_Sequence_Number_BE+"\n")
                    fw.close()

                    if Transport_Layer_Type == "00":
                        Transport_Layer_Type_Re = "Reply"
                    elif Transport_Layer_Type == "08":
                        Transport_Layer_Type_Re = "Request"

                #elif Protocol == "01":                                                                     # 表示 Transport Layer 是 TCP
        
                with open(output_icmp_file, 'a') as fw:
                    fw.write ("---------- Data Link Layer ----------\n")
                    fw.write ("\n")
                    fw.write ("Data Link Layer Distination: "+Data_Link_Layer_Distination+"\n")
                    fw.write ("Data Link Layer Source: "+Data_Link_Layer_Source+"\n")
                    fw.write ("VLAN Layer Type: "+VLAN_Layer_Type+"\n")
                    fw.write (""+"\n")
                    fw.write ("---------- Network Layer ----------"+"\n")
                    fw.write (""+"\n")
                    fw.write ("Network Layer ID: "+Network_Layer_ID+"\n")
                    fw.write ("Network Layer Type: "+Network_Layer_Type+" ("+Network_Layer_Type+")"+"\n")
                    fw.write ("Network Layer Version: "+Network_Layer_Version+"\n")
                    fw.write ("Network Layer Header Length: "+Network_Layer_Header_Length+"\n")
                    fw.write ("Network Layer Differentiated Services Field: "+Network_Layer_Differentiated_Services_Field+"\n")
                    fw.write ("Network Layer Total Length: "+Network_Layer_Total_Length+"\n")
                    fw.write ("Network Layer Identification: "+Network_Layer_Identification+"\n")
                    fw.write ("Network Layer Flags: "+Network_Layer_Flags+"\n")
                    fw.write ("Network Layer Time to live: "+Network_Layer_Time_to_live+"\n")
                    fw.write ("Protocol: "+Protocol+" ("+Protocol_name+")"+"\n")
                    fw.write ("Network Layer Header Checksum: "+Network_Layer_Header_Checksum+"\n")
                    fw.write ("Source IP: "+Source+" ("+Source_IP+")"+"\n")
                    fw.write ("Destination IP: "+Destination+" ("+Destination_IP+")"+"\n")
                    fw.write (""+"\n")
                    fw.write ("---------- Transport Layer ----------"+"\n")
                    fw.write (""+"\n")
                    fw.write ("Transport Layer Type: "+Transport_Layer_Type+" ("+Transport_Layer_Type_Re+")"+"\n")
                    fw.write ("Transport Layer Code: "+Transport_Layer_Code+"\n")
                    fw.write ("Transport Layer Checksum: "+Transport_Layer_Checksum+"\n")
                    fw.write ("Transport Layer Identifier BE: "+Transport_Layer_Identifier_BE+"\n")
                    fw.write ("Sequence Number: "+Transport_Layer_Sequence_Number_BE+"\n")
                    fw.write ("Transport Layer Timestamp: "+Transport_Layer_Timestamp+"\n")
                    fw.write (""+"\n")
                    fw.write ("Data: "+Data+"\n")  
                    '''
                    print("")
                    mode = input("Please choose one mode(1. Detail information 2. Customization 0. Exit): ")
                    print("")

                    if mode == "1":
                        print ("---------- Data Link Layer ----------")
                        print("")
                        print ("Data Link Layer Distination: "+Data_Link_Layer_Distination)
                        print ("Data Link Layer Source: "+Data_Link_Layer_Source)
                        print ("VLAN Layer Type: "+VLAN_Layer_Type)
                        print("")
                        print ("---------- Network Layer ----------")
                        print("")
                        print ("Network Layer ID: "+Network_Layer_ID)
                        print ("Network Layer Type: "+Network_Layer_Type+" ("+Network_Layer_Type_name+")")
                        print ("Network Layer Version: "+Network_Layer_Version)
                        print ("Network Layer Header Length: "+Network_Layer_Header_Length)
                        print ("Network Layer Differentiated Services Field: "+Network_Layer_Differentiated_Services_Field)
                        print ("Network Layer Total Length: "+Network_Layer_Total_Length)
                        print ("Network Layer Identification: "+Network_Layer_Identification)
                        print ("Network Layer Flags: "+Network_Layer_Flags)
                        print ("Network Layer Time to live: "+Network_Layer_Time_to_live)
                        print ("Protocol: "+Protocol+" ("+Protocol_name+")")
                        print ("Network Layer Header Checksum: "+Network_Layer_Header_Checksum)
                        print ("Source IP: "+Source+" ("+Source_IP+")")
                        print ("Destination IP: "+Destination+" ("+Destination_IP+")")
                        print("")
                        print ("---------- Transport Layer ----------")
                        print("")
                        print ("Transport Layer Type: "+Transport_Layer_Type+" ("+Transport_Layer_Type_Re+")")
                        print ("Transport Layer Code: "+Transport_Layer_Code)
                        print ("Transport Layer Checksum: "+Transport_Layer_Checksum)
                        print ("Transport Layer Identifier BE: "+Transport_Layer_Identifier_BE)
                        print ("Transport Layer Sequence_Number BE: "+Transport_Layer_Sequence_Number_BE)
                        print ("Transport Layer Timestamp: "+Transport_Layer_Timestamp)
                        print("")
                        print ("Data: "+Data)

                    elif mode == "2":
                        location = int(input("Please input first bit: "))
                        length = int(input("Please input length: "))
                        select_offset = field_define(location,length)
                        if location == 1 and length == 12:
                            print (Data_Link_Layer_Distination+ " (Data Link Layer Distination)")
                        elif location == 13 and length == 12:
                            print (Data_Link_Layer_Source+ " (Data Link Layer Source)")
                        elif location == 25 and length == 4:
                            print (VLAN_Layer_Type+ " (VLAN Layer Type)")
                        elif location == 29 and length == 4:
                            print (Network_Layer_ID+ " (Network Layer ID)")
                        elif location == 33 and length == 4:
                            print (Network_Layer_Type+ " (Network Layer Type:"+Network_Layer_Type_name+")")
                        elif location == 37 and length == 1:
                            print (Network_Layer_Version+ " (Network Layer Version)")
                        elif location == 38 and length == 1:
                            print (Network_Layer_Header_Length+ " (Network Layer Header Length)")
                        elif location == 39 and length == 2:
                            print (Network_Layer_Differentiated_Services_Field+ " (Network Layer Differentiated Services Field)")
                        elif location == 41 and length == 4:
                            print (Network_Layer_Total_Length+ " (Network Layer Total Length)")
                        elif location == 45 and length == 4:
                            print (Network_Layer_Identification+ " (Network Layer Identification)")
                        elif location == 49 and length == 4:
                            print (Network_Layer_Flags+ " (Network Layer Flags)")
                        elif location == 53 and length == 2:
                            print (Network_Layer_Time_to_live+ " (Network Layer Time to live)")
                        elif location == 55 and length == 2:
                            print (Protocol+ " (Protocol: "+Protocol_name+")")
                        elif location == 57 and length == 4:
                            print (Network_Layer_Header_Checksum+ " (Network Layer Header Checksum)")
                        elif location == 61 and length == 8:
                            print (Source+ " (Source IP: "+Source_IP+")")
                        elif location == 69 and length == 8:
                            print (Destination+ " (Destination IP: "+Destination_IP+")")
                        elif location == 77 and length == 2:
                            print (Transport_Layer_Type+ " (Transport Layer Type: "+Transport_Layer_Type_Re+")")
                        elif location == 79 and length == 2:
                            print (Transport_Layer_Code+ " (Transport Layer Code)")
                        elif location == 81 and length == 4:
                            print (Transport_Layer_Checksum+ " (Transport Layer Checksum)")
                        elif location == 85 and length == 4:
                            print (Transport_Layer_Identifier_BE+ " (Transport Layer Identifier BE)")
                        elif location == 89 and length == 4:
                            print (Transport_Layer_Sequence_Number_BE+ " (Transport Layer Sequence_Number BE)")
                        elif location == 92 and length == 16:
                            print (Transport_Layer_Timestamp+ " (Transport Layer Timestamp)")
                        elif location == 109 and length == int(size)-1 :
                            print (Data+ " (Data)")
                        else :
                            print (select_offset)

                    elif mode == "0":
                        exit(1)

                    else :
                        print("")
                        print ("Please select again.")
                        print("")
                    '''
    sup.seq_num_pair(seq_icmp_file,pair_icmp_file)                                                                    # check seq nums are pair or not
    sup.uniq(pair_icmp_file,result_icmp_file)                                                                         # delete 重複的 seq num
    print("Testcase %r: %s"%(i,sup.continuous_number(result_icmp_file)))                                              # 判斷是否連續
    sup.field_define(Read_in_File_Path,0,0,0)                                                                         # 關掉檔案讀取