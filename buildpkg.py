# 
# @File:   buildpkg.py 
# @Author: liu2guang
# @Date:   2018-09-11 18:07:00
#
# @LICENSE: https://github.com/liu2guang/buildpkg/blob/master/LICENSE.
#
# Change Logs:
# Date           Author       Notes
# 2018-09-11     liu2guang    The first version.

import os, sys
import argparse
import shutil
import stat

# 模板仓库地址
rtthread_pkg_example_repo = "https://github.com/liu2guang/rtthread_pkg_example.git"

# 声明命令
# pkgname
parser = argparse.ArgumentParser(
    description = 'Quick build rt-thread pkg toolkits')
parser.add_argument('pkgname', type = str, help = 'The package name that needs to be created') 
parser.add_argument('-u', '--url', type = str, help = 'The URL needs to be build into package') 

# 创建工程
def buildpkg_mkdir(args):

    # 检查是否工程已经存在
    if os.path.exists(args.pkgname) == True:

        # Todo: 这里可以针对已经存在的包名做一个备份处理, 让用户体验感提示!
        # print("[警告]: 指定的包名工程已经存在, 请重新输入包名!")
        sys.exit(0)

    # os.mkdir(args.pkgname) 
    # os.chdir(args.pkgname) 

    # 1. 克隆pkg模板仓库, 并修改名称为需要创建的包名
    cmd = 'git clone --no-tags ' + rtthread_pkg_example_repo + " " + args.pkgname
    os.system(cmd) 
    os.chdir(args.pkgname) 

    # 删除模板仓库中的.git目录, Todo: 这里可能在Mac和linux有问题
    git_removepath = os.path.join(os.getcwd(), '.git')
    os.system('attrib -r ' + git_removepath + '\\*.* /s')
    shutil.rmtree(git_removepath)

    # 2. 初始化仓库
    cmd = 'git init' 
    os.system(cmd) 

    # 3. 添加子模块
    cmd = 'git submodule add ' + args.url
    os.system(cmd) 

    # 4. Todo: 提交commit为第一版本
    cmd = 'git add -A'
    os.system(cmd) 
    cmd = 'git commit -m "Quick build ' + args.pkgname + 'pkg for rt-thread."'
    print(cmd)
    os.system(cmd) 

if __name__ == '__main__':

    # 解析buildpkg输出参数
    args = parser.parse_args() 

    # 打印输入参数字典 
    # print("[提示]: 用户输入的参数列表: " + str(args))

    # 创建工程
    buildpkg_mkdir(args) 
