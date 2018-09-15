## buildpkg for rt-thread 

[![release](https://img.shields.io/badge/release-v0.1.0-orange.svg)]()
[![buildpkg](https://img.shields.io/badge/build-pass-blue.svg)]()

工具测试

### 1. 使用方法
```cmd
python .\buildpkg.py make cstring https://github.com/liu2guang/cstring.git --version=v1.0.0 --license=MIT --ci=github --demo
python .\buildpkg.py update cstring --version=v1.1.0 --license=GPLv3 --ci=gitlab --demo
```

### 2. 目前实现功能

| 序号 | 支持功能 | 备注 |
| :--- | :--- | :--- |
| 1 | 支持生成pkg模板+git仓库, 便于用户在此基础上添加自己的代码, 实现pkg的开发 | 自动生成scons脚本+git仓库+readme.md文件+首个commit提交 |
| 2 | 支持通过指定git仓库快速生成pkg, 一般用于纯c项目、兼容RT-Thread支持标准(posix/libc/filesystem)的项目快速构建 | 1号功能+指定仓库的子模块 |
| 3 | 支持日志生成, 便于调试和记录生成pkg的记录 | - |
| 4 | 支持输出自动构建的pkg到指定目录中 | - | 
| 5 | 支持开源协议文件的添加 | 开发中... | 
| 6 | 支持github ci文件的生成 | 开发中... | 
| 7 | 创建demo目录模板及其scons脚本 | 开发中... | 
| 7 | 可配置的移除对于xxxx.c, 支持正则表达式 | 开发中... | 

### 2. 设计功能

功能设计目前不完善, 大家可以提提自己的想法. 以下为待完成功能: 

![待实现功能](https://i.imgur.com/gKehWKr.png) 

总体功能设计图: 

![全部功能](https://i.imgur.com/iGmWMQ1.png)
