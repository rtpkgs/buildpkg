# -*- coding:utf-8 –*-
# 
# ################################################################################
# @File:   buildpkg.py 
# @Author: liu2guang
# @Date:   2018-09-19 18:07:00
# 
#                _____                                                            
#               /     \                                                           
#               vvvvvvv  /|__/|                                                   
#                  I   /O,O   |                                                   
#                  I /_____   |      /|/|                                         
#                 J|/^ ^ ^ \  |    /00  |    _//|                                 
#                  |^ ^ ^ ^ |W|   |/^^\ |   /oo |                                 
#                   \m___m__|_|    \m_m_|   \mm_|                                 
#
#                                      Quick build rt-thread pkg toolkits         
#                                                           --- liu2guang         
#
# @LICENSE: GPLv3: https://github.com/rtpkgs/buildpkg/blob/master/LICENSE.
#
# Change Logs:
# Date           Author       Notes 
# 2018-09-19     liu2guang    The first version. 
# 2018-09-20     liu2guang    To optimize the implementation. 
#
# ################################################################################

# --------------------------------------------------------------------------------
# Import module 
# --------------------------------------------------------------------------------
import os, sys 
import logging
import json
import argparse
import time
import shutil 
import platform

# --------------------------------------------------------------------------------
# Info and config 
# --------------------------------------------------------------------------------
_BUILDPKG_VERSION      = "v0.2.0" 
_BUILDPKG_AUTHOR       = "liu2guang" 
_BUILDPKG_LICENSE      = "GPLv3" 
_BUILDPKG_RELEASE      =  False

_BUILDPKG_CONTRIBUTORS = {
    "liu2guang" : "https://github.com/liu2guang", 
    "balanceTWK": "https://github.com/balanceTWK" 
}
_BUILDPKG_LOG_FORMAT   = "[%(asctime)s %(filename)s L%(lineno).4d %(levelname)-8s]: %(message)s" 

_BUILDPKG_RUN_LOG_FILE = "buildpkg.log"
_BUILDPKG_PKG_LOG_FILE = os.path.join("packages", "pkglist.log") 

# --------------------------------------------------------------------------------
# Variable: path/log 
# --------------------------------------------------------------------------------
_buildpkg_path                      = None # ./buildpkg/ 
_buildpkg_template_path             = None # ./buildpkg/template/
_buildpkg_packages_path             = None # ./buildpkg/template/
_buildpkg_packages_xxx_path         = None # ./buildpkg/template/xxx
_buildpkg_packages_xxx_example_path = None # ./buildpkg/template/xxx/example
_buildpkg_packages_xxx_scripts_path = None # ./buildpkg/template/xxx/scripts

_run_log = None # run buildpkg log 
_pkg_log = None # create the package record log 

# default config 
_config_default = """
{
    "username"              : "None", 
    "list_ignore_inc"       : [".git", "example", "doc", "test"], 
    "list_ignore_src"       : ["test.c", "example.c"], 

    "template": 
    {
        "github-ci"         : "template-github-ci.txt",
        "kconfig"           : "template-kconfig.txt",
        "package-json"      : "template-package-json.txt",
        "readme"            : "template-readme-rtt.txt",
        "sconscript"        : "template-sconscript.txt", 
        "sconscript-example": "template-sconscript-example.txt"
    },
    "pkg_def_version"       : "v1.0.0", 
    "commit_content"        : "[builpkg] Use the buildpkg tool to quickly build {{pkgname}}'s packages!"
}
"""

_config = None

# --------------------------------------------------------------------------------
# Create log object
# --------------------------------------------------------------------------------
def _create_log(log_name, log_path, level = logging.INFO, console = True):
    log = logging.getLogger(log_name) 
    log.setLevel(logging.DEBUG) 
    format = logging.Formatter(_BUILDPKG_LOG_FORMAT) 

    f = logging.FileHandler(log_path)
    f.setFormatter(format)
    f.setLevel(logging.DEBUG)
    log.addHandler(f) 

    if console == True: 
        c = logging.StreamHandler() 
        c.setFormatter(format) 
        c.setLevel(level) 
        log.addHandler(c) 

    return log 

