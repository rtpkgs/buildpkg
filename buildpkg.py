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
import logging
import argparse
import time
import shutil 

template_readme_name     = "template-readme-v1.0.0.md"
template_sconscript_name = "template-sconscript-v1.0.0"

# buildpkg log
log = logging.getLogger('buildpkg') 
log.setLevel(logging.DEBUG)
format = logging.Formatter('[%(asctime)s %(filename)s L%(lineno).4d %(levelname)-8s]: %(message)s')

# output console
c = logging.StreamHandler()
c.setLevel(logging.INFO)
c.setFormatter(format)
log.addHandler(c)

# output log file
f = logging.FileHandler('buildpkg.log')
f.setLevel(logging.DEBUG)
f.setFormatter(format)
log.addHandler(f)

# buildpkg cmd
parser = argparse.ArgumentParser(
    description = "Quick build rt-thread pkg toolkits")
parser.add_argument(  "pkgname",       type = str, help = "The package name to be created") 
parser.add_argument(  "pkgrepo",       type = str, help = "Build the package from the specified git repository", nargs = "?", default = "None") 
parser.add_argument('--version', '-v', type = str, help = 'The version of package', default = "v1.0.0a") 
parser.add_argument('--output' , '-o', type = str, help = 'The output path of buildpkg package', default = "./") 
parser.add_argument('--license', '-l', type = str, help = 'The license of package', default = "None") 

# add readme file
def buildpkg_add_readme(template, name, version): 
    readme_name = name + "/readme.md"
    with open("template/" + template, 'r', encoding='utf-8') as file_in, open(readme_name, 'w+', encoding='utf-8') as file_out: 
        textlist = file_in.readlines()
        for line in textlist: 
            line = line.replace("[template_name]", name)
            line = line.replace("[template_version]", version)
            file_out.write(line)
            # log.debug(line.rstrip())

    log.info("%s pkg generate readme.md file success!" %(name)) 

# add SConscript file
def buildpkg_add_sconscript(template, name, version):
    sconscript_name = name + "/SConscript"
    with open("template/" + template, 'r', encoding='utf-8') as file_in, open(sconscript_name, 'w+', encoding='utf-8') as file_out: 
        textlist = file_in.readlines()
        for line in textlist: 
            line = line.replace("[template_name]", '"' + name + '"')
            line = line.replace("[template_version]", '"' + version + '"')
            line = line.replace("[template_date]", time.strftime("%Y-%m-%d", time.localtime()))
            line = line.replace("[template_datetime]", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            file_out.write(line)
            # log.debug(line.rstrip())

    log.info("%s pkg generate SConscript file success!" %(name)) 

# add package license
def buildpkg_add_license(name, license): 
    log.info("%s pkg add %s license success!" %(name, license)) 

# add git repository
def buildpkg_add_repository(name, pkgrepo): 
    os.chdir(name) 
    os.system("git init") 
    os.system("git submodule add " + pkgrepo) 
    os.chdir("./../") 
    log.info("%s pkg add %s repo success!" %(name, pkgrepo)) 

# make base package 
def buildpkg_make_base_package(name, pkgrepo, version, license, output): 
    log.info("start make base package(name: %s, version: %s, license: %s, output: %s)..." % (name, version, license, output)) 

    package_path = os.path.join(output, name)

    # check dir or file is exist
    if os.path.exists(name) == True: 
        old_name = name + "_old_" + time.strftime("%Y%m%d%H%M%S", time.localtime()) 
        log.warning("%s dir or file already existed, backup to %s!" %(name, old_name))
        os.rename(name, old_name)

    # make package directory
    os.mkdir(name)
    log.info("%s pkg generate directory success!" % name) 

    # add SConscript file
    # add Readme.md file
    # init and add repository
    buildpkg_add_readme(template_readme_name, name, version)
    buildpkg_add_sconscript(template_sconscript_name, name, version)

    if license != "None": 
        buildpkg_add_license(name, license) 

    if pkgrepo != "None":
        buildpkg_add_repository(name, pkgrepo) 

if __name__ == "__main__":
    args = parser.parse_args() 
    log.info("start run buildpkg...") 
    log.debug(args) 

    # check cmd input para
    if args.pkgrepo == "None": 
        log.debug("No found pkgrepo parameter!") 

    if args.version == "v1.0.0a": 
        log.debug("No found version parameter, set version v1.0.0a!") 

    if args.license == "None": 
        log.debug("No found license parameter!") 

    if args.output == "None": 
        log.debug("No found output parameter, set output path './'!") 

    # make package
    buildpkg_make_base_package(args.pkgname, args.pkgrepo, args.version, args.license, args.output) 
