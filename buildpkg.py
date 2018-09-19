# -*- coding:utf-8 –*-
# @File:   buildpkg.py 
# @Author: liu2guang
# @Date:   2018-09-19 18:07:00
#
# @LICENSE: https://github.com/rtpkgs/buildpkg/blob/master/LICENSE.
#
# Change Logs:
# Date           Author       Notes 
# 2018-09-19     liu2guang    The first version. 

import os, sys 
import logging
import json
import argparse
from urllib.parse import urlparse
import time

_BUILDPKG_VERSION    = "v0.2.0_alpha"
_BUILDPKG_LOG_FORMAT = "[%(asctime)s %(filename)s L%(lineno).4d %(levelname)-8s]: %(message)s"

# run logger
def _buildpkg_run_log(file): 
    log = logging.getLogger("buildpkg") 
    log.setLevel(logging.DEBUG)
    format = logging.Formatter(_BUILDPKG_LOG_FORMAT)

    c = logging.StreamHandler()
    f = logging.FileHandler(file)
    c.setFormatter(format)
    f.setFormatter(format)
    c.setLevel(logging.DEBUG)
    f.setLevel(logging.DEBUG)
    log.addHandler(c) 
    log.addHandler(f) 

    return log

# pkg logger
def _buildpkg_pkg_log(file): 
    log = logging.getLogger("pkglist") 
    log.setLevel(logging.DEBUG)
    format = logging.Formatter(_BUILDPKG_LOG_FORMAT)

    f = logging.FileHandler(file)
    f.setFormatter(format)
    f.setLevel(logging.DEBUG)
    log.addHandler(f) 

    return log

# Init log 
run_log = _buildpkg_run_log("buildpkg.log") 
pkg_log = _buildpkg_pkg_log("packages/pkglist.log") # Todo 这里判断下linux和mac下有没有问题. 

# Load buildpkg config 
# Todo: try
with open("config.json", 'r') as f:
    _config = json.load(f)
    run_log.debug("Read config: \n" + json.dumps(_config, indent=4)) 

# buildpkg cmd
parser = argparse.ArgumentParser(
    description = "Quick build rt-thread pkg toolkits")
parser.add_argument(  "action"   ,        type = str, help = "The action of build package by buildpkg", choices=["make", "update"]) 
parser.add_argument(  "pkgname"  ,        type = str, help = "The package name to be make or update", nargs = "?") 
parser.add_argument(  "pkgrepo"  ,        type = str, help = "To make the package from the specified git repository", nargs = "?") 
parser.add_argument("--version"  , "-v" , type = str, help = "The package version to be make or update") 
parser.add_argument("--license"  , "-l" , type = str, help = "The package license to be make or update, one of: agpl3, apache, bsd2, bsd3, cddl, cc0, epl, gpl2, gpl3, lgpl, mit, mpl") 
parser.add_argument("--remove-submodule", action='store_true', help = "Remove the submodule of repository")

# generate file
def _buildpkg_generate_file(template_name, pkgname, target_path, replace_list): 
    run_log.debug("Replace the list is " + str(replace_list)) 

    template_path = os.path.join("template", template_name)
    target_file_path = os.path.join("packages", pkgname, target_path) 
    print(template_path)
    print(target_file_path)

    if sys.version_info < (3, 0): 
        with open(template_path, 'r') as file_in, open(target_file_path, 'w+') as file_out: 
            textlist = file_in.readlines()
            for line in textlist: 
                for (key, value) in replace_list.items():
                    line = line.replace("{{" + key + "}}", value) 
                file_out.write(line) 
    else: 
        with open(template_path, 'r', encoding='utf-8') as file_in, open(target_file_path, 'w+', encoding='utf-8') as file_out: 
            textlist = file_in.readlines()
            for line in textlist: 
                for (key, value) in replace_list.items():
                    line = line.replace("{{" + key + "}}", value) 
                file_out.write(line) 

    run_log.info("add success...") 

# buildpkg cmd
def _buildpkg_make_package(pkgname = None, pkgrepo = None, version = _config["default_version"], license = None, remove_submodule = False): 
    if version == None: 
        version = _config["default_version"]

    if pkgname == None and pkgrepo == None: 
        run_log.error("Please input pkgname or pkgrepo while you make package!") 
        run_log.error("Stop make package!\n") 
        exit(1); 

    # 2. buildpkg make cstring 
    # 3. buildpkg make https://github.com/liu2guang/cstring.git
    if pkgname != None and pkgrepo == None: 
        if pkgname.endswith(".git") == True: 
            package_name = pkgname.split("/")[-1].replace(".git", "") 
            pkgrepo = pkgname
        else: 
            package_name = pkgname

    # 4. buildpkg make cstring https://github.com/liu2guang/cstring.git 
    elif pkgname != None and pkgrepo != None: 
        package_name = pkgname

    run_log.info("The package name is %s." % (package_name)) 
    run_log.info("The package repo addr is %s." % (pkgrepo)) 

    package_path = os.path.join("packages", package_name) 
    #pwd = os.getcwd()           # 记录当前路径, /
    #os.chdir(repository_path)   # 进入package/xxxx

    # check package directory is exist 
    if os.path.exists(package_path) == True: 
        package_path_backup = package_path + "_backup_" + time.strftime("%y%m%d_%H%M%S", time.localtime()) 
        run_log.warning("\"%s\" already existed, backup to \"%s\"" %(package_path, package_path_backup))
        os.rename(package_path, package_path_backup)

    os.makedirs(package_path) 
    run_log.info("\"%s\" directory create success!" % (package_path)) 

    # 必须添加的: 
    # 1. readme文件
    # 2. 根目录scons脚本
    # 3. demo目录 + 空xxx_demo.c文件 + scons脚本
    # 4. 添加ci脚本 + ci配置文件
    # 5. 迁移时将仓库做成子模块
    # 6. 添加.git仓库, 添加第一个提交
    
    # 可选的: 
    # 1. 移除子模块修改成源码方式
    username = _config["username"]

    # 1. add readme.md 
    replace_list = {"username": username, "pkgname": package_name, "version": version}
    _buildpkg_generate_file(_config["template"]["readme"], package_name, "readme.md", replace_list) 

    # 2. add demo 
    example_path = os.path.join(package_path, "example") 
    os.makedirs(example_path) 

    replace_list = {"pkgname": package_name, "version": version, "pkgname_letter": package_name.upper()}
    _buildpkg_generate_file(_config["template"]["sconscript-example"], package_name, os.path.join("example", "SConscript"), replace_list) 

if __name__ == "__main__":
    run_log.info("start run buildpkg") 
    run_log.info("current buildpkg version %s" % (_BUILDPKG_VERSION)) 

    # parse and print input args 
    args = parser.parse_args() 
    run_log.debug(args) 

    # build package
    if args.action == "make": 
        run_log.info("The package is being built.") 
        _buildpkg_make_package(args.pkgname, args.pkgrepo, args.version, args.license, args.remove_submodule) 
        run_log.info("To completion package build.\n") 
    elif args.action == "update": 
        run_log.info("The package is being update.") 
        run_log.info("To completion package update.\n") 
        pass
