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

_config    = None
_templates = None
_config_default = """ 
{
    "username"              : "None", 
    "list_ignore_inc"       : [".git", "example", "doc", "test"], 
    "list_ignore_src"       : ["test.c", "example.c"], 

    "templates": 
    {
        "readme_md"         : "template-readme-rtt.txt",
        "sconscript"        : "template-sconscript.txt", 
        "sconscript_example": "template-sconscript-example.txt", 
        "ci_github"         : "template-ci-github.txt",
        "kconfig"           : "template-kconfig.txt",
        "package_json"      : "template-package-json.txt"
    },
    "pkg_def_version"       : "v1.0.0", 
    "commit_content"        : "[builpkg] Use the buildpkg tool to quickly build ${pkgname}'s packages!" 
}
"""

# --------------------------------------------------------------------------------
# Shell cmd 
# --------------------------------------------------------------------------------
_parser = argparse.ArgumentParser(
    description = "Quick build rt-thread pkg toolkits", 
    epilog = "You can find the latest version form https://github.com/rtpkgs/buildpkg"
    )
_parser.add_argument(  "action"   ,        type = str, help = "The action of build package by buildpkg", choices=["make", "update"]) 
_parser.add_argument(  "pkgname"  ,        type = str, help = "The package name to be make or update") 
_parser.add_argument(  "pkgrepo"  ,        type = str, help = "To make the package from the specified git repository", nargs = "?") 
_parser.add_argument("--version"  , "-v" , type = str, help = "The package version to be make or update") 
_parser.add_argument("--license"  , "-l" , type = str, help = "The package license to be make or update, one of: agpl3, apache, bsd2, bsd3, cddl, cc0, epl, gpl2, gpl3, lgpl, mit, mpl") 
_parser.add_argument("--submodule", "-s" , action = "store_true", help = "Add to the repository as a submodule")
_args = _parser.parse_args() 

# --------------------------------------------------------------------------------
# Create log object
# --------------------------------------------------------------------------------
def _create_log(log_name, log_path, level = logging.INFO, console = True):
    path = os.path.dirname(os.path.abspath(log_path))
    if os.path.exists(path) == False: 
        os.makedirs(path) 

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
# Save confg 
# --------------------------------------------------------------------------------
def _save_config(filename): 
    if sys.version_info < (3, 0): 
        with open(filename, "w") as _file:
            _file.write(json.dumps(_config, indent=4)) 
    else: 
        with open(filename, "w", encoding='utf-8') as _file:
            _file.write(json.dumps(_config, indent=4)) 

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
            _run_log.info("Please modify config.json correctly before running buildpkg.") 
            sys.exit("sorry, goodbye!")

        _run_log.info("Fix the config.json file contents.")

    # 3. load config
    global _config
    global _templates

    with open(filename, 'r') as file:
        _config = json.load(file) 
        _templates = _config["templates"]
        _run_log.debug("Buildpkg load config: \n" + json.dumps(_config, indent=4)) 

    # 4. check that the user name is configured 
    if _config["username"] == "None": 
        _run_log.info("Please enter your github username: ") 
        _config["username"] = input()
        if _config["username"] != "" and _config["username"] != "None": 
            _save_config("config.json")

        _run_log.info("Update %s to config.json." % (_config["username"]))

# --------------------------------------------------------------------------------
# Save package confg 
# --------------------------------------------------------------------------------
def _save_package_config(filename, config): 
    if sys.version_info < (3, 0): 
        with open(filename, "w+") as _file:
            _file.write(json.dumps(config, indent=4)) 
    else: 
        with open(filename, "w+", encoding='utf-8') as _file:
            _file.write(json.dumps(config, indent=4)) 

# --------------------------------------------------------------------------------
# Load package confg 
# --------------------------------------------------------------------------------
def _load_package_config(filename): 
    # 1. check if "filename" file exists
    if os.path.exists(filename) == False:  
        return None  

    # 2. check that "filename" is illegal, Waiting for user processing
    try: 
        with open(filename, 'r') as file:
            json.load(file)
    except ValueError: 
        return None 

    # 3. load package config
    with open(filename, 'r') as file:
        _package_config = json.load(file) 

    _run_log.debug("Buildpkg load package config: \n" + json.dumps(_package_config, indent=4)) 

    return _package_config

