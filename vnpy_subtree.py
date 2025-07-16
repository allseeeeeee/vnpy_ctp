# -*- coding: utf-8 -*-
"""
描述: 提供 git subtree add/pull/push 操作封装
作者: LuoJingtian
日期: 2025/7/15
"""
import subprocess
import yaml
from pathlib import Path
import argparse

ROOT = Path(__file__).resolve().parent.parent
MODULES_CONFIG = ROOT / "vnpy_modules.yaml"
VN_MODULES_DIR = ROOT / "vnpy_modules"


def run(cmd):
    print("▶", cmd)
    subprocess.run(cmd, shell=True, check=True)


def load_modules():
    with open(MODULES_CONFIG, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def subtree_add(name, mod):
    repo = mod["repo"]
    branch = mod.get("branch", "master")
    path = VN_MODULES_DIR / name
    run(f"git subtree add --prefix={path} {repo} {branch} --squash")


def subtree_pull(name, mod):
    repo = mod["repo"]
    branch = mod.get("branch", "master")
    path = VN_MODULES_DIR / name
    run(f"git subtree pull --prefix={path} {repo} {branch} --squash -r")


def subtree_push(name, mod):
    repo = mod["repo"]
    branch = mod.get("branch", "master")
    path = VN_MODULES_DIR / name
    run(f"git subtree push --prefix={path} {repo} {branch}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["add", "pull", "push"])
    parser.add_argument("name", help="模块名，如 vnpy-ctp 或 all")
    args = parser.parse_args()

    modules = load_modules()

    targets = [args.name] if args.name != "all" else [k for k, v in modules.items() if v.get("subtree")]
    for name in targets:
        mod = modules.get(name)
        if not mod:
            print(f"❌ 未找到模块 {name}")
            continue

        if args.action == "add":
            subtree_add(name, mod)
        elif args.action == "pull":
            subtree_pull(name, mod)
        elif args.action == "push":
            subtree_push(name, mod)

    print(f"✅ 完成")

if __name__ == '__main__':
    main()