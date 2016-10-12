import tkinter as tk
import os
from tkinter.filedialog import askdirectory
import csv
import chardet
from dict import *
import tkinter.messagebox as messagebox
import time
import threading
import random


## 按运营商拆分
# 在act函数处理文件时，负责把匹配结果写入到结果文件中
def write2(line,csvfile2,csvfile3,csvfile4,csvfile5):
    try:
        n=0
        str2=''
        str3=''
        str4=''
        str5=''
        ilen=len(line)
        while n<ilen-1:
            explode=','
            if n==ilen-2:
                explode="\r\n"
            if str(line[ilen-1])=='移动':
                #str2=str(line[0])+',"'+str(line[n])+'"'+explode
                str2=str2+str(line[n])+explode
            if str(line[ilen-1])=='联通':
                #str3=str(line[0])+',"'+str(line[n])+'"'+explode
                str3=str3+str(line[n])+explode
            if str(line[ilen-1])=='电信':
                #str4=str(line[0])+',"'+str(line[n])+'"'+explode
                str4=str4+str(line[n])+explode
            if str(line[ilen-1])=='无法匹配':
                #str5=str(line[0])+',"'+str(line[n])+'"'+explode
                str5=str5+str(line[n])+explode
            n=n+1
        csvfile2.write(str2)
        csvfile3.write(str3)
        csvfile4.write(str4)
        csvfile5.write(str5)
    except Exception as err:
        messagebox.showinfo('错误信息',str(err))
# 主体业务流程
def act(file1,file2,file3,file4,file5,pathf='./',patht='./'):        #file1为输入文件,其他为输出文件
    try:
        global c
        info=''
        codedetect='gbk'
        try:
            fileobj = open(pathf+'/'+file1,'r',encoding=codedetect)
            fileobj.read()
            fileobj.close()
        except Exception as err:
            codedetect='utf-8'
        try:
            fileobj = open(pathf+'/'+file1,'r',encoding=codedetect)
            fileobj.read()
            fileobj.close()
        except Exception as err:
            #messagebox.showinfo('错误信息','文件'+pathf+'/'+file1+'编码有误，请使用文件编码转换服务进行转码')
            return '文件'+pathf+'/'+file1+'编码有误，请使用文件编码转换服务进行转码'
        csvfile1 = open(pathf+'/'+file1,'r',newline='',encoding=codedetect)
        csvfile2=open(patht+'/'+file2,'w',newline='')
        csvfile3=open(patht+'/'+file3,'w',newline='')
        csvfile4=open(patht+'/'+file4,'w',newline='')
        csvfile5=open(patht+'/'+file5,'w',newline='')
        cont1=csv.reader(csvfile1)
        items_num=0
        for items in cont1:
            if c>int(len(items)-1):
                csvfile1.close()
                csvfile2.close()
                csvfile3.close()
                csvfile4.close()
                csvfile5.close()
                os.remove(patht+'/'+file2)
                os.remove(patht+'/'+file3)
                os.remove(patht+'/'+file4)
                os.remove(patht+'/'+file5)
                info=info+'您输入的列号在文件'+file1+'超出范围'+"\r\n"
                return info
            else:
                if items[c][-11:].isdigit():
                    m=4
                    flag=0          #标记是否匹配上，0为未匹配，1为已匹配上
                    while m>0:
                        city=int(items[c][0:m])
                        if city in dic.keys():
                            items.append(dic[city])
                            flag=1
                            write2(items,csvfile2,csvfile3,csvfile4,csvfile5)
                            #break
                        m=m-1
                    if flag==0:
                        items.append('无法匹配')
                        write2(items,csvfile2,csvfile3,csvfile4,csvfile5)
                else:           #号码不是纯数字则打印异常
                    if items_num>0:
                        info=info+'文件'+file1+'第 '+str(items_num+1)+' 行有异常，请检查!'+"\r\n"
                items_num+=1
        csvfile1.close()
        csvfile2.close()
        csvfile3.close()
        csvfile4.close()
        csvfile5.close()
        return info
    except Exception as err:
        #messagebox.showinfo('错误信息',str(err))
        info=str(err)
        return info