# --------------------------------------------------------------------------------
# Check self(It will load the configuration)
# --------------------------------------------------------------------------------
def _check_self(): 
    # 1. check if the "package" directory exists
    if os.path.exists("packages") == False: 
        _run_log.info("The [packages] path was not found, auto create directory.") 
        os.makedirs  ("packages") 

    # 2. check if the "template" directory exists
    if os.path.exists("templates") == False: 
        _run_log.info("The [template] path was not found, auto create directory.") 
        os.makedirs  ("templates") 

    # 3. check if "filename" file exists
    #    check that "filename" is illegal, Waiting for user processing
    #    load config
    _load_config("config.json") 

    # 4. check if License file exists
    if os.path.exists("LICENSE") == False: 
        _run_log.info("Please do not delete the license, otherwise you will not be able to use buildpkg!") 
        sys.exit("sorry, goodbye!")

    # 5. check if the library generated by the license is installed
    try:
        import lice
    except ImportError:
        if sys.version_info < (3, 0): 
            os.system("easy_install lice") 
            _run_log.info("The license generation module was not found, Automatic installation by easy_install!") 
        else: 
            os.system("pip install lice") 
            _run_log.info("The license generation module was not found, Automatic installation! by pip.") 

    # 6. check that the template file exists
    global _templates 

    for item, file_name in _templates.items(): 
        file_path = os.path.join(_buildpkg_template_path, str(file_name))
        if os.path.exists(file_path) == False: 
           _run_log.info("The template file [%s] does not exist and exit." % (file_name))  
           sys.exit("sorry, goodbye!")
    
    _run_log.info("To complete self-check, and load config form [config.json] file.")  

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
# Generate file based on the template
# --------------------------------------------------------------------------------
def _generate_file(template_name, target_name, replace_list): 
    if _BUILDPKG_RELEASE == False: 
        _run_log.info("Generate [%s] file form [%s], Replace list is %s." % (target_name, template_name, str(replace_list))) 
    else:
        _run_log.info("Generate [%s] file form [%s]." % (target_name, template_name)) 

    _template_file_path = os.path.join(_buildpkg_template_path, template_name)
    _target_file_path   = os.path.join(_buildpkg_packages_xxx_path, target_name) 

    if sys.version_info < (3, 0): 
        with open(_template_file_path, 'r') as _file_in, open(_target_file_path, 'w+') as _file_out: 
            _contents = _file_in.readlines() 
            for _line in _contents: 
                for (key, value) in replace_list.items(): 
                    _line = _line.replace("${" + key + "}", value) 
                _file_out.write(_line) 
    else: 
        with open(_template_file_path, 'r', encoding='utf-8') as _file_in, open(_target_file_path, 'w+', encoding='utf-8') as _file_out: 
            _contents = _file_in.readlines() 
            for _line in _contents: 
                for (key, value) in replace_list.items(): 
                    _line = _line.replace("${" + key + "}", value) 
                _file_out.write(_line) 

    _run_log.info("Generate [%s] file success." % (target_name)) 

# --------------------------------------------------------------------------------
# Commit package git 
# --------------------------------------------------------------------------------
def _commit_git(pkgname, commit_content): 
    _run_log.info("Start commit the commit.") 
    os.chdir(_buildpkg_packages_xxx_path)

    os.system('git add -A') 
    os.system("git commit -m \"" + commit_content.replace("${pkgname}", pkgname) + "\"") 

    os.chdir(_buildpkg_path) 
    _run_log.info("Commit the commit success.") 

