<div align="center">
  <a href="https://github.com/rtpkgs/buildpkg">
    <img width="200" heigth="200" src="/figures/logo.png">
  </a>  

  <div align="center">
    <a href="https://github.com/rtpkgs/buildpkg">
      <img src="https://img.shields.io/travis/liu2guang/Lua2RTT/master.svg?style=flat-square" alt="travis-ci" />
    </a>
    <a href="https://github.com/rtpkgs/buildpkg/stargazers">
      <img src="https://img.shields.io/github/stars/rtpkgs/buildpkg.svg?style=flat-square" alt="stargazers" />
    </a>
    <a href="https://github.com/rtpkgs/buildpkg/graphs/contributors">
      <img src="https://img.shields.io/github/contributors/rtpkgs/buildpkg.svg?style=flat-square" alt="contributors" />
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

buildpkg 是用于生成 RT-Thread package 的快速构建工具。

一个优秀的 package 应该是这样的：
 1. 代码优雅, 规范化。
 2. examples 例程，提供通俗易懂的使用例程。
 3. SConscript 文件，用于和 RT-Thread 环境一起进行编译。
 4. README.md 文档，向用户提供必要的功能说明。
 5. docs 文件夹, 放置除了 README 之外的其他细节文档。
 6. license 许可文件，版权说明。

为了方便快速的生成 RT-Thread package 规范化模板 以及 减轻开源仓库迁移 RT-Thread 的前期准备工作的负担，基于此目的的 buildpkg 应运而生，为开发 Rt-Thread 的 package 的开发者提供辅助开发工具。

| 序号  | 支持功能 | 描述 |
| :--- | :--- | :--- |
| 1 | 构建 package 模板 | 创建指定名称 package , 自动添加 readme /版本号/ github ci脚本/demo/开源协议文件 |
| 2 | 迁移开源仓库 | 从指定 git 仓库构建 package , 自动添加readme/版本号/ github ci脚本/demo/开源协议文件, 但是迁移的仓库需要用户自己按照实际情况修改 |
| 3 | 更新 package | 生成package后可以再次更新之前设定的版本号，开源协议或者scons脚本等 | 

## 使用说明

### 1. 构建package
> buildpkg.exe make pkgdemo

### 2. 迁移开源仓库
> buildpkg.exe make cstring https://github.com/liu2guang/cstring.git

### 3. 更新package
> buildpkg.exe update pkgname

### 4. 可选配置 
| 长参数  | 短参数 | 描述 |
| :--- | :--- | :--- |
| --version=v1.0.0 | -v v1.0.0 | 设置 package 的版本 |
| --license=MIT | -l MIT | 设置 package 所遵循的版权协议 |
| --submodule | -s |删除 git 子模块 |

## Windows10 及 Linux 平台的演示动图
![buildpkg](/figures/buildpkg.gif)

## 测试平台

| 序号 | 测试平台 | 测试结果 | 
|:---|:---|:---|
| 1 | win10 | exe测试通过, py测试通过 |
| 2 | win7  | exe待测试, py待测试 | 
| 3 | mac   | py脚本不知道是否兼容, 没有测试条件, 后面维护下 |
| 4 | linux | py脚本不知道是否兼容, 没有测试条件, 后面维护下 |

## 联系人

* 邮箱：[1004383796@qq.com](mailto:1004383796@qq.com)
* 主页：[liu2guang](https://github.com/liu2guang)
* 仓库：[Github](https://github.com/liu2guang), [Gitee](https://github.com/liu2guang) 

## 感谢

感谢以下开发者的大力支持: [contributed](CONTRIBUTING.md)
<div>
    <a href="https://github.com/rtpkgs/buildpkg">
      <img width="50" heigth="50" src="https://avatars2.githubusercontent.com/u/24929334?s=400&u=da62f43f6c4ff722b9b9defb704f2c585536347e&v=4">
    </a>
    <a href="https://github.com/rtpkgs/buildpkg">
      <img width="50" heigth="50" src="https://avatars2.githubusercontent.com/u/30776697?s=400&v=4">
    </a>
</div>