# 浏览文件夹并调用act函数进行处理
def scan_dir(pathf,patht):
    try:
        st['state']='disabled'
        warn.grid(row=11,column=0,sticky=tk.W)
        files=[]
        files_all=os.listdir(pathf)
        for file in files_all:
            if (file[-4:]=='.csv' or file[-4:]=='.txt') and file[-8:]!='_new.txt' and file[-8:]!='_new.csv' and os.path.isfile(pathf+'/'+file):
                files.append(file)
        fcount=0
        readme=open(patht+'/'+'readme.txt','a',encoding='gbk',newline='')
        for f in files:
            if (f[-4:]=='.txt' or f[-4:]=='.csv') and f[-8:]!='_new.txt' and file[-8:]!='_new.csv':
                file1=f
                file2=f[:-4]+'_移动_new'+f[-4:]
                file3=f[:-4]+'_联通_new'+f[-4:]
                file4=f[:-4]+'_电信_new'+f[-4:]
                file5=f[:-4]+'_未识别_new'+f[-4:]
                info=act(file1,file2,file3,file4,file5,patht=patht,pathf=pathf)
                if len(info)>0:
                    readme.write(time.strftime('%Y-%m-%d %H:%M:%S')+"\r\n"+info)
                    if len(info)<500:
                        messagebox.showinfo('错误信息', info+'详情已保存到输出文件夹中的readme.txt文件中')
                    else:
                        messagebox.showinfo('错误信息', '您的业务在处理过程中遇到错误,'+'详情已保存在输出文件夹中的readme.txt文件中')
                else:
                    flist2.insert(tk.END,file2)
                    flist2.insert(tk.END,file3)
                    flist2.insert(tk.END,file4)
                    flist2.insert(tk.END,file5)
                fcount+=1
        readme.close()
        if fcount==0:
            messagebox.showinfo('错误信息','抱歉，未检测到文件，请检查文件夹')
    except Exception as err:
        messagebox.showinfo('错误信息',str(err))
    finally:
        st['state']='active'
        warn.grid_forget()


## 国际号码处理
# 对文件的第一行单独处理
def write1_1(line,csvfile2):
    try:
        n=0
        str2=''
        ilen=len(line)
        while n<ilen:
            explode=','
            str2=str2+'"'+str(line[n])+'"'+explode
            n=n+1
        str2=str2+'国家代码,'+'国家'+'\n'
        csvfile2.write(str2)
    except Exception as err:
        messagebox.showinfo('错误信息',str(err))
# 对文件的其他行统一处理
def write2_1(line,csvfile2):
    try:
        n=0
        str2=''
        ilen=len(line)
        while n<ilen:
            explode=','
            if n==ilen-1:
                explode='\n'
            str2=str2+'"'+str(line[n])+'"'+explode
            n=n+1
        csvfile2.write(str2)
    except Exception as err:
        messagebox.showinfo('错误信息',str(err))
