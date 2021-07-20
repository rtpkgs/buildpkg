#-*- encoding: utf-8 -*-
#---------------------------------------------------------------------------------
# @File:   Sconscript for package 
# @Author: liu2guang
# @Date:   2018-09-19 18:07:00(v0.1.0) 
# 
# @LICENSE: GPLv3: https://github.com/rtpkgs/buildpkg/blob/master/LICENSE.
#
#---------------------------------------------------------------------------------
import os
from building import * 
Import('RTT_ROOT')
Import('rtconfig')

#---------------------------------------------------------------------------------
# Package configuration
#---------------------------------------------------------------------------------
PKGNAME = "${pkgname}"
VERSION = "${version}"
DEPENDS = ["PKG_USING_${pkgname_letter}"]

#---------------------------------------------------------------------------------
# Compile the configuration 
#
# SOURCES: Need to compile c and c++ source, auto search when SOURCES is empty
# 
# LOCAL_CPPPATH: Local file path (.h/.c/.cpp)
# LOCAL_CCFLAGS: Local compilation parameter 
# LOCAL_ASFLAGS: Local assembly parameters
# 
# CPPPATH: Global file path (.h/.c/.cpp), auto search when LOCAL_CPPPATH/CPPPATH 
#          is empty # no pass!!!
# CCFLAGS: Global compilation parameter 
# ASFLAGS: Global assembly parameters
#
# CPPDEFINES: Global macro definition
# LOCAL_CPPDEFINES: Local macro definition 
# 
# LIBS: Specify the static library that need to be linked
# LIBPATH: Specify the search directory for the library file (.lib/.a)
#
# LINKFLAGS: Link options
#---------------------------------------------------------------------------------
SOURCES          = [] 

LOCAL_CPPPATH    = [] 
LOCAL_CCFLAGS    = "" 
LOCAL_ASFLAGS    = ""

CPPPATH          = [] 
CCFLAGS          = "" 
ASFLAGS          = ""

CPPDEFINES       = []
LOCAL_CPPDEFINES = []

LIBS             = [] 
LIBPATH          = [] 

LINKFLAGS        = "" 

SOURCES_IGNORE   = []
CPPPATH_IGNORE   = []

#---------------------------------------------------------------------------------
# Feature clip configuration, optional 
#---------------------------------------------------------------------------------
if GetDepend(['XXX_USING_FUN1']) == True: 
    pass

if GetDepend(['XXX_USING_FUN2']) == False:
    pass

#---------------------------------------------------------------------------------
# Compiler platform configuration, optional
#---------------------------------------------------------------------------------
if rtconfig.CROSS_TOOL == "gcc":
    pass

if rtconfig.CROSS_TOOL == "iar":
    pass

if rtconfig.CROSS_TOOL == "keil":
    pass

#---------------------------------------------------------------------------------
# Warning: internal related processing, developers do not modify!!! 
#---------------------------------------------------------------------------------

#---------------------------------------------------------------------------------
# System variables
#---------------------------------------------------------------------------------
objs   = [] 
root   = GetCurrentDir()
ignore = [] 

#---------------------------------------------------------------------------------
# Add relative path support for CPPPATH and LOCAL_CPPPATH
#---------------------------------------------------------------------------------
for index, value in enumerate(CPPPATH): 
    if string.find(value, root) == False: 
        CPPPATH[index] = os.path.join(root, value)

for index, value in enumerate(LOCAL_CPPPATH): 
    if string.find(value, root) == False: 
        LOCAL_CPPPATH[index] = os.path.join(root, value)

if rtconfig.CROSS_TOOL == "gcc": # no test
    for index, value in enumerate(LIBS): 
        if value.startswith("lib") == True: 
            print("Automatic fix the nonstandard lib name, %s -> %s" % 
                (LIBS[index], LIBS[index].lstrip("lib")))
            LIBS[index] = LIBS[index].lstrip("lib")
            
elif rtconfig.CROSS_TOOL == "keil": 
    for index, value in enumerate(LIBS): 
        if value.startswith("lib") == False: 
            print("Automatic fix the nonstandard lib name, %s -> %s" % 
                (LIBS[index], "lib" + LIBS[index]))
            LIBS[index] = "lib" + LIBS[index]

LIBPATH += [root] 

#---------------------------------------------------------------------------------
# Auto search source files and paths, when SOURCES/CPPPATH/LOCAL_CPPPATH are empty 
#---------------------------------------------------------------------------------
_SOURCES_IGNORE = SOURCES_IGNORE + ${list_ignore_src} 
_CPPPATH_IGNORE = CPPPATH_IGNORE + ${list_ignore_inc} 

if not SOURCES: 
    for dirpath, dirnames, filenames in os.walk(root): 
        for name in filenames:
            suffix = os.path.splitext(name)[1]
            if (suffix == '.c' or suffix == '.cpp') and (not name in _SOURCES_IGNORE): 
                SOURCES.append(os.path.join(dirpath, name))

if not LOCAL_CPPPATH and not CPPPATH: 
    for dirpath, dirnames, filenames in os.walk(root): 
        for dir in dirnames:
            abs_path = os.path.join(dirpath, dir)
            if (not ".git" in abs_path) and (not dir in _SOURCES_IGNORE):
                LOCAL_CPPPATH.append(abs_path) 

#---------------------------------------------------------------------------------
# Sub target
#---------------------------------------------------------------------------------
list = os.listdir(root)
if GetDepend(DEPENDS):
    for d in list:
        path = os.path.join(root, d)
        if os.path.isfile(os.path.join(path, 'SConscript')):
            objs = objs + SConscript(os.path.join(d, 'SConscript')) 

#---------------------------------------------------------------------------------
# Main target
#---------------------------------------------------------------------------------
objs = +DefineGroup(name = PKGNAME, src = SOURCES, depend = DEPENDS, 
                   CPPPATH          = CPPPATH, 
                   CCFLAGS          = CCFLAGS, 
                   ASFLAGS          = ASFLAGS, 
                   LOCAL_CPPPATH    = LOCAL_CPPPATH, 
                   LOCAL_CCFLAGS    = LOCAL_CCFLAGS, 
                   LOCAL_ASFLAGS    = LOCAL_ASFLAGS, 
                   CPPDEFINES       = CPPDEFINES, 
                   LOCAL_CPPDEFINES = LOCAL_CPPDEFINES, 
                   LIBS             = LIBS, 
                   LIBPATH          = LIBPATH,
                   LINKFLAGS        = LINKFLAGS)  

Return("objs") 
#---------------------------------------------------------------------------------
# End
#---------------------------------------------------------------------------------