# --------------------------------------------------------------------------------
# Generate package
# --------------------------------------------------------------------------------
def _make_package(pkgname, version = None, license = None): 
    _run_log.info("Start make %s package." % (pkgname)) 

    if version == None: 
        version = _config["pkg_def_version"]

    # Replace the list
    _replace_list = {
        "username"       : _config["username"], 
        "pkgname"        : pkgname, 
        "version"        : version,
        "pkgname_letter" : pkgname.upper(), 
        "list_ignore_inc": str(_config["list_ignore_inc"]), 
        "list_ignore_src": str(_config["list_ignore_src"])
    }

    # 0. Generate package directory
    global _buildpkg_path 
    global _buildpkg_template_path 
    global _buildpkg_packages_path 
    global _buildpkg_packages_xxx_path 
    global _buildpkg_packages_xxx_example_path 
    global _buildpkg_packages_xxx_scripts_path 

    if _BUILDPKG_RELEASE == False: 
        if os.path.exists(_buildpkg_packages_xxx_path) == True: 
            shutil.rmtree(_buildpkg_packages_xxx_path) 
        os.makedirs(_buildpkg_packages_xxx_path) 
    else: 
        if os.path.exists(_buildpkg_packages_xxx_path) == True: 
            _backup_path = _buildpkg_packages_xxx_path + "_backup_" + time.strftime("%y%m%d_%H%M%S", time.localtime()) 
            _run_log.warning("[%s] already existed, backup to [%s]" %(_buildpkg_packages_xxx_path, _backup_path))
            os.rename(_buildpkg_packages_xxx_path, _backup_path) 
        else: 
            os.makedirs(_buildpkg_packages_xxx_path) 
    
    os.makedirs(_buildpkg_packages_xxx_example_path) 
    # os.makedirs(_buildpkg_packages_xxx_scripts_path) 

    # 1. Generate the /readme.md file
    _generate_file(_templates["readme_md"], "readme.md", _replace_list)

    # 2. Generate the /SConscript file
    _generate_file(_templates["sconscript"], "SConscript", _replace_list)

    # 3. Generate the /example/SConscript file
    _example_sconscript_path = os.path.join("example", "SConscript")
    _generate_file(_templates["sconscript_example"], _example_sconscript_path, _replace_list) 

    # 4. Generate the /.travis.yml file
    _templates_ci_script_dir_path = os.path.join(_buildpkg_template_path, "ci_script_github") 

    shutil.copytree(_templates_ci_script_dir_path, _buildpkg_packages_xxx_scripts_path)
    _generate_file(_templates["ci_github"], ".travis.yml", _replace_list) 

    # 5. Generate the /LICENSE file 
    if license != None: 
        _license_file_path = os.path.join(_buildpkg_packages_xxx_path, "LICENSE")
        _run_log.info("Generate [%s LICENSE] file by \"lice module\"." % (license))
        cmd = "lice " + license.lower() + " -f " + _license_file_path + " -o " + _config["username"]
        os.system(cmd) 

        if os.path.exists(_license_file_path) == True: 
            _run_log.info("Generate [%s LICENSE] file success." % (license)) 
        else: 
            _run_log.error("Generate [%s LICENSE] file failed." % (license)) 

    # 6. Save the configuration file when generating the project
    _run_log.info("Save the configuration file to [%s]." % (pkgname)) 
    __buildpkg_config_json_path              = os.path.join(_buildpkg_path, "config.json")
    __buildpkg_packages_xxx_config_json_path = os.path.join(_buildpkg_packages_xxx_path, "config.json")

    _config_save = {}
    _config_save.update(_config)
    _config_save.update(_replace_list) 
    _save_package_config(__buildpkg_packages_xxx_config_json_path, _config_save)

    _run_log.info("Save the configuration success.") 

    # 7. Create git repository
    _run_log.info("Create git repository in [%s]." % (_buildpkg_packages_xxx_path))
    os.chdir(_buildpkg_packages_xxx_path)
    os.system("git init")
    os.chdir(_buildpkg_path)
    _run_log.info("Create git repository success.")

    _run_log.info("Make %s package success." % (pkgname)) 

# --------------------------------------------------------------------------------
# Transplant package
# --------------------------------------------------------------------------------
def _transplant_package(pkgname, pkgrepo, version = None, license = None, submodule = False): 
    global _buildpkg_path
    global _buildpkg_packages_xxx_path 

    _make_package(pkgname, version, license)

    # Todo: check pkgrepo is git addr? 

    # 1.1 Add to the repository as a submodule when Transplant package
    if submodule == True: 
        os.chdir(_buildpkg_packages_xxx_path)
        os.system("git submodule add " + pkgrepo) 
        os.chdir(_buildpkg_path)
        _run_log.debug("Add %s to the %s repository as a submodule." % (pkgrepo, pkgname))  

    # 1.2 Add to the repository as source code when Transplant package  
    else:
        # Todo path???
        _git_name = pkgrepo.split("/")[-1].replace(".git", "") 
        _git_remove_path = os.path.join(_buildpkg_packages_xxx_path, _git_name, ".git") 
        os.chdir(_buildpkg_packages_xxx_path)
        os.system('git clone --progress --recursive ' + pkgrepo) 
        os.system('attrib -r ' + _git_remove_path + '\\*.* /s')
        shutil.rmtree(_git_remove_path) 
        os.chdir(_buildpkg_path)
        _run_log.info("Add %s to the %s repository as source code." % (pkgrepo, pkgname)) 