#主体业务流程
def act_1(file1,file2):        #file1为输入文件,file2为输出文件
    try:
        global c
        info_1=''
        codedetect='gbk'
        try:
            fileobj = open(file1,'r',encoding=codedetect)
            fileobj.read()
            fileobj.close()
        except Exception as err:
            codedetect='utf-8'
        try:
            fileobj = open(file1,'r',encoding=codedetect)
            fileobj.read()
            fileobj.close()
        except Exception as err:
            messagebox.showinfo('错误信息','文件'+file1+'编码有误，请使用文件编码转换服务进行转码')
            return 0
        csvfile1 = open(file1,'r',encoding=codedetect,newline='')
        csvfile2=open(file2,'w',encoding='UTF-8-SIG',newline='')
        cont1=csv.reader(csvfile1)
        items_num=0
        for items in cont1:
            if c>len(items)-1:
                info_1='您输入的列号在文件'+file1+'中超出索引'+"\r\n"
                return info_1
            if items_num==0:
                write1_1(items,csvfile2)
            else:
                if items[c][0:5].isdigit():
                    m=4
                    flag=0          #标记是否匹配上，0为未匹配，1为已匹配上
                    while m>0:
                        city=int(items[c][0:m])
                        if city in dic_1.keys():
                            items.append(city)
                            items.append(dic_1[city])
                            flag=1
                            write2_1(items,csvfile2)
                            break
                        m=m-1
                    if flag==0:
                        items.append('无法匹配')
                        items.append('无法匹配')
                        write2_1(items,csvfile2)
                else:           #号码不是纯数字或不足4位，抛出异常
                    info_1=info_1+'文件'+file1+'第 '+str(items_num+1)+' 行有异常，请检查!'+"\n"
            items_num+=1
        csvfile2.close()
        csvfile1.close()
        flist2.insert(tk.END,file2.split('/')[-1])
    except Exception as err:
        messagebox.showinfo('错误信息',str(err))
        info_1=''
    finally:
        return info_1
#浏览文件夹
def scan_dir_1(pathf,patht):
    try:
        files=[]
        files_all=os.listdir(pathf)
        for file in files_all:
            if (file[-4:]=='.csv' or file[-4:]=='.txt') and file[-8:]!='_new.csv' and file[-8:]!='_new.txt' and os.path.isfile(pathf+'/'+file):
                files.append(file)
        fcount=0
        for f in files:
            if f[-4:]=='.csv' and f[-8:]!='_new.csv':
                #print('正在处理文件'+f)
                file1=f
                file2=f[:-4]+'_new.csv'
                info_1=act_1(pathf+'/'+file1,patht+'/'+file2)
                if len(info_1)>0:
                    readme=open(patht+'/'+'readme.txt','a',encoding='gbk',newline='')
                    readme.write(time.strftime('%Y-%m-%d %H:%M:%S')+"\r\n"+info_1)
                    readme.close()
                    if len(info_1)<500:
                        messagebox.showinfo('错误信息', info_1+'详情已保存在输出文件夹中的readme.txt文件中')
                    else:
                        messagebox.showinfo('错误信息', '您的业务在处理过程中遇到错误,'+'详情已保存在输出文件夹中的readme.txt文件中')
    except Exception as err:
        messagebox.showinfo('错误信息',str(err))
    finally:
        st['state']='active'
        warn.grid_forget()
## 号码归属地匹配
# 对文件filef进行归属地匹配，并写入到文件filet
def city(filef,filet):
    try:
        global c
        filet_f=filet
        codedetect='gbk'
        try:
            fileobj = open(filef,'r',encoding=codedetect)
            fileobj.read()
            fileobj.close()
        except Exception as err:
            codedetect='utf-8'
        try:
            fileobj = open(filef,'r',encoding=codedetect)
            fileobj.read()
            fileobj.close()
        except Exception as err:
            #messagebox.showinfo('错误信息','文件'+filef+'编码有误，请使用文件编码转换服务进行转码')
            return '文件'+filef+'编码有误，请使用文件编码转换服务进行转码'
        fencoding=codedetect
        filet=open(filet,'w',encoding=fencoding,newline='')
        
        with open(filef,'r',encoding=fencoding) as file:
            for line in file:
                if filef[-4:]=='.csv':
                    explode=','
                else:
                    explode="\t"
                line_new=line
                line=line.split(explode)
                if c>len(line)-1:
                    filet.close()
                    os.remove(filet_f)
                    return 0
                if line[c][0:7].isdigit():
                    pnumsub=int(line[c][0:7])
                    if dic_2.get(pnumsub) is not None:
                        filet.write(line_new[0:-1]+explode+dic_2.get(pnumsub)[0]+"\r\n")
                    else:
                        filet.write(line_new[0:-1]+explode+'无法识别'+"\r\n") 
                else:
                    filet.write(line_new[0:-1]+explode+'无法识别'+"\r\n") 
        filet.close()
        return ''
    except Exception as err:
        #messagebox.showinfo('错误信息',str(err))
        return str(err)
