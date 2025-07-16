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

def load_modules():
    if not VN_MODULES_CONF.exists():
        print(f"❌ 配置文件不存在: {VN_MODULES_CONF}")
        sys.exit(1)

    with open(VN_MODULES_CONF, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def run(cmd):
    print("▶", cmd)
    subprocess.run(cmd, shell=True, check=True)


def install_editable(mod_name):
    print(f"🔧 Installing in editable mode: {mod_name}")
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "-e", str(VN_MODULES_DIR / mod_name)],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print(f"❌ Install failed: {mod_name}")
        print(result.stderr)
        sys.exit(1)
    else:
        print(f"✅ Installed: {mod_name}\n")


def update_subtree(name, mod):
    repo = mod["repo"]
    branch = mod.get("branch", "master")

    path = VN_MODULES_DIR / name
    if not path.exists():
        run(f"git subtree add --prefix={VN_MODULES}/{name} {repo} {branch} --squash")
    else:
        run(f"git subtree pull --prefix={VN_MODULES}/{name} {repo} {branch} --squash")


def update_pyproject(modules):
    with open(PYPROJECT, "r", encoding="utf-8") as f:
        doc = tomlkit.parse(f.read())

    dependencies = doc["project"]["dependencies"]
    dependencies[:] = [
        f"{name}{mod['version']}"
        for name, mod in modules.items()
        if not mod.get("subtree")
    ]

    with open(PYPROJECT, "w", encoding="utf-8") as f:
        f.write(tomlkit.dumps(doc))


def main():
    modules = load_modules()
    for name, mod in modules.items():
        if mod.get("subtree"):
            update_subtree(name, mod)
            # install_editable(name)

    update_pyproject(modules)
    print("✅ vnpy_setup 完成")


if __name__ == "__main__":
    main()
    print(ROOT)
    print(VN_MODULES_DIR)
    print(VN_MODULES_DIR / "vnpy")
    pass
