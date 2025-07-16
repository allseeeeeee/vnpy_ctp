# -*- coding: utf-8 -*-
"""
描述: setup_vnpy.py用于管理 vnpy_modules.yaml 中定义的模块，自动：
1. 拉取/更新 subtree
2. pip install -e 安装
3. 更新 pyproject.toml 中的 dependencies

作者: LuoJingtian
日期: 2025/7/15
"""
import os
import subprocess
import sys

import yaml
import tomlkit
from pathlib import Path

ROOT = Path(__file__).parent.resolve()
PYPROJECT = ROOT / "pyproject.toml"
VN_MODULES = "vnpy_modules"
VN_MODULES_DIR = ROOT / VN_MODULES
VN_MODULES_CONF = ROOT / f"{VN_MODULES}.yaml"
os.makedirs(VN_MODULES_DIR, exist_ok=True)

class GitContext :
    def __init__(self, commit=False):
        self.commit = commit
    def __enter__(self):
        if self.commit:
            print("💡 Commiting current changes...")
            subprocess.run(["git", "add", "."])
            subprocess.run(["git", "commit", "-m", "auto commit before subtree"])
        else:
            print("💡 Stashing current changes...")
            subprocess.run(["git", "stash", "push", "-m", "auto stash before subtree"])
    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.commit:
            print("💡 Applying stash...")
            subprocess.run(["git", "stash", "pop"])

def load_modules():
    if not VN_MODULES_CONF.exists():
        print(f"❌ 配置文件不存在: {VN_MODULES_CONF}")
        sys.exit(1)

    with open(VN_MODULES_CONF, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def run(cmd, shell=True, check=True, timeout=None):
    print("▶", cmd)
    subprocess.run(cmd, shell=shell, check=check, timeout=timeout)


def install(mod_name, version=None, editable=False):
    print(f"🔧 Installing{' in editable mode' if editable else ''}: {mod_name}{version if version else ''}")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", f"{'-e' if editable else ''}", str(VN_MODULES_DIR / mod_name)],
            shell=True,
            check=True,
            capture_output=True,
            text=True,
            encoding='utf-8'  # ➤ 关键：强制使用 UTF-8 解码
        )
        if result.returncode != 0:
            print(f"❌ Install failed: {mod_name}")
            print(result.stdout)
            print(result.stderr)
            sys.exit(1)
        else:
            print(f"✅ Installed: {mod_name}\n")
    except subprocess.CalledProcessError as e:
        print(f"❌ Install failed: {mod_name}", e)
        print(e.stdout)
        print(e.stderr)
        return None


def update_subtree(name, mod):
    repo = mod["repo"]
    branch = mod.get("branch", "master")

    path = VN_MODULES_DIR / name
    if not path.exists():
        run(f"git subtree add --prefix={VN_MODULES}/{name} {repo} {branch} --squash")
    else:
        run(f"git subtree pull --prefix={VN_MODULES}/{name} {repo} {branch} --squash")


def main():
    with GitContext(commit=True):
        modules = load_modules()
        for name, mod in modules.items():
            if mod.get("subtree"):
                update_subtree(name, mod)
                install(name, editable=True) # ➤ 本地模块，-e 安装
            else:
                install(name, mod.get("version"), editable=False)  # ➤ 非本地模块，正常 pip 安装

    print("✅ vnpy_setup 完成")


if __name__ == "__main__":
    main()
    print(ROOT)
    print(VN_MODULES_DIR)
    print(VN_MODULES_DIR / "vnpy")
    pass