# 浏览文件夹
def addcity(dir1,dir2):
    try:
        global c
        city_d={}
        c=column.get() or 1
        c=int(c)-1
        files=os.listdir(dir1)
        flist2.insert(tk.END,'+++++++++++++++++++++')
        flist2.insert(tk.END,'新生成文件列表:'+"\n")
        st['state']='disabled'
        warn.grid(row=11,column=0,sticky=tk.W)
        nfnum=1
        for f in files:
            if (f[-4:]=='.csv' or f[-4:]=='.txt') and f[-8:]!='_new.csv' and f[-8:]!='_new.txt' and os.path.isfile(dir1+'/'+f):
                city_d[f]=city(filef=dir1+'/'+f,filet=dir2+'/'+f[0:-4]+'_new'+f[-4:])
                #print(city_d[f])
                #threading.Thread(target=city,args=(dir1+'/'+f,dir2+'/'+f[0:-4]+'_new.csv')).start()
                if len(city_d[f])==0:
                    flist2.insert(tk.END,'    '+str(nfnum)+'.'+f[0:-4]+'_new'+f[-4:]+"\n")
                else:
                    messagebox.showinfo('错误信息',city_d[f])
        '''
        info_str=''
        nfnum=1
        for info in city_d:
            #print(info)
            if len(city_d[info])!=0:
                info_str=info_str+'您输入的列号在文件'+str(info)+'中超出总列数'+"\r\n"
            else:
                nfnum+=1
        if len(info_str)>0:#有文件超出索引
            messagebox.showinfo('处理信息',info_str)
        '''
    except Exception as err:
        messagebox.showinfo('错误信息',str(err))
    finally:
        st['state']='active'
        warn.grid_forget()
## 大文件拆分
# 浏览文件夹
def scan_dir_2(pathf,patht):
    try:
        global c
        filelist=os.listdir(pathf)
        if (not ',' in c) or (not c.replace(',','').isdigit()):
            messagebox.showinfo('错误信息','您输入的拆分条数格式错误，请重新输入')
            st['state']='active'
            warn.grid_forget()
            return 0
        for f in filelist:
            if (f[-4:]=='.csv' or f[-4:]=='.txt') and os.path.isfile(pathf+'/'+f):
                filecode='gbk'
                try:
                    fileobj = open(pathf+'/'+f,'r',encoding=filecode)
                    fileobj.read()
                    fileobj.close()
                except Exception as err:
                    filecode='utf-8'
                try:
                    fileobj = open(pathf+'/'+f,'r',encoding=filecode)
                    fileobj.read()
                    fileobj.close()
                except Exception as err:
                    messagebox.showinfo('错误信息','文件'+pathf+'/'+str(f)+'编码有误，请使用文件编码转换服务进行转码')
                    continue
                handle(filef=pathf+'/'+f,filet=patht+'/'+f,code=filecode)
    except Exception as err:
        messagebox.showinfo('错误信息',str(err))
    finally:
        st['state']='active'
        warn.grid_forget()
# 读文件，在handle函数中调用
def readfile(start=0,stop=0,file='final.csv',code='gbk'):
    try:
        dic=[]
        with open(file,'r',encoding=code,newline='') as f:
            c=0
            for line in f:
                if stop==0:
                    if c>start:
                        dic.append(line)
                else:
                    if c in range(start,stop):
                        dic.append(line)
                c=c+1
        return dic
    except Exception as err:
        messagebox.showinfo('错误信息',str(err))
