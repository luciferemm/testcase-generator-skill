#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
记忆管理器 - 管理 .memory 文件夹
支持：持久化记忆、历史趋势分析、歧义决策复用
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

MEMORY_DIR = ".memory"
FILES = {
    "project_context": "project-context.json",
    "terminology": "terminology.json",
    "generation_history": "generation-history.json",
    "user_preferences": "user-preferences.json",
    "ambiguity_decisions": "ambiguity-decisions.json"
}


def _print(msg):
    """Windows GBK 兼容输出"""
    try:
        print(msg)
    except UnicodeEncodeError:
        safe = msg.encode('utf-8', errors='replace').decode('gbk', errors='replace')
        print(safe)


def _print_err(msg):
    """Windows GBK 兼容错误输出"""
    try:
        print(msg, file=sys.stderr)
    except UnicodeEncodeError:
        safe = msg.encode('utf-8', errors='replace').decode('gbk', errors='replace')
        print(safe, file=sys.stderr)


def init_memory(project_path: str, assets_dir: str = "assets"):
    """初始化 .memory 文件夹"""
    memory_path = Path(project_path) / MEMORY_DIR
    memory_path.mkdir(exist_ok=True)

    context = {
        "project_name": Path(project_path).name,
        "initialized_at": datetime.now().isoformat(),
        "assets_dir": assets_dir
    }

    with open(memory_path / FILES["project_context"], 'w', encoding='utf-8') as f:
        json.dump(context, f, ensure_ascii=False, indent=2)

    defaults = {
        "terminology": {"domain_terms": {}, "module_abbreviations": {}},
        "generation_history": {"generations": []},
        "user_preferences": {
            "last_output_format": "excel",
            "default_output_dir": "./",
            "show_samples_in_preview": True,
            "auto_confirm_parsing": False,
            "ambiguity_handling": "ask",
            "priority_distribution": {
                "p0_min": 10,
                "p0_max": 25,
                "p1_min": 30,
                "p1_max": 60,
                "warn_on_imbalance": True
            },
            "default_tag": None,
            "step_granularity": "normal",
            "title_style": None,
            "updated_at": None
        },
        "ambiguity_decisions": {"decisions": []}
    }

    for key, default_value in defaults.items():
        file_path = memory_path / FILES[key]
        if not file_path.exists():
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(default_value, f, ensure_ascii=False, indent=2)

    _print("已初始化记忆: " + str(memory_path))
    return str(memory_path)


def read_memory(project_path: str, memory_type: str) -> dict:
    """读取记忆文件"""
    file_path = Path(project_path) / MEMORY_DIR / FILES.get(memory_type, "")
    if not file_path.exists():
        return {}
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def update_memory(project_path: str, memory_type: str, data: dict, merge: bool = True):
    """更新记忆文件"""
    file_path = Path(project_path) / MEMORY_DIR / FILES.get(memory_type, "")

    if merge and file_path.exists():
        with open(file_path, 'r', encoding='utf-8') as f:
            existing = json.load(f)

        def deep_merge(base, updates):
            for key, value in updates.items():
                if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                    deep_merge(base[key], value)
                else:
                    base[key] = value
            return base
        data = deep_merge(existing, data)

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    _print("已更新: " + str(file_path))


def add_generation_record(project_path: str, record: dict):
    """添加生成记录 - 支持历史趋势分析"""
    history = read_memory(project_path, "generation_history")
    if "generations" not in history:
        history["generations"] = []

    record["date"] = datetime.now().isoformat()
    history["generations"].append(record)

    update_memory(project_path, "generation_history", history, merge=False)

    trend_summary = analyze_trends(history)
    _print("趋势分析:")
    for line in trend_summary:
        _print("  " + line)


def analyze_trends(history: dict) -> list:
    """分析生成历史趋势"""
    generations = history.get("generations", [])
    if len(generations) < 2:
        return ["首次生成，暂无趋势数据"]

    last = generations[-1]
    prev = generations[-2]
    lines = []

    case_diff = last.get("case_count", 0) - prev.get("case_count", 0)
    if case_diff > 0:
        lines.append("用例数增加 " + str(case_diff) + " 条")
    elif case_diff < 0:
        lines.append("用例数减少 " + str(abs(case_diff)) + " 条")

    last_cov = last.get("coverage_rate", "0%")
    prev_cov = prev.get("coverage_rate", "0%")
    try:
        lc = float(str(last_cov).strip().rstrip('%'))
        pc = float(str(prev_cov).strip().rstrip('%'))
        if lc > pc:
            lines.append("覆盖率提升 " + f"{lc - pc:.1f}%")
        elif lc < pc:
            lines.append("覆盖率下降 " + f"{pc - lc:.1f}%")
    except (ValueError, AttributeError):
        pass

    last_dist = last.get("priority_distribution", {})
    prev_dist = prev.get("priority_distribution", {})
    for p in ["P0", "P1", "P2"]:
        lc = last_dist.get(p, 0)
        pc = prev_dist.get(p, 0)
        if lc != pc:
            lines.append(p + " 用例: " + str(pc) + " -> " + str(lc))

    total_cases = sum(g.get("case_count", 0) for g in generations)
    lines.append("累计生成 " + str(len(generations)) + " 次，共 " + str(total_cases) + " 条用例")

    modules_seen = {}
    for g in generations:
        for m in g.get("modules", []):
            modules_seen[m] = modules_seen.get(m, 0) + 1
    top_modules = sorted(modules_seen.items(), key=lambda x: -x[1])[:3]
    if top_modules:
        modules_str = "、".join(m + "(" + str(c) + "次)" for m, c in top_modules)
        lines.append("常见模块: " + modules_str)

    return lines


