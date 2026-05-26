# TestCase Generator 3 入口

本项目是自主学习型测试用例生成器。请完整加载并严格遵循以下 Skill 文件中定义的工作流程和行为规范：

@SKILL.md

---

## 启动行为（每次对话开始时必须执行）

1. **检测 `.memory/` 是否存在**：
   - 存在 → 读取 `.memory/user-preferences.json` 恢复用户偏好（标签、步骤粒度等）
   - 不存在 → 执行 **Phase 0 首次初始化**流程

2. **Phase 0 首次初始化**：
   - 运行 `python scripts/memory_manager.py --action init --project .`
   - 初始化用户偏好，保存到 `.memory/user-preferences.json`

3. **等待用户指令**，常见触发词：
   - "生成测试用例" / "创建用例" / "输出测试用例"
   - "根据这个文档生成测试"
   - "只要正向" / "不要异常" / "只要功能测试"

## 项目结构

```
testcase-generator3/
├── scripts/                     # 工具脚本（write_excel_from_json.py / memory_manager.py）
│   ├── write_excel_from_json.py # Excel 输出脚本
│   └── memory_manager.py       # 记忆管理器
├── references/                  # 规范文档（测试用例标准、记忆系统 Schema）
├── .memory/                     # 持久化记忆（自动生成，勿手动修改）
├── assets/                      # 模板资源
└── tmp/                         # 中间 JSON 文件（自动管理）
```