# 对文件filef进行拆分，每次取内容时都掉用readfile函数
def handle(filef,filet,code='gbk'):
    try:
        global c
        temp=c
        li=list(temp.split(','))
        stp=0
        for i in range(0,len(li)+1):
            if i==0:
                stp=stp+int(li[i])
                dic=readfile(start=0,stop=stp,file=filef,code=code)
                f=open(filet+'_'+str(i)+'_'+li[i]+'条'+filef[-4:],'w',encoding=code,newline='')
                f.writelines(dic)
                f.close()
                flist2.insert(tk.END,'    '+filet.split('/')[-1]+'_'+str(i)+'_'+li[i]+'条'+filef[-4:])
            elif i<len(li):
                stp=stp+int(li[i])
                dic=readfile(start=stp-int(li[i]),stop=stp,file=filef,code=code)
                f=open(filet+'_'+str(i)+'_'+li[i]+'条'+filef[-4:],'w',encoding=code,newline='')
                f.writelines(dic)
                f.close()
                flist2.insert(tk.END,'    '+filet.split('/')[-1]+'_'+str(i)+'_'+li[i]+'条'+filef[-4:])
            else:
                dic=readfile(start=stp-1,stop=0,file=filef,code=code)
                f=open(filet+'_'+str(i)+'_'+str(len(dic))+'条'+filef[-4:],'w',encoding=code,newline='')
                f.writelines(dic)
                f.close()
                flist2.insert(tk.END,'    '+filet.split('/')[-1]+'_'+str(i)+'_'+str(len(dic))+'条'+filef[-4:])
    except Exception as err:
        messagebox.showinfo('错误信息',str(err))
## 生成随机号码
def createpnums(patht):
    try:
        global c
        nums=c
        t=time.time()
        fname=patht+'/'+str(t)+'_new.txt'
        start_all=[]
        for start in dic_2:
            start_all.append(start)
        start_all_len=len(start_all)
        file=open(str(fname),'w',encoding='gbk',newline='')
        for i in range(0,int(nums)):
            file.write(str(start_all[random.randint(0,start_all_len)-1])+str(random.randint(1000,9999))+"\r\n")
        file.close()
        flist2.insert(tk.END,str(t)+'_new.txt')
        st['state']='active'
        warn.grid_forget()
    except Exception as err:
        messagebox.showinfo('错误信息',str(err))
    finally:
        st['state']='active'
        warn.grid_forget()
## 文件编码转换
# 把文件filef的编码转换成codet，并输出到文件filet中
def changecode(filef,filet,codet):
    try:
        f1=open(filef,'rb')
        bt=f1.read()
        f1.close()
        fencoding=chardet.detect(bt).get('encoding')
        f2=open(filet,'wb')
        f2.write(bt.decode(fencoding).encode('utf-8').decode('utf-8').encode(codet))
        f2.close()
        ftname=filet.split('/')[len(filet.split('/'))-1]
        flist2.insert(tk.END,ftname)
    except Exception as wrr:
        messagebox.showinfo('错误信息','文件'+filet+'转换出错，请检查!')
    finally:
        st['state']='active'
        warn.grid_forget()
# 浏览文件夹
def scan_dir_3(pathf,patht,code):
    try:
        files=os.listdir(pathf)
        for f in files:
            if os.path.isfile(pathf+'/'+f) and (f[-4:]=='.csv' or f[-4:]=='.txt'):
                changecode(filef=pathf+'/'+f,filet=patht+'/'+f[0:-4]+'_new'+str(f[-4:]),codet=code)
    except Exception as err:
        messagebox.showinfo('错误信息',str(err))
    finally:
        st['state']='active'
        warn.grid_forget()
def area_part(filef,patht):
    pass