def clear_memory(project_path: str):
    """清除所有记忆"""
    import shutil
    memory_path = Path(project_path) / MEMORY_DIR
    if memory_path.exists():
        shutil.rmtree(memory_path)
        _print("已清除记忆: " + str(memory_path))
    else:
        _print("记忆不存在")


def get_preferences(project_path: str) -> dict:
    """获取用户偏好设置"""
    return read_memory(project_path, "user_preferences")


def set_preference(project_path: str, key: str, value):
    """设置单个偏好项"""
    prefs = get_preferences(project_path)
    prefs[key] = value
    prefs["updated_at"] = datetime.now().isoformat()
    update_memory(project_path, "user_preferences", prefs, merge=False)


def add_ambiguity_decision(project_path: str, decision: dict):
    """添加歧义处理决策记录 - 支持歧义决策复用"""
    data = read_memory(project_path, "ambiguity_decisions")
    if "decisions" not in data:
        data["decisions"] = []

    decision["date"] = datetime.now().isoformat()
    data["decisions"].append(decision)

    update_memory(project_path, "ambiguity_decisions", data, merge=False)
    _print("已记录歧义决策: " + str(decision.get('context', 'unknown')))


def find_similar_ambiguity(project_path: str, ambiguity_type: str, context: str) -> dict:
    """查找类似的历史歧义决策 - 用于自动复用"""
    data = read_memory(project_path, "ambiguity_decisions")
    decisions = data.get("decisions", [])

    for decision in reversed(decisions):
        if decision.get("type") == ambiguity_type:
            if context.lower() in decision.get("context", "").lower():
                return decision
            if context.lower() in decision.get("original_text", "").lower():
                return decision
    return None


def export_trend_report(project_path: str, format_type: str = "text"):
    """导出趋势分析报告"""
    history = read_memory(project_path, "generation_history")
    trends = analyze_trends(history)

    if format_type == "json":
        report = {
            "total_generations": len(history.get("generations", [])),
            "trends": trends,
            "generations": history.get("generations", [])
        }
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        _print("=== 生成趋势分析 ===\n")
        for line in trends:
            _print(line)

        generations = history.get("generations", [])
        if generations:
            _print("\n详细历史:")
            for i, g in enumerate(generations, 1):
                date = str(g.get("date", ""))[:19]
                source = g.get("source", "unknown")
                count = g.get("case_count", 0)
                cov = g.get("coverage_rate", "N/A")
                tag = g.get("tag", "N/A")
                _print(f"  #{i} [{date}] {source} -> {count}条 | 覆盖率: {cov} | 标签: {tag}")


def main():
    parser = argparse.ArgumentParser(
        description='管理 .memory 记忆文件夹 - 持久化记忆/历史趋势/歧义复用')
    parser.add_argument('--action', required=True,
                       choices=['init', 'read', 'update', 'clear', 'add-record',
                                'get-prefs', 'set-pref',
                                'add-ambiguity', 'find-ambiguity',
                                'trend-report'],
                       help='操作类型')
    parser.add_argument('--project', default='.', help='项目路径')
    parser.add_argument('--type', help='记忆类型')
    parser.add_argument('--data', help='JSON 格式数据')
    parser.add_argument('--key', help='偏好设置键名')
    parser.add_argument('--value', help='偏好设置值')
    parser.add_argument('--context', help='歧义上下文')
    parser.add_argument('--assets-dir', default='assets', help='模板资源目录')
    parser.add_argument('--format', default='text', choices=['text', 'json'],
                       help='趋势报告输出格式')
    args = parser.parse_args()

    try:
        if args.action == 'init':
            init_memory(args.project, args.assets_dir)

        elif args.action == 'read':
            if not args.type:
                _print_err("错误：需要指定 --type")
                sys.exit(1)
            data = read_memory(args.project, args.type)
            print(json.dumps(data, ensure_ascii=False, indent=2))

        elif args.action == 'update':
            if not args.type or not args.data:
                _print_err("错误：需要指定 --type 和 --data")
                sys.exit(1)
            update_memory(args.project, args.type, json.loads(args.data))

        elif args.action == 'clear':
            clear_memory(args.project)

        elif args.action == 'add-record':
            if not args.data:
                _print_err("错误：需要指定 --data")
                sys.exit(1)
            add_generation_record(args.project, json.loads(args.data))

        elif args.action == 'get-prefs':
            prefs = get_preferences(args.project)
            print(json.dumps(prefs, ensure_ascii=False, indent=2))

        elif args.action == 'set-pref':
            if not args.key or not args.value:
                _print_err("错误：需要指定 --key 和 --value")
                sys.exit(1)
            try:
                value = json.loads(args.value)
            except json.JSONDecodeError:
                value = args.value
            set_preference(args.project, args.key, value)
            _print("已设置 " + str(args.key) + " = " + str(value))

        elif args.action == 'add-ambiguity':
            if not args.data:
                _print_err("错误：需要指定 --data")
                sys.exit(1)
            add_ambiguity_decision(args.project, json.loads(args.data))

        elif args.action == 'find-ambiguity':
            if not args.type or not args.context:
                _print_err("错误：需要指定 --type 和 --context")
                sys.exit(1)
            result = find_similar_ambiguity(args.project, args.type, args.context)
            if result:
                _print("找到历史歧义决策:")
                print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                _print("未找到类似决策")

        elif args.action == 'trend-report':
            export_trend_report(args.project, args.format)

    except Exception as e:
        _print_err("操作失败: " + str(e))
        sys.exit(1)


if __name__ == "__main__":
    main()
