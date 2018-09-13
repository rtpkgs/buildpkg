#coding:utf-8
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
debug = False
github_name = "xxx"
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

    with open('SConscript', 'w') as file:
        file.write(sconscript_head)
        file.write('name    = \'' + pkgname + '\'\n')
        file.write('version = \'' + version + '\'\n')
        file.write(sconscript_tail)

    print("生成scons脚本成功!") 

github_ci_tail = '''language: c

notifications:
  email: true

git:
  depth: 3

before_script:
  - sudo apt-get update 
  - "sudo apt-get -qq install gcc-multilib libc6:i386 libgcc1:i386 gcc-4.6-base:i386 libstdc++5:i386 libstdc++6:i386 libsdl-dev || true" 
  - "[ $RTT_TOOL_CHAIN = 'sourcery-arm' ] && curl -s https://launchpadlibrarian.net/287101520/gcc-arm-none-eabi-5_4-2016q3-20160926-linux.tar.bz2 | sudo tar xjf - -C /opt && export RTT_EXEC_PATH=/opt/gcc-arm-none-eabi-5_4-2016q3/bin && /opt/gcc-arm-none-eabi-5_4-2016q3/bin/arm-none-eabi-gcc --version || true" 
  
  - git clone --depth=3 --branch=master https://github.com/RT-Thread/rt-thread.git ../RT-Thread 
  
  - export RTT_ROOT=/home/travis/build/$USER_NAME/RT-Thread
  - "[ x$RTT_CC == x ] && export RTT_CC='gcc' || true"

  - sudo mkdir $RTT_ROOT/bsp/$RTT_BSP/packages 
  - sudo cp    /home/travis/build/$USER_NAME/$REPO_NAME/script/script_bspcfg $RTT_ROOT/bsp/$RTT_BSP/rtconfig.h
  - sudo cp    /home/travis/build/$USER_NAME/$REPO_NAME/script/script_scons  $RTT_ROOT/bsp/$RTT_BSP/packages/SConscript
  - sudo cp -r /home/travis/build/$USER_NAME/$REPO_NAME                      $RTT_ROOT/bsp/$RTT_BSP/packages/$REPO_NAME

script:
  - scons -C $RTT_ROOT/bsp/$RTT_BSP

env:
'''

# 生成github ci脚本: 默认使用rt1050或者qeum-a9的bsp中测试
def buildpkg_make_github_ci(pkgname): 
    print("生成github ci脚本中...") 

    with open('.travis.yml', 'w') as file:
        file.write(github_ci_tail)
        file.write("  - RTT_BSP='imxrt1052-evk' RTT_TOOL_CHAIN='sourcery-arm' USER_NAME='" + github_name + "' REPO_NAME='" + pkgname + "'")
    
    print("生成github ci脚本!") 

readme_tail = '''# libcsv pkg #

[![Build Status](https://travis-ci.org/liu2guang/libcsv.svg?branch=master)](https://travis-ci.org/liu2guang/libcsv)
[![release](https://img.shields.io/badge/Release-v3.0.4-orange.svg)](https://github.com/liu2guang/libcsv/releases)
---

## 1、介绍
## 2、获取方式
## 3、使用说明 
## 4、注意事项
## 5、许可方式
## 6、联系方式 & 感谢
* 感谢：[liu2guang](https://github.com/liu2guang) 本pkg使用buildpkg工具快速自动构建! 
* 维护：[github_name]().
'''

# 生成readme文件, 这里生成的代码是GB2312
def buildpkg_make_readme(pkgname):
    print("生成readme中...") 
    with open('readme.md', 'w') as file:
        file.write(readme_tail)
    print("生成readme成功!") 

# 生成pkg commit提交
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
    if debug == True: 
        print("启动调试模式...")
        # buildpkg_make_project(args.pkgname, args.url) 
        # buildpkg_make_license(args.license) 
        # buildpkg_make_scons(args.pkgname, args.version)
        # buildpkg_make_github_ci(args.pkgname)
        buildpkg_make_readme(args.pkgname)
        # buildpkg_make_commit(args.pkgname)
        exit(0)
    
    buildpkg_make_project(args.pkgname, args.url) 
    buildpkg_make_license(args.license) 
    buildpkg_make_scons(args.pkgname, args.version)
    buildpkg_make_github_ci(args.pkgname)
    buildpkg_make_readme(args.pkgname)
    buildpkg_make_commit(args.pkgname)