def scan_dir_4(pathf,patht):
    global c
    try:
        files=os.listdir(pathf)
        if len(files)<1:
            messagebox.showinfo('错误信息','输入文件夹内没有符合条件的文件')
            st['state']='active'
            warn.grid_forget()
            return 0;
        newfile=[]
        for f in files:
            if os.path.isfile(pathf+'/'+f) and (f[-4:]=='.csv' or f[-4:]=='.txt'):
                with open(pathf+'/'+f) as ff:
                    for line in ff:
                        numstr = line.split()
                        if len(numstr)>0:
                            numstr=numstr[0]
                        if numstr.isdigit() and len(numstr) == 11:
                            area = dic_2.get(int(numstr[0:7]))
                            if area is not None:
                                area=area[0].split(' ')[0]
                            else:
                                area='无法匹配'
                            newfile.append(area+f[-4:])
                            with open(patht + '/' + area + f[-4:], 'a', encoding='utf-8', newline=None) as ft:
                                ft.write(str(numstr) + "\n")
                        else:
                            with open(patht + '/无法匹配' + f[-4:], 'a', encoding='utf-8', newline=None) as ft:
                                ft.write(str(numstr) + "\n")
        newfile=set(newfile)
        for nf in newfile:
            flist2.insert(tk.END,nf)
    except Exception as err:
        messagebox.showinfo('错误信息',str(err))
    finally:
        st['state']='active'
        warn.grid_forget()


def sel1():
    try:
        global dir1
        global files
        dir1=tk.filedialog.askdirectory()
        flist.delete(0,tk.END)
        files=os.listdir(dir1)
        if len(files)==0:
            messagebox.showinfo('错误信息', '您选择的输入文件夹为空,请重新选择')
        else:
            flist.insert(tk.END,'输入文件夹:'+"\n")
            flist.insert(tk.END,'    '+dir1)
            flist.insert(tk.END,'+++++++++++++++++++++')
            flist.insert(tk.END,'文件列表:'+"\n")
            n=1
            for i in files:
                flist.insert(tk.END,'    '+str(n)+'.'+' '+i)
                n+=1
    except Exception as err:
        flist.insert(tk.END,'未选择文件夹')
def sel2():
    try:
        global dir2
        dir2=tk.filedialog.askdirectory()
        flist2.delete(0,tk.END)
        flist2.insert(tk.END,'输出文件夹:'+"\n")
        flist2.insert(tk.END,'    '+dir2)
        flist2.insert(tk.END,'+++++++++++++++++++++')
        files2=os.listdir(dir2)
        if len(files2)!=0:
            flist2.insert(tk.END,'已有文件列表:'+"\n")
            n2=1
            for i in files2:
                flist2.insert(tk.END,'    '+str(n2)+'.'+' '+i.split('/')[-1])
                n2+=1
    except Exception as err:
        flist2.delete(0,tk.END)
        flist2.insert(tk.END,'未选择文件夹')
