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
# 2018-09-15     liu2guang    Refactor the entire business layer logic. 

import os, sys
import logging
import argparse
import time
import shutil 
import platform

# buildpkg config
config = {
    "output_path": ".\\packages", 
    "template":{
        "readme"    : ".\\template\\template-readme.txt", 
        "sconscript": ".\\template\\template-sconscript.txt"
    }, 
    "default_version": "v1.0.0", 
    "commit_content": "Use the buildpkg tool to quickly build {{name}}'s packages!"
}

# buildpkg cmd
parser = argparse.ArgumentParser(
    description = "Quick build rt-thread pkg toolkits")
parser.add_argument(  "action" ,       type = str, help = "The action of build package by buildpkg", choices=["make", "update"]) 
parser.add_argument(  "pkgname",       type = str, help = "The package name to be make or update") 
parser.add_argument(  "pkgrepo",       type = str, help = "To make the package from the specified git repository", nargs = "?") 
parser.add_argument("--version", "-v", type = str, help = "The package version to be make or update") 
parser.add_argument("--license", "-l", type = str, help = "The package license to be make or update") 
parser.add_argument("--ci"     , "-c", type = str, help = "The package ci script to be make or update") 
parser.add_argument("--demo"   , "-d", action='store_true', help = "To make demo folder and scons script") 

# Create the log object
def buildpkg_log(name): 
    log = logging.getLogger("buildpkg") 
    log.setLevel(logging.DEBUG)
    format = logging.Formatter("[%(asctime)s %(filename)s L%(lineno).4d %(levelname)-8s]: %(message)s")

    c = logging.StreamHandler()
    f = logging.FileHandler(name + ".log")
    c.setFormatter(format)
    f.setFormatter(format)
    c.setLevel(logging.INFO)
    f.setLevel(logging.DEBUG)
    log.addHandler(c) 
    log.addHandler(f) 

    return log

# Instantiate the log object 
log = buildpkg_log("buildpkg") 

# add readme file
def buildpkg_add_readme(pkgname, version): 
    log.info("add readme.md...") 
    template_readme_path = os.path.join(config["template"]["readme"])
    readme_path = os.path.join(config["output_path"], pkgname, "readme.md") 
    
    log.debug("find readme.md template: \"%s\"" % (template_readme_path)) 
    
    with open(template_readme_path, 'r', encoding='utf-8') as file_in, open(readme_path, 'w+', encoding='utf-8') as file_out: 
        textlist = file_in.readlines()
        for line in textlist: 
            line = line.replace("{{name}}", pkgname)
            line = line.replace("{{version}}", version)
            file_out.write(line)
    log.info("add readme.md success...") 

# add SConscript file
def buildpkg_add_sconscript(pkgname, version): 
    log.info("add SConscript...") 
    template_sconscript_path = os.path.join(config["template"]["sconscript"])
    sconscript_path = os.path.join(config["output_path"], pkgname, "SConscript") 

    log.debug("find SConscript template: \"%s\"" % (template_sconscript_path)) 

    with open(template_sconscript_path, 'r', encoding='utf-8') as file_in, open(sconscript_path, 'w+', encoding='utf-8') as file_out: 
        textlist = file_in.readlines()
        for line in textlist: 
            line = line.replace("{{name}}", pkgname)
            line = line.replace("{{version}}", version)
            line = line.replace("{{date}}", time.strftime("%Y-%m-%d", time.localtime()))
            line = line.replace("{{datetime}}", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            file_out.write(line)
    log.info("add SConscript success...") 

# add git repository
def buildpkg_add_repository(pkgname, pkgrepo): 
    log.info("add git repository...") 
    pwd = os.getcwd()
    repository_path = os.path.join(config["output_path"], pkgname) 
    os.chdir(repository_path) 

    os.system("git init") 
    log.debug("Initialize the git repository success") 

    os.system("git submodule add " + pkgrepo) 
    log.debug("Add the \"%s\" git submodule" % (repository_path)) 

    os.chdir(pwd) 

    log.info("add git repository success...") 

# make package 
def buildpkg_make_package(pkgname, pkgrepo, version, license, ci, demo): 
    log.info("create package...") 
    package_path = os.path.join(config["output_path"], pkgname) 

    # check package directory is exist
    log.info("create \"%s\" directory..." % (package_path)) 
    if os.path.exists(package_path) == True: 
        package_path_backup = package_path + "_backup_" + time.strftime("%y%m%d_%H%M%S", time.localtime()) 
        log.warning("\"%s\" already existed, backup to \"%s\"" %(package_path, package_path_backup))
        os.rename(package_path, package_path_backup)

    # make package directory
    os.makedirs(package_path)
    log.info("\"%s\" directory create success!" % (package_path)) 

    # add SConscript file
    # add Readme.md file
    # init and add repository
    buildpkg_add_readme    (pkgname, version if version != None else config["default_version"])
    buildpkg_add_sconscript(pkgname, version if version != None else config["default_version"])

    if pkgrepo != None: 
        buildpkg_add_repository(pkgname, pkgrepo)

    log.info("create package success...") 

# add the first commit of git repository the first commit
def buildpkg_add_commit(pkgname): 
    log.info("add first commit...") 

    pwd = os.getcwd()
    repository_path = os.path.join(config["output_path"], pkgname) 
    os.chdir(repository_path) 

    # Prevent git from generating warnings: LF will be replaced by CRLF
    if(platform.system() == 'Windows'):
        os.system('git config --global core.autocrlf false') 

    os.system('git add -A') 
    commit_content = config["commit_content"]
    os.system("git commit -m \"" + commit_content.replace("{{name}}", pkgname) + "\"") 

    os.chdir(pwd) 
    log.info("add first commit success...") 

# main run 
if __name__ == "__main__":
    log.info("start run buildpkg...") 
    
    args = parser.parse_args() 
    log.debug(args) 

    if args.action == "make": 
        buildpkg_make_package(args.pkgname, args.pkgrepo, args.version, args.license, args.ci, args.demo)
    elif args.action == "update": 
        log.info("update package...") 

    buildpkg_add_commit(args.pkgname)

    log.info("To complete the building by buildpkg...\n") 
