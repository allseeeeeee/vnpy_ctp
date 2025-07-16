# ai-trader-edge

实盘终端（客户端）

## 项目结构
ai-trader-edge/                 ← 主项目根目录（Git 仓库）
├── ai_trader_edge/             ← 主项目业务代码
│   ├── __init__.py
│   ├── main.py                 ← PyQt 主程序入口
│   └── ...
│
├── setup_vnpy.py               ← 根据vnpy-modules.yaml 配置 pyproject.toml, requirements-dev.txt, ai-trader-edge.spec, 管理 subtree
├── vnpy_modules.yaml           ← ✅ 模块注册中心
├── vnpy/                       ← ✅ subtree 所有本地子模块源码统一放这里, 由 setup_vnpy.py 配置
│   ├── vnpy/                   ← 若要本地维护核心模块
│   ├── vnpy-ctp/               ← 就从社区 clone
│   ├── vnpy-tts/               ← 可选, 如需OpenCTP模拟盘时安装
│   └── ...
├── ai_trader_edge.spec         ← ✅ PyInstaller 打包脚本
├── pyproject.toml              ← 主项目依赖声明（包含 dev 本地模块依赖）
├── requirements-dev.txt        ← 仅声明 dev 依赖中的本地模块, -e 模式 只能用requirements-dev.txt, 不能用pyproject.toml
└── .gitignore


### 下载源码

#### 克隆主项目
```shell
cd D:\Team\
git clone http://git.i.healthcareyun.com/JIANSU/ai-trader-edge.git
```

#### 以 subtree 模式克隆VN.py项目
> 为避免污染主项目 .git 历史, 使用 subtree模式添加社区模块（因为 --squash）
> 子模块目录是普通目录，打包、导入都无障碍
> 支持向上游提交 PR（可从 upstream clone/fork 提交）

```shell
cd vnpy/

git subtree add --prefix vnpy/vnpy https://github.com/vnpy/vnpy.git master --squash
git subtree add --prefix vnpy/vnpy-ctp https://github.com/vnpy/vnpy-ctp.git master --squash
git subtree add --prefix vnpy/vnpy-tts https://github.com/vnpy/vnpy-tts.git master --squash
git subtree add --prefix vnpy/vnpy-mongodb https://github.com/vnpy/vnpy-mongodb.git master --squash

```


### 后续更新社区模块

> 更新指定的社区模块
```shell
cd vnpy/vnpy-mongodb/
# 拉取远端变更并合并到当前目录下
git subtree pull --prefix vnpy/vnpy-mongodb https://github.com/vnpy/vnpy-mongodb.git master --squash -r 
```

> 一键更新所有社区模块

```powershell
$baseDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$modules = Get-ChildItem -Path "$baseDir\vnpy_modules" -Directory

foreach ($mod in $modules) {
    $modName = $mod.Name
    Write-Host ">>> 更新模块 $modName ..."
    git subtree pull --prefix="vnpy/$modName" origin master --squash -r
    Write-Host ">>> 模块 $modName 更新完成"
}

Write-Host "所有模块更新完毕"
```

```bash
#!/bin/bash

BASE_DIR="$(cd "$(dirname "$0")" && pwd)/vnpy_modules"

for mod_dir in "$BASE_DIR"/*; do
  if [ -d "$mod_dir" ]; then
    mod_name=$(basename "$mod_dir")
    echo ">>> 更新模块 $mod_name ..."
    git subtree pull --prefix="vnpy_modules/$mod_name" origin master --squash -r
    echo ">>> 模块 $mod_name 更新完成"
  fi
done

echo "所有模块更新完毕"
```


### push PR 到社区
```shell
git remote add vnpy-mongodb-fork https://github.com/yourname/vnpy-mongodb.git
git checkout -b your-feature-branch
git subtree push --prefix=vnpy/vnpy-mongodb vnpy-mongodb-fork your-feature-branch
```


## 环境配置

### 安装 Python 3.11+


### 安装开发依赖

```shell
python -m pip install --upgrade pip
pip install -e . -i https://mirrors.aliyun.com/pypi/simple
pip install ".[dev]" -i https://mirrors.aliyun.com/pypi/simple
# 拉取/更新 + 安装所有模块 + 同步配置
python -m tools.setup_vnpy
```

ta_lib 安装失败时的解决办法:
> fatal error C1083: 无法打开包括文件: “ta_libc.h”: No such file or directory
> 解决办法:
```shell
wget https://github.com/cgohlke/talib-build/releases/download/v0.6.4/ta_lib-0.6.4-cp311-cp311-win_amd64.whl
pip install "C:\Users\DEV01\Downloads\ta_lib-0.6.4-cp311-cp311-win_amd64.whl"
pip install . -i https://mirrors.aliyun.com/pypi/simple 
```

### 手动以开发模式安装指定的VNPY模块
```shell
pip install -e ./vnpy/vnpy
pip install -e ./vnpy/vnpy-ctp
pip install -e ./vnpy/vnpy-tts
pip install -e ./vnpy/vnpy-mongodb
```


## 打包 PyQt 界面应用
```shell
pyinstaller ai-trader-edge.spec
```