import os
from building import * 

# get current dir path
cwd = GetCurrentDir()

# init src and inc vars
src = []
inc = []

# add libcsv common include
inc = inc + [cwd]

# add libcsv basic code
src = src + Glob('./*.c')

# add group to IDE project
objs = DefineGroup('${pkgname}-${version}', src, depend = ['${pkgname_letter}_USING_DEMO'], CPPPATH = inc)

Return('objs')
