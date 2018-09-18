<div align="center">
  <h1>buildpkg</h1>

  <div align="center">
    <a href="https://github.com/rtpkgs/buildpkg">
      <img src="https://img.shields.io/travis/liu2guang/Lua2RTT/master.svg?style=flat-square" alt="travis-ci" />
    </a>
    <a href="https://github.com/rtpkgs/buildpkg/stargazers">
      <img src="https://img.shields.io/github/stars/rtpkgs/buildpkg.svg?style=flat-square" alt="stargazers" />
    </a>
  </div>

  <div align="center">
    <a href="https://github.com/rtpkgs/buildpkg">
      <img src="https://img.shields.io/github/downloads/rtpkgs/buildpkg/total.svg?style=flat-square" alt="downloads" />
    </a>
    <a href="https://github.com/rtpkgs/buildpkg/blob/master/LICENSE">
        <img src="https://img.shields.io/github/license/rtpkgs/buildpkg.svg?style=flat-square" alt="license" />
    </a>
    <a href="https://github.com/rtpkgs/buildpkg/releases">
      <img src="https://img.shields.io/github/release/rtpkgs/buildpkg.svg?style=flat-square" alt="Github All Releases" />
    </a>
  </div>

  <p align="center">Quick build rt-thread pkg toolkits | 快速构建rt-thread pkg工具集</p>
</div>

## 简介 ([English](/readme.en.md)) 

buildpkg是用于生成RT-Thread package的快速构建工具.

本项目重点关注package的快速生成和开源仓库的快速迁移, 为开发Rt-Thread的package的开发者提供便利. 如果您喜欢该项目觉得该项目不错的话, 请赏赐一个星星, 星星就是更新的动力! 

| 序号  | 支持功能 | 描述 |
| :--- | :--- | :--- |
| 1 | 构建package | 创建指定名称package, 自动添加readme/版本号/github ci脚本/demo/开源协议文件 |
| 2 | 迁移开源仓库 | 从指定git仓库构建package, 自动添加readme/版本号/github ci脚本/demo/开源协议文件, 但是迁移的仓库需要用户自己按照实际情况修改, 对于纯软件仓库且兼容RT-Thread支持标准可以无需修改 |
| 3 | 更新package | 生成package后修复部分错误信息 |

## 安装步骤
> pip install lice 或者 easy_install lice

## 使用方法

### 1. 构建package
> python .\buildpkg.py make mypkg --version=v1.0.0 --license=MIT --ci=github --demo

### 2. 迁移开源仓库
> python .\buildpkg.py make cstring https://github.com/liu2guang/cstring.git --version=v1.0.0 --license=MIT --ci=github --demo

### 3. 更新package
> python .\buildpkg.py update cstring --version=v1.1.0 --license=GPLv3 --ci=gitlab --demo

## 测试平台

| 序号 | 测试平台 | 测试结果 | 
|:---|:---|:---|
| 1 | python27+win10 | 测试通过 |
| 2 | python37+win10 | 中文名许可证生成错误 | 
| 3 | python27+win7  | 待测试 |
| 4 | python37+win7  | 待测试 |
| 5 | python27+mac   | 路径不兼容导致错误 |
| 6 | python37+mac   | 路径不兼容导致错误 |

## 联系人

* 邮箱：[1004383796@qq.com](mailto:1004383796@qq.com)
* 主页：[liu2guang](https://github.com/liu2guang)
* 仓库：[Github](https://github.com/liu2guang), [Gitee](https://github.com/liu2guang) 

## 感谢

这个项目的存在要感谢以下开发者 [contributed](CONTRIBUTING.md). 