# --------------------------------------------------------------------------------
# Load confg 
# --------------------------------------------------------------------------------
def _load_config(filename): 
    # 1. check if "filename" file exists
    if os.path.exists(filename) == False: 
        with open(filename, 'w+') as file: 
            file.write(_config_default) 

    # 2. check that "filename" is illegal, Waiting for user processing
    try: 
        with open(filename, 'r') as file:
            json.load(file)
            # json.load(file, encoding='utf-8')
    except ValueError: 
        _run_log.info("\"config.json\" is not illegal, whether to regenerate the default configuration [Y/N]: ")
        option = input() 
        if option == "Y" or option == "y" or option == "YES" or option == "Yes" or option == "yes" or option == "": 
            _run_log.info("Y") 
            with open(filename, 'w+') as file: 
                file.write(_config_default)
        else: 
            _run_log.info("N") 
            _run_log.info("Please modify config.json correctly before running buildpkg") 
            exit(1)

        _run_log.info("Fix the config.json file contents")

    # load config
    global _config

    with open(filename, 'r') as file:
        _config = json.load(file) 
        _run_log.debug("Buildpkg load config: \n" + json.dumps(_config, indent=4)) 

# --------------------------------------------------------------------------------
# Check self(It will load the configuration)
# --------------------------------------------------------------------------------
def _check_self(): 
    # 1. check if the "package" directory exists
    if os.path.exists("packages") == False: 
        os.makedirs  ("packages") 

    # 2. check if the "template" directory exists
    if os.path.exists("template") == False: 
        os.makedirs  ("template") 

    # 3. check if "filename" file exists
    #    check that "filename" is illegal, Waiting for user processing
    #    load config
    _load_config("config.json") 

    # 4. check if License file exists
    if os.path.exists("LICENSE") == False: 
        _run_log.info("Please do not delete the license, otherwise you will not be able to use buildpkg!") 
        exit(1)

# --------------------------------------------------------------------------------
# Analyze the path to use 
# --------------------------------------------------------------------------------
def _analyze_path(package_name): 
    global _buildpkg_path 
    global _buildpkg_template_path 
    global _buildpkg_packages_path 
    global _buildpkg_packages_xxx_path 
    global _buildpkg_packages_xxx_example_path 
    global _buildpkg_packages_xxx_scripts_path 

    _buildpkg_path = os.getcwd() 
    _buildpkg_template_path = os.path.join(_buildpkg_path, "templates") 
    _buildpkg_packages_path = os.path.join(_buildpkg_path, "packages") 
    _buildpkg_packages_xxx_path = os.path.join(_buildpkg_packages_path, package_name) 
    _buildpkg_packages_xxx_example_path = os.path.join(_buildpkg_packages_xxx_path, "example") 
    _buildpkg_packages_xxx_scripts_path = os.path.join(_buildpkg_packages_xxx_path, "scripts") 

    _run_log.debug("Analyze the path to use: ")
    _run_log.debug("- buildpkg_path                     : " + _buildpkg_path)
    _run_log.debug("- buildpkg_template_path            : " + _buildpkg_template_path)
    _run_log.debug("- buildpkg_packages_path            : " + _buildpkg_packages_path)
    _run_log.debug("- buildpkg_packages_xxx_path        : " + _buildpkg_packages_xxx_path)
    _run_log.debug("- buildpkg_packages_xxx_example_path: " + _buildpkg_packages_xxx_example_path)
    _run_log.debug("- buildpkg_packages_xxx_scripts_path: " + _buildpkg_packages_xxx_scripts_path)

# --------------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------------
def main(): 
    # 1. create run and pkg log 
    # 2. parse input args 
    # 3. self check 
    # 4. analyze path
    global _run_log 
    global _pkg_log 
    _run_log = _create_log("run_log", _BUILDPKG_RUN_LOG_FILE, logging.DEBUG if _BUILDPKG_RELEASE == False else logging.INFO, True)
    _pkg_log = _create_log("pkg_log", _BUILDPKG_PKG_LOG_FILE, logging.DEBUG, False)

    _check_self() 

    _analyze_path("xxx")

if __name__ == "__main__":
    main()