def start():
    if (column.get().isdigit() and (v.get()==1 or v.get()==2 or v.get()==3 or v.get()==5 or v.get()==7)) or (column.get().replace(',','') and v.get()==4) or (v.get()==6):
        try:
            global c
            global dir1
            global dir2
            c=column.get()
            if v.get()<5:
                global files
                if len(files)==0:
                    messagebox.showinfo('错误信息', '您选择的输入文件夹为空，请重新选择')
                    return 0
            if v.get()==1:
                try:
                    c=column.get() or 3
                    c=int(c)-1
                    flist2.insert(tk.END,'+++++++++++++++++++++')
                    flist2.insert(tk.END,'新生成文件列表:'+"\n")
                    threading.Thread(target=scan_dir_1,args=(dir1,dir2)).start()
                    st['state']='disabled'
                    warn.grid(row=11,column=0,sticky=tk.W)
                except Exception as err:
                    st['state']='active'
                    warn.grid_forget()
                    messagebox.showinfo('错误信息',str(err))

            if v.get()==2:
                try:
                    c=column.get() or 1
                    c=int(c)-1
                    flist2.insert(tk.END,'+++++++++++++++++++++')
                    flist2.insert(tk.END,'新生成文件列表:'+"\n")
                    threading.Thread(target=scan_dir,args=(dir1,dir2)).start()
                    warn.grid_forget()
                except Exception as err:
                    messagebox.showinfo('错误信息',str(err))

            if v.get()==3:
                try:
                    threading.Thread(target=addcity,args=(dir1,dir2)).start()
                except Exception as err:
                    st['state']='active'
                    warn.grid_forget()
                    messagebox.showinfo('错误信息',str(err))
            if v.get()==4:
                try:
                    st['state']='disabled'
                    warn.grid(row=11,column=0,sticky=tk.W)
                    flist2.insert(tk.END,'+++++++++++++++++++++')
                    flist2.insert(tk.END,'新生成文件列表:'+"\n")
                    threading.Thread(target=scan_dir_2,args=(dir1,dir2)).start()
                except Exception as err:
                    st['state']='active'
                    warn.grid_forget()
                    messagebox.showinfo('错误信息',str(err))
            if v.get()==5:
                try:
                    st['state']='disabled'
                    warn.grid(row=11,column=0,sticky=tk.W)
                    flist2.insert(tk.END,'+++++++++++++++++++++')
                    flist2.insert(tk.END,'新生成文件列表:'+"\n")
                    threading.Thread(target=createpnums,args=(dir2,)).start()
                except Exception as err:
                    st['state']='active'
                    warn.grid_forget()
                    messagebox.showinfo('错误信息',str(err))
            if v.get()==6:
                try:
                    st['state']='disabled'
                    warn.grid(row=11,column=0,sticky=tk.W)
                    flist2.insert(tk.END,'+++++++++++++++++++++')
                    flist2.insert(tk.END,'新生成文件列表:'+"\n")
                    threading.Thread(target=scan_dir_3,args=(dir1,dir2,opts.get())).start()
                except Exception as err:
                    st['state']='active'
                    warn.grid_forget()
                    messagebox.showinfo('错误信息',str(err))
            if v.get()==7:
                try:
                    st['state']='disabled'
                    warn.grid(row=11,column=0,sticky=tk.W)
                    flist2.insert(tk.END,'+++++++++++++++++++++')
                    flist2.insert(tk.END,'新生成文件列表:'+"\n")
                    threading.Thread(target=scan_dir_4,args=(dir1,dir2)).start()
                except Exception as err:
                    st['state']='active'
                    warn.grid_forget()
                    messagebox.showinfo('错误信息',str(err))
        except Exception as err:
            st['state']='active'
            warn.grid_forget()
            messagebox.showinfo('Message',str(err))
    else:
        messagebox.showinfo('警告信息', '您输入的参数不合法，请重新输入')
def pick():
    if v.get()==1:
        column.delete(0,tk.END)
        column.insert(0,'3')
        column_text.set('请输入列号')
        column.grid(row=9,column=0,sticky=tk.W,padx=5)
        options.grid_forget()
    if v.get()==2:
        column.delete(0,tk.END)
        column.insert(0,'1')
        column_text.set('请输入列号')
        column.grid(row=9,column=0,sticky=tk.W,padx=5)
        options.grid_forget()
    if v.get()==3:
        column.delete(0,tk.END)
        column.insert(0,'1')
        column_text.set('请输入列号')
        column.grid(row=9,column=0,sticky=tk.W,padx=5)
        options.grid_forget()
    if v.get()==4:
        column_text.set('请输入拆分行数')
        column.delete(0,tk.END)
        column.grid(row=9,column=0,sticky=tk.W,padx=5)
        column.insert(0,'100,100,100')
        options.grid_forget()
    if v.get()==5:
        column.delete(0,tk.END)
        column.insert(0,'1000')
        column_text.set('请输入号码个数')
        options.grid_forget()
        column.grid(row=9,column=0,sticky=tk.W,padx=5)
        #column_label.grid_forget()
    if v.get()==6:
        column_text.set('请选择输出编码')
        column.grid_forget()
        #column_label.grid_forget()
        options.grid(row=9,column=0,sticky=tk.W,padx=5)
    if v.get()==7:
        column.delete(0,tk.END)
        column.insert(0,'1')
        column_text.set('请输入列号')
        column.grid(row=9,column=0,sticky=tk.W,padx=5)
        options.grid_forget()


