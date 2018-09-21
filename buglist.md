1. .\buildpkg.exe make https://github.com/Jacajack/liblightmodbus.git -l gpl3 --remove-submodule 异常缓慢

[2018-09-21 12:36:56,970 buildpkg.py L0186 INFO    ]: add package license success.
[2018-09-21 12:36:56,971 buildpkg.py L0189 INFO    ]: add git repository.
Initialized empty Git repository in G:/embedded/GitHub/buildpkg/packages/liblightmodbus/.git/
[2018-09-21 12:36:57,054 buildpkg.py L0193 DEBUG   ]: Initialize the git repository success
Cloning into 'liblightmodbus'...
remote: Enumerating objects: 3, done.
remote: Counting objects: 100% (3/3), done.
remote: Compressing objects: 100% (3/3), done.
remote: Total 6679 (delta 0), reused 1 (delta 0), pack-reused 6676
Receiving objects: 100% (6679/6679), 5.23 MiB | 109.00 KiB/s, done.
Resolving deltas: 100% (4353/4353), done.
Submodule 'doc/html' (https://www.github.com/Jacajack/liblightmodbus.git) registered for path 'doc/html'
Cloning into 'G:/embedded/GitHub/buildpkg/packages/liblightmodbus/liblightmodbus/doc/html'...

过了2 3分钟才开始继续clone

分析了下, 是因为添加子模块的方式不会将子模块的子模块clone update下来, 所以速度有提升, 原本clone就很慢的

2. scons脚本的添加方式感觉在项目中很慢. 