# --------------------------------------------------------------------------------
# Update package
# --------------------------------------------------------------------------------
def _update_package(pkgname, version = None, license = None): 
    global _config
    global _buildpkg_path 
    global _buildpkg_template_path 
    global _buildpkg_packages_path 
    global _buildpkg_packages_xxx_path 
    global _buildpkg_packages_xxx_example_path 
    global _buildpkg_packages_xxx_scripts_path  
    
    # 1. Read the previously generated configuration 
    _package_config_path = os.path.join(_buildpkg_packages_path, pkgname, "config.json")  
    _package_config = _load_package_config(_package_config_path)

    if _package_config == None: 
        _run_log.error("The [%s] package was not found, exit buildpkg update." % (pkgname))  
        sys.exit("sorry, goodbye!")

    _replace_list = {
        "username"       : _config["username"], 
        "pkgname"        : _package_config["pkgname"], 
        "version"        : _package_config["version"] if version == None else version,
        "pkgname_letter" : _package_config["pkgname_letter"], 
        "list_ignore_inc": str(_config["list_ignore_inc"]), 
        "list_ignore_src": str(_config["list_ignore_src"])
    }

    # 2. Update the /readme.md file
    _generate_file(_templates["readme_md"], "readme.md", _replace_list)

    # 3. Update the /SConscript file
    _generate_file(_templates["sconscript"], "SConscript", _replace_list)    

    # 4. Update the /example/SConscript file
    _example_sconscript_path = os.path.join("example", "SConscript")
    _generate_file(_templates["sconscript_example"], _example_sconscript_path, _replace_list) 

    # 5. Update the /.travis.yml file
    _templates_ci_script_dir_path = os.path.join(_buildpkg_template_path, "ci_script_github") 
    shutil.rmtree(_buildpkg_packages_xxx_scripts_path) 
    shutil.copytree(_templates_ci_script_dir_path, _buildpkg_packages_xxx_scripts_path)
    _generate_file(_templates["ci_github"], ".travis.yml", _replace_list) 

    # 6. Update the /LICENSE file 
    if license != None: 
        _license_file_path = os.path.join(_buildpkg_packages_xxx_path, "LICENSE")
        _run_log.info("Generate [%s LICENSE] file by \"lice module\"." % (license))
        cmd = "lice " + license.lower() + " -f " + _license_file_path + " -o " + _config["username"]
        os.system(cmd) 

        if os.path.exists(_license_file_path) == True: 
            _run_log.info("Generate [%s LICENSE] file success." % (license)) 
        else: 
            _run_log.error("Generate [%s LICENSE] file failed." % (license))       

    # 7. Save the configuration file when generating the project
    _run_log.info("Save the configuration file to [%s]." % (pkgname)) 
    __buildpkg_config_json_path              = os.path.join(_buildpkg_path, "config.json")
    __buildpkg_packages_xxx_config_json_path = os.path.join(_buildpkg_packages_xxx_path, "config.json")

    _config_save = {}
    _config_save.update(_config)
    _config_save.update(_replace_list) 
    _save_package_config(__buildpkg_packages_xxx_config_json_path, _config_save)

    _run_log.info("Save the configuration success.")   

# --------------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------------
def main(): 
    # 1. create log 
    global _run_log 
    global _pkg_log 

    _run_log = _create_log("run_log", _BUILDPKG_RUN_LOG_FILE, logging.DEBUG if _BUILDPKG_RELEASE == False else logging.INFO, True)
    _pkg_log = _create_log("pkg_log", _BUILDPKG_PKG_LOG_FILE, logging.DEBUG, False) 

    _run_log.info("<< Start run buildpkg >>")
    _run_log.info("Version      : %s" % (_BUILDPKG_VERSION))
    _run_log.info("Author       : %s" % (_BUILDPKG_AUTHOR))
    _run_log.info("License      : %s" % (_BUILDPKG_LICENSE))
    _run_log.info("Conteributors: %s" % (str(_BUILDPKG_CONTRIBUTORS)))
    
    # 2. analyze path
    _analyze_path(_args.pkgname)

    # 3. self check
    _check_self() 
    
    # 4. make or transplant package 
    if _args.action == "make": 
        # 4.1. make package 
        if _args.pkgrepo == None:  
            if str(_args.pkgname).find(".git") != -1 or str(_args.pkgname).find("http://") != -1 or str(_args.pkgname).find("https://") != -1: 
                _run_log.error("The %s is a url! Please input package name" % (_args.pkgname))
                sys.exit("sorry, goodbye!")

            _make_package(_args.pkgname, _args.version, _args.license)
            _commit_git(_args.pkgname, _config["commit_content"])
        # 4.2. transplant package
        else: 
            _transplant_package(_args.pkgname, _args.pkgrepo, _args.version, _args.license, _args.submodule)
            _commit_git(_args.pkgname, _config["commit_content"])

        _run_log.info("To complete to make package [%s]!" % (_args.pkgname))
        _pkg_log.info("To complete to make package [%s]!" % (_args.pkgname))
    elif _args.action == "update":  
        _update_package(_args.pkgname, _args.version, _args.license)
        _run_log.info("To complete to update package [%s]!" % (_args.pkgname))
        _pkg_log.info("To complete to update package [%s]!" % (_args.pkgname))

if __name__ == "__main__":
    try:
        main() 
    except:
        _pkg_log.exception(sys.exc_info()) 
        sys.exit("sorry, goodbye!")