root = tk.Tk()
root.resizable(False,False)
frame1=tk.Frame(root,bg='#87ceeb')
frame2=tk.Frame(root)
frame3=tk.Frame(root,bg='#87ceeb')
frame1.grid(row=0,column=0,padx=2,pady=2)
frame2.grid(row=0,column=1,padx=2,pady=2)
frame3.grid(row=0,column=2,padx=2,pady=2)
root.title('号码魔方')
sc1=tk.Scrollbar(frame1,orient="vertical")
sc1.grid(row=1,column=1,sticky='ns')
sc2=tk.Scrollbar(frame1,orient="horizontal")
sc2.grid(row=2,columnspan=1,sticky='ew')
flist=tk.Listbox(frame1,width=28,height=20,bg='#F0F8FF',yscrollcommand=sc1.set,xscrollcommand=sc2.set)
flist.grid(row=1,column=0,pady=0,padx=1)
sc1.configure(command=flist.yview)
sc2.configure(command=flist.xview)
tk.Button(frame1, text='请选择输入路径',fg='black',command=sel1,width=12,height=1).grid(row=0,column=0,pady=10)
#这里是选择服务的按钮
tk.Label(frame2,text='请选择服务',width=12,height=1).grid(row=0,column=0)
v=tk.IntVar()
v.set(1)
tk.Radiobutton(frame2,text='国际号码标识',variable=v,value=1,command=pick).grid(sticky=tk.W)
tk.Radiobutton(frame2,text='按运营商拆分',variable=v,value=2,command=pick).grid(sticky=tk.W)
tk.Radiobutton(frame2,text='归属城市标识',variable=v,value=3,command=pick).grid(sticky=tk.W)
tk.Radiobutton(frame2,text='大文件拆分',variable=v,value=4,command=pick).grid(sticky=tk.W)
tk.Radiobutton(frame2,text='生成随即号码',variable=v,value=5,command=pick).grid(sticky=tk.W)
tk.Radiobutton(frame2,text='文件编码转换',variable=v,value=6,command=pick).grid(sticky=tk.W)
tk.Radiobutton(frame2,text='按归属省拆分',variable=v,value=7,command=pick).grid(sticky=tk.W)
column_text=tk.StringVar()
column_text.set('请输入列号')
column_label=tk.Label(frame2,textvariable=column_text,width=13,height=1)
column_label.grid(row=8,column=0,sticky=tk.W)
column=tk.Entry(frame2,width=13)
column.grid(row=9,column=0,sticky=tk.W,padx=5)
column.insert(0,'3')

opts = tk.StringVar()
opts.set("UTF-8")
options= tk.OptionMenu(frame2, opts, "UTF-8", "GBK")
warn=tk.Label(frame2,text='正在处理'+"\n"+'请勿操作...',width=13,height=2,fg='red')
st=tk.Button(frame2, text='开始转换',fg='black', command=start,justify=tk.LEFT)
st.grid(pady=10)
tk.Button(frame3, text='请选择输出路径',fg='black', command=sel2,justify=tk.LEFT).grid(pady=10)
sc1_1=tk.Scrollbar(frame3,orient="vertical")
sc1_1.grid(row=1,column=1,sticky='ns')
sc2_1=tk.Scrollbar(frame3,orient="horizontal")
sc2_1.grid(row=2,columnspan=1,sticky='ew')
flist2=tk.Listbox(frame3,width=28,height=20,bg='#F0F8FF',yscrollcommand=sc1_1.set,xscrollcommand=sc2_1.set)
flist2.grid(row=1,column=0,pady=0,padx=1)
sc1_1.configure(command=flist2.yview)
sc2_1.configure(command=flist2.xview)

root.mainloop()

