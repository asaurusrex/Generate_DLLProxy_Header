import os
import subprocess
import sys
#requires use of VS Code Debug or shell with dumpbin in path, also requires you to specify path to DLL as argument
dll_to_proxy = sys.argv[1]

process_out = subprocess.run("dumpbin /exports {} > dll_export.txt".format(dll_to_proxy),shell=True)
#print(type(process_out.stdout))
#print(process_out.stdout)

#list_info = process_out.stdout.decode().split("\r\n")
#print(type(process_out.stdout))
with open('dll_export.txt', 'r+') as f:
    number_functions = 0
    lines = f.readlines()
    for i in range(len(lines)):
        #print("This is a line: {}".format(lines[i]))
        if "number of names" in lines[i]:
            line = lines[i].strip()
            list_words = line.split(" ")
            number_functions = list_words[0]
            #print(number_functions)
        if "ordinal hint RVA" in lines[i]:
            for y in range(int(number_functions)*2 + 1):
                #print(y)
                if lines[i+y] != " " and y!= 0 and lines[i+y].strip() != "Summary":
                    if len(lines[i+y].strip().split(" ")) != 1:
                        #print(lines[i+y].strip().split(" ")[-1])
                        functionname = lines[i+y].strip().split(" ")[-1]
                        ##pragma comment(linker,"/export:SystemFunction002=C:\\Windows\\System32\\cryptbaseGetFileVersionInfoA,@1")
                        string_of_interest = "#pragma comment(linker,\"/export:{0}=C:\\\\Windows\\\\System32\\\\{1}.{2},@{3}\")".format(functionname, dll_to_proxy[:-4], functionname, y)
                        print(string_of_interest)
                if lines[i+y].strip() == "Summary":
                    break

        #if ""
        #print(line)
#print(list_info)
