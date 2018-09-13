# 
# @File:   buildpkg.py 
# @Author: liu2guang
# @Date:   2018-09-11 18:07:00
#
# @LICENSE: https://github.com/rtpkgs/buildpkg/blob/master/LICENSE.
#
# Change Logs:
# Date           Author       Notes
# 2018-09-11     liu2guang    The first version.

import os, sys
import argparse
import shutil
import stat
import platform 

# 模板仓库地址
rtthread_pkg_example = "https://github.com/rtpkgs/rtthread_pkg_example.git" 

# 声明命令
# pkgname
parser = argparse.ArgumentParser(
    description = 'Quick build rt-thread pkg toolkits')
parser.add_argument('pkgname', type = str, help = 'The package name that needs to be created') 
parser.add_argument('-u', '--url', type = str, help = 'The URL needs to be build into package') 
parser.add_argument('-l', '--license', type = str, help = 'The license for package') 
parser.add_argument('-v', '--version', type = str, help = 'The license for version') 

# 生成工程
def buildpkg_make_project(pkgname, url):

    print("生成工程中...")

    # 检查是否工程已经存在
    if os.path.exists(pkgname) == True:
        # Todo: 这里可以针对已经存在的包名做一个备份处理, 让用户体验感提升!
        print("[警告]: 指定的包名工程已经存在, 请重新输入包名!")
        sys.exit(0)

    # 1. 克隆pkg模板仓库, 并修改名称为需要创建的包名(递归克隆)
    os.system('git clone --progress --recursive ' + rtthread_pkg_example + " " + pkgname) 
    os.chdir(pkgname) 

    # 删除模板仓库中的.git目录, 
    git_removepath = os.path.join(os.getcwd(), '.git')

    if platform.system() == 'Windows':
        print("Windows platform") 
        os.system('attrib -r ' + git_removepath + '\\*.* /s') # 递归修改windows下面的只读文件为可读属性
    elif platform.system() == 'Linux': 
        print("Linux platform") # Todo
    else:
        print("Other platform") # Todo
    
    shutil.rmtree(git_removepath)

    # 2. 初始化仓库
    os.system('git init') 

    # 3. 添加子模块
    os.system('git submodule add ' + url) 

    print("生成工程成功!") 
    
# def buildpkg_update_license()
#    # Todo

# 生成许可证文件
def buildpkg_make_license(license): 
    # Todo
    print("生成许可证中...")
    print("生成许可证失败!") 

# scons脚本文件头
sconscript_head = '''# 
# @File:   SConscript 
# @Author: buildpkg.py 
# @Date:   2018-09-13 10:20:00
#
# @LICENSE: https://github.com/rtpkgs/buildpkg/blob/master/LICENSE.
#
# Change Logs:
# Date           Author       Notes
# 2018-09-11     buildpkg.py  Generate the scons script automatically.

import os
from building import * 

# get current dir path
cwd = GetCurrentDir()

# init src and inc vars
src = []
inc = []

'''

# scons脚本文件末尾
sconscript_tail = '''
# print debug info
# print(name + '-' + version)
# print('PKG_USING_' + name.upper()) 

# add to project 
def make_pkg(f):
    fs = os.listdir(f)
    for f1 in fs:
        tmp_path = os.path.join(f, f1)

        if os.path.isdir(tmp_path):
            make_pkg(tmp_path)

        else: 
            if os.path.splitext(tmp_path)[1] == '.c':
                src.append(tmp_path)
            elif os.path.splitext(tmp_path)[1] == '.h':
                inc.append(f)
            
make_pkg(cwd) 

# add group to IDE project
objs = DefineGroup(name + '-' + version, src, depend = ['PKG_USING_' + name.upper()], CPPPATH = inc)

# traversal subscript
list = os.listdir(cwd)
if GetDepend('PKG_USING_' + name.upper()):
    for d in list:
        path = os.path.join(cwd, d)
        if os.path.isfile(os.path.join(path, 'SConscript')):
            objs = objs + SConscript(os.path.join(d, 'SConscript'))

Return('objs') 
'''

# 生成scons脚本
def buildpkg_make_scons(pkgname, version):
    print("生成scons脚本中...") 

    #os.chdir(pkgname) 

    with open('SConscript', 'w') as f:
        f.write(sconscript_head)
        f.write('name    = \'' + pkgname + '\'\n')
        f.write('version = \'' + version + '\'\n')
        f.write(sconscript_tail)

    print("生成scons脚本成功!") 

def buildpkg_make_commit(pkgname):
    print("提交commit中...") 
    os.system('git add -A') 
    os.system('git commit -m "Quick build ' + pkgname + 'pkg for rt-thread by buildpkg toolkits!"') 

    print("提交commit成功!") 

if __name__ == '__main__':
    args = parser.parse_args() 

    # 1. 生成工程 
    # 2. 生成许可证 
    # 3. 生成pkg scons脚本
    # n. 生成pkg commit提交
    buildpkg_make_project(args.pkgname, args.url) 
    buildpkg_make_license(args.license) 
    buildpkg_make_scons(args.pkgname, args.version)
    buildpkg_make_commit(args.pkgname)
