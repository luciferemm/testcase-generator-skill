---
name: testcase-generator
description: >
  自主学习型测试用例生成器 - 根据PRD文档/设计图/在线文档自动生成功能测试用例Excel。

  **核心能力**：支持PRD输入(Word/Markdown/PDF/图片/URL)、只输出Excel格式、多类型覆盖(功能/边界/异常)、智能用例筛选、持久化记忆系统、历史趋势分析与歧义决策复用

  **触发词**：
  - 生成类："生成测试用例"、"创建用例"、"输出测试用例"
  - 筛选类："只要正向"、"不要异常"、"只要功能测试"
  - 记忆类："更新术语表"、"清除记忆"、"查看偏好"
---

# TestCase Generator 2 - 自主学习型测试用例生成器

## 快速参考

### 输出格式

只输出 Excel 格式（.xlsx 文件），直接生成测试用例Excel。

### 用例类型筛选


| 筛选词           | 效果        |
| ------------- | --------- |
| "只要正向"、"正向用例" | 只生成正向测试用例 |
| "不要异常"、"不要反向" | 排除异常/反向用例 |
| "只要功能"        | 只生成功能测试用例 |


### 输入类型识别


| 类型       | 支持格式                    |
| -----     | -------------------------  |
| PRD文档    | .docx, .md, .txt, .pdf     |
| 设计图     | .png, .jpg (需配合文字描述)  |
| 在线文档   | 任意可访问的URL              |


### 记忆操作命令

| 用户指令       | 脚本操作                                     |
|--------------|---------------------------------------------|
| `更新术语表`   | 重新扫描 `terminology.json`                 |
| `清除记忆`     | 重置所有学习数据                              |
| `查看偏好`     | 查看当前保存的用户偏好和生成历史               |
| `更新偏好`     | 直接对话说明偏好，AI 询问是否持久化             |

---

## 交互模式定义

### 模式类型

采用**快速模式**：仅在发现问题或异常时询问用户，无异常时自动继续执行。

### 偏好存储

用户偏好保存在 `.memory/user-preferences.json` 中。

### 检查点概览

| 检查点 | 阶段 | 行为 |
|--------|------|------|
| 解析确认 | Phase 2.5 | 摘要+问题时询问 |
| 歧义处理 | Phase 2.6 | 仅关键歧义 |
| 生成预览 | Phase 2.8 | 统计数据 |

---

## 核心能力

### 1. 智能输入解析
自动识别输入文档类型，提取功能需求。支持 PRD 文档、设计图、在线文档。

### 2. 测试覆盖维度

| 类型        | 覆盖内容              |
| ---------- | ------------------- |
| 正向测试    | 核心业务流程验证        |
| 反向测试    | 异常输入、错误处理      |
| 边界值测试  | 输入边界、条件边界      |
| 等价类划分  | 测试数据合理分组        |
| 场景测试    | 跨模块业务流程          |
| 权限测试    | 未授权访问、越权操作    |
| 网络异常测试 | 断网、超时、弱网环境    |
| 并发测试    | 重复提交、并发抢购      |

### 3. 字段规范

**标准字段**：

| 字段       | 必填 | 说明                      |
| ---------- | --- | ------------------------- |
| 用例编号   | ✓   | TC_模块_序号，如 TC_LOGIN_001 |
| 所属模块   | ✓   | 用例所属模块               |
| 用例标题   | ✓   | 简洁描述测试点             |
| 用例类型   | ✓   | 功能测试/边界测试/异常测试  |
| 优先级     | ✓   | P0/P1/P2                  |
| 前置条件   | ✓   | 执行前需满足的条件         |
| 测试步骤   | ✓   | 逐条操作描述              |
| 预期结果   | ✓   | 每步对应的预期行为         |

### 4. 优先级定义

| 优先级 | 占比     | 定义            |
| ------ | -------- | --------------- |
| P0     | 10-25%   | 核心功能、主流程 |
| P1     | 30-60%   | 重要功能、主流场景 |
| P2     | 10-25%   | 边缘功能、特殊场景 |

### 5. 质量标准（7维度自检）

生成测试用例前必须通过以下 7 维度检查（Phase 2.8 质量预审时逐项检查，任一不通过则修正后再展示）：

| 维度 | 标准 | 检查方式 |
|------|------|----------|
| **需求覆盖** | 每条需求至少关联 1 条用例，覆盖率 ≥ 95% | 追溯计算 |
| **方法覆盖** | 每条需求至少使用 1 种设计方法 | 方法分布统计 |
| **优先级分布** | P0: 10-25%, P1: 30-60% | 分布比例检查 |
| **步骤可执行** | 每条用例的步骤明确、可操作，预期结果可验证 | AI 自检 |
| **无需求外编造** | 所有用例来源于需求文档，不凭空编造场景 | 追溯关系验证 |
| **术语一致** | 用例中使用的术语与需求文档、`terminology.json` 一致 | 术语对照 |
| **无冗余重复** | 不同方法产生的用例无语义重复 | 去重扫描 |

---

## 需求追溯与覆盖率

### 双向追溯矩阵

每次生成后自动建立需求↔用例的双向追溯，确保每条需求都有测试覆盖，每条用例都能追溯到来源需求。

**正向追溯（需求 → 用例）**：

```markdown
| 需求ID | 需求名称 | 用例ID列表 | 用例数 | 覆盖状态 |
|--------|---------|-----------|-------|---------|
| MOD_LOGIN_001 | 用户登录 | TC_001, TC_002 | 2 | ✅ 已覆盖 |
| MOD_ORDER_001 | 订单创建 | TC_005, TC_006, TC_007 | 3 | ✅ 已覆盖 |
| REQ-003 | 第三方登录 | - | 0 | ❌ 未覆盖 |
```

**反向追溯（用例 → 需求）**：
每条用例 JSON 中记录 `关联需求ID` 字段，可在 Excel 中体现。

### 需求ID提取规则

解析需求文档时自动识别需求标识：

| 模式 | 示例 |
|------|------|
| 标准编号 `REQ[-_]?\d+` | REQ_001, REQ-123 |
| 功能编号 `F[-_]?\d+(\.\d+)*` | F1.2, F-3.1.2 |
| 用户故事 `US[-_]?\d+` | US_042 |
| JIRA格式 `[A-Z]+-\d+` | PROJ-123 |
| 中文编号 | 需求001 |

**自动生成**：若需求文档无编号，按 `MOD_{模块缩写}_{序号}` 自动生成（如 `MOD_LOGIN_001`）。

### 覆盖率计算

```
需求覆盖率 = 已覆盖需求数 / 总需求数 × 100%
```

- 至少有 1 条用例关联的需求视为「已覆盖」
- 覆盖率目标：**≥ 95%**
- Phase 2.8 质量预审时自动计算覆盖率
- Phase 4 将覆盖率写入 `generation-history.json`

### 遗漏检测

- **未覆盖需求**：遍历需求列表，标记无关联用例的需求为 ❌ 未覆盖
- **孤儿用例**：遍历用例列表，无关联需求ID的用例标记为 ⚠️ 孤儿用例

---

## .memory 记忆系统

Skill 在项目中创建 `.memory/` 文件夹，存储跨会话学习数据：

```
.memory/
├── project-context.json      # 项目上下文（路径、名称）
├── terminology.json          # 领域术语库（自动学习 + 手动补充）
├── generation-history.json   # 生成历史（质量趋势分析）
├── user-preferences.json     # 用户偏好（交互模式、默认标签）
└── ambiguity-decisions.json  # 歧义决策记录（避免重复询问）
```

### 核心机制

- **持久化记忆**：每次生成自动写入 `generation-history.json`（含覆盖率、优先级分布、用例数等）
- **历史趋势分析**：与历史记录对比，生成趋势摘要（覆盖率变化、用例数变化、常见遗漏类型）
- **歧义决策复用**：歧义处理决策写入 `ambiguity-decisions.json`，后续相似歧义自动复用
- **术语自动学习**：用户修正的术语自动持久化到 `terminology.json`，下次会话即刻生效
- **偏好记忆**：用户偏好（标签、步骤粒度等）自动保存在 `user-preferences.json`

### 自学习闭环

```
写入端（Phase 4/5）                    读取端（Phase 2）
─────────────────────                ─────────────────────
生成历史 ───→ generation-history.json ──→ 优先级基线 + 遗漏场景补充
歧义决策 ───→ ambiguity-decisions.json ─→ 相似歧义自动复用
新术语   ───→ terminology.json ────────→ 术语统一 + 缩写展开
用户偏好 ───→ user-preferences.json ────→ 标签/粒度/风格自动应用
用户反馈 ───→ 分发到以上各文件 ──────────→ 下次生成自动避免相同问题
```

---

## 工作流程（阶段式）

### Phase 0: 项目初始化（首次运行）
1. 检测 `.memory/` 是否存在，不存在时初始化
2. 创建 `.memory/` 文件夹（`python scripts/memory_manager.py --action init --project .`）
3. 保存默认偏好到 `user-preferences.json`

### Phase 1: 读取输入
1. 识别输入类型：
   - 本地文件（`.docx`, `.md`, `.txt`, `.pdf`）→ 直接读取内容
   - 图片（`.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`）→ 作为多模态输入
   - URL → 抓取页面内容
   - 直接文本 → 直接使用
2. 将内容进入 Phase 2 解析

### Phase 2: 解析需求 & 测试设计
1. **加载记忆并应用**：
   - 读取 `terminology.json` → 解析时统一术语
   - 读取 `ambiguity-decisions.json` → 相似歧义自动复用历史决策，跳过询问
   - 读取 `generation-history.json` → 提取历史优先级分布作为基线，识别历史常见遗漏场景类型并主动补充
   - 读取 `user-preferences.json` → 应用用户偏好

2. **提取需求ID**：识别或生成需求唯一标识（遵循需求追溯章节的提取规则）

3. **智能解析**：
   - 提取功能模块和层级关系
   - 抽取业务规则、验收条件、约束条件
   - 识别输入字段、边界值、异常场景
   - 为每条需求关联需求ID

3. **系统化测试设计**（考虑多种覆盖维度）：
   - 等价类划分：识别所有输入的有效/无效等价类
   - 边界值提取：识别数值、长度、时间边界
   - 场景流识别：基本流、备选流、异常流
   - 错误推测补充：根据输入类型和模块风险等级触发
   - 根据筛选词调整覆盖范围

4. **去重扫描**：合并语义重复的用例，保留更具体的

5. **歧义检测**：识别不明确的需求描述；与 `ambiguity-decisions.json` 比对

### Phase 2.5: 【检查点1】解析确认

**触发条件**：Phase 2 解析完成后

**显示内容**：
```markdown
## 解析完成

已识别 **{module_count}** 个模块，**{req_count}** 条需求，**{rule_count}** 条业务规则

{如果有警告}
⚠️ 发现以下潜在问题：
- {warning_message}
```

**AskUserQuestion 配置**（仅有警告时）：
```yaml
questions:
  - question: "发现潜在问题，如何处理？"
    header: "解析警告"
    multiSelect: false
    options:
      - label: "忽略，继续生成"
        description: "问题不影响生成质量"
      - label: "查看详情"
        description: "显示完整解析结果"
```

**无警告时**：显示摘要后自动继续

此处确定「适用端」标签（首次或无偏好时询问）：
- 若需求中有显式声明（如 `tag只适用于PC端`），直接读取，**不得询问**
- 无显式声明时提供选项：PC/APP/C端/PC,APP/小程序/其他
- 用户输入原样写入标签，禁止翻译/展开/同义替换
- **标签问题仅在此阶段处理一次，全程不再重复询问**

---

### Phase 2.6: 歧义处理

**触发条件**：检测到不明确的需求描述

**歧义类型**：

| 类型代码 | 类型名称 | 检测模式 | 询问重点 |
|---------|---------|---------|---------|
| `BOUNDARY_UNCLEAR` | 边界不明确 | "适当"、"合理"、"一定" | 询问具体数值 |
| `RULE_CONFLICT` | 规则冲突 | 互斥条件 | 询问优先级 |
| `MISSING_ERROR` | 缺少错误处理 | 无失败子句 | 询问预期行为 |
| `VAGUE_CRITERIA` | 模糊验收标准 | "正常"、"正确" | 询问具体结果 |
| `INCOMPLETE_FLOW` | 流程不完整 | 缺少步骤 | 询问完整流程 |

**显示上下文**：
```markdown
## 需求歧义确认 ({current}/{total})

**需求原文**：
> {original_text}

**歧义类型**：{ambiguity_type_name}

**我的理解**：
{ai_interpretation}

**影响范围**：
- 可能影响 {affected_cases} 条用例
- 涉及模块：{affected_modules}
```

**AskUserQuestion 配置**：
```yaml
questions:
  - question: "需求存在歧义，请帮助澄清"
    header: "歧义 {current}/{total}"
    multiSelect: false
    options:
      - label: "接受我的理解"
        description: "{interpretation}"
      - label: "提供不同解释"
        description: "我将输入正确的理解"
      - label: "跳过此需求"
        description: "不为此需求生成用例"
      - label: "标记为待确认"
        description: "生成用例但添加待确认标记"
```

**歧义过滤**：
- 仅询问影响 P0/P1 用例的歧义
- 涉及核心业务流程的歧义
- 可能导致生成错误的关键歧义
- 其他歧义自动采用 AI 理解，并在生成结果中标注

**与 `ambiguity-decisions.json` 比对**：相似歧义自动复用历史决策，跳过询问

---

### Phase 2.8: 【检查点2】质量预审 & 生成预览

**触发条件**：歧义处理完成，准备生成用例

**质量自检（不通过则修正后再展示）**：
```
□ 覆盖率 ≥ 95%（未覆盖需求列表高亮）
□ P0 占比 10-25%
□ P1 占比 30-60%
□ 每条需求至少关联 1 种设计方法
□ 无需求外编造的场景
□ 无语义重复用例
```

**显示内容**：
```markdown
## 生成预览

将生成 **{total_cases}** 条用例：
P0:{p0} | P1:{p1} | P2:{p2}

覆盖率概览：
- 总需求数：{total_reqs}
- 已覆盖：{covered}（{coverage_rate}%）
- 未覆盖：{uncovered}
- 覆盖深度：{depth} 用例/需求

{未覆盖时高亮显示}
⛔ 未覆盖需求：{uncovered_reqs}
```

**AskUserQuestion 配置**（仅质量自检不通过时）：
```yaml
questions:
  - question: "P0比例({p0_percent}%)超出建议范围(10-25%)，是否调整？"
    header: "分布警告"
    multiSelect: false
    options:
      - label: "自动调整到建议范围"
        description: "将部分 P0 用例降级为 P1"
      - label: "保持当前分布"
        description: "不做调整，继续生成"
```

**通过则自动继续**，质量自检通过 + 分布正常时不询问；
**不通过时先自动修正，修正后再重新检查**，直到通过才进入 Phase 3

### Phase 3: 生成文档
1. 分配优先级（P0/P1/P2）
2. **关联需求ID**：每个用例记录来源需求ID，实现反向追溯
3. 构建标准字段的测试用例 JSON 数组
4. `write_to_file()` 保存到临时 JSON 文件 `tmp/testcases_<时间戳>.json`
5. `execute_command()` 调用 `python scripts/write_excel_from_json.py --data tmp/testcases_<时间戳>.json --output testcases_<时间戳>.xlsx`
6. 生成的 Excel 文件保存在项目根目录，文件名格式：`testcases_<YYYYmmddHHMMSS>.xlsx`

### Phase 4: 更新记忆（自学习闭环）
1. **生成历史**：写入 `generation-history.json`（含覆盖率、优先级分布、用例数、模块列表、来源文档、未覆盖需求列表）
2. **歧义决策**：将 Phase 2.6 中用户的决策写入 `ambiguity-decisions.json`
3. **新术语**：如解析中发现新术语，更新 `terminology.json`
4. **用户偏好**：保存默认标签等到 `user-preferences.json`
5. **质量趋势**：与历史记录对比，生成趋势摘要

### Phase 5: 用户反馈学习（生成后可选）
用户对生成结果提出修改时，自动触发学习：

| 反馈类型     | 示例                       | 学习动作                                   |
|------------|---------------------------|-------------------------------------------|
| 纠正错误     | "这条用例逻辑不对"            | 重新生成 + 记录歧义模式到 `ambiguity-decisions.json` |
| 删减用例     | "P2 太多了"                 | 询问"是否调整优先级分布作为默认？"→ 写入 `user-preferences.json` |
| 补充场景     | "还缺并发场景"               | 增补用例 + 记录为常见遗漏到 `generation-history.json` |
| 修改术语     | "这里应该叫 XXX"             | 询问"是否记住？"→ 写入 `terminology.json` |
| 调整步骤     | "步骤太细了，合并一下"         | 询问"是否记住这个粒度偏好？"→ 写入 `user-preferences.json` |

---

## 响应处理规则

### 用户响应映射

| 用户输入 | 处理动作 |
|---------|---------|
| `确认` / `ok` / `yes` / `y` | 继续下一步 |
| `取消` / `cancel` / `no` / `n` | 中止流程 |
| `详情` / `detail` / `more` | 显示详细信息 |
| `修改` / `edit` / `change` | 进入修改模式 |
| `重试` / `retry` / `redo` | 重新执行当前步骤 |
| `帮助` / `help` / `?` | 显示当前步骤帮助 |

### 超时处理

无超时限制，无异常时自动继续。

### 错误恢复

当用户输入无法识别时：
1. 显示可用选项列表
2. 提示正确的输入格式
3. 等待用户重新输入

---

## 进度指示

### 流程进度显示

```
[■■■■■□□□□□] 50% - 正在解析需求...

阶段: 2/5 需求解析
已处理: 10/20 个需求
当前: 分析登录模块边界条件
```

### 检查点进度

```
检查点 1/3: 解析确认
└── ✓ 模块识别完成
└── ✓ 需求提取完成
└── → 等待用户确认
```

---

## 记忆集成与自学习

### 偏好自动应用

每次启动时从 `.memory/user-preferences.json` 读取：
- `default_output_dir`: Excel 输出目录默认值
- `default_tag`: 上次选择的标签值，作为建议选项
- `step_granularity`: 用户偏好的步骤粒度

### 歧义决策复用

从 `.memory/ambiguity-decisions.json` 读取历史决策：
- 自动应用历史决策，不再询问

### 学习用户习惯

每次交互后自动记录：
- 用户对歧义的处理偏好（ask/skip/mark）
- 用户常调整的优先级比例
- 用户选择的标签值
- 反馈修正（如删减用例、补充场景）

### 质量趋势

从 `.memory/generation-history.json` 分析：
- 历史生成的优先级分布，作为下次生成的参考基线
- 常见模块清单，优化场景覆盖模式
- 覆盖率趋势，发现系统性遗漏

---

## Excel输出流程

当用例数量较多时（>10个），使用文件方式避免超限：

```
1. 生成测试用例 JSON 数组
2. write_to_file() 保存到临时 JSON 文件（如 tmp/testcases_<时间戳>.json）
3. execute_command() 调用脚本转换格式
```

**调用脚本**：

```bash
python scripts/write_excel_from_json.py --data tmp/testcases_<时间戳>.json --output testcases_<时间戳>.xlsx
```

**JSON格式要求**：

```json
{
  "testcases": [
    {
      "case_id": "TC_LOGIN_001",
      "module": "登录模块",
      "case_name": "用例标题",
      "case_type": "功能测试",
      "priority": "P0",
      "req_id": "MOD_LOGIN_001",
      "precondition": "前置条件",
      "test_steps": "测试步骤",
      "expected_result": "预期结果",
      "remark": "备注"
    }
  ]
}
```

**脚本参数说明**：

| 参数             | 说明                        | 默认值                              |
|----------------|----------------------------|------------------------------------|
| `--data` / `-d` | JSON文件路径（必填）         | -                                  |
| `--output` / `-o` | 输出Excel路径（必填）       | -                                  |
| `--template` / `-t` | Excel模板名称             | 测试用例模板.xlsx                    |
| `--title`      | 工作表标题                   | 测试用例                             |
| `--template-key` | template-config.json中的key | default                             |

---

## 记忆管理脚本

```bash
# 初始化记忆
python scripts/memory_manager.py --action init --project .

# 读取记忆文件
python scripts/memory_manager.py --action read --project . --type user_preferences
python scripts/memory_manager.py --action read --project . --type generation_history

# 添加生成记录
python scripts/memory_manager.py --action add-record --project . --data '{"type":"test_case","source":"需求文档.docx","output":"testcases_xxx.xlsx","case_count":40,"coverage_rate":"100%"}'

# 记录歧义决策
python scripts/memory_manager.py --action add-ambiguity --project . --data '{"type":"BOUNDARY_UNCLEAR","context":"密码复杂度","original_text":"密码应有足够的复杂度","user_decision":"长度8-20位，必须包含大小写字母和数字"}'

# 查找相似歧义
python scripts/memory_manager.py --action find-ambiguity --project . --type BOUNDARY_UNCLEAR --context "密码"

# 设置用户偏好
python scripts/memory_manager.py --action set-pref --project . --key default_tag --value "C端"

# 清除所有记忆
python scripts/memory_manager.py --action clear --project .
```

---

## 模板支持

### 模板文件

`assets/` 目录预置了标准模板：

| 模板文件                   | 用途                     |
| ------------------------ | ------------------------ |
| `测试用例模板.xlsx`        | 标准功能测试用例 Excel 格式 |
| `template-config.json`   | 模板配置定义               |

### 使用方式

Excel 输出时使用 `测试用例模板.xlsx` 作为格式基准。

---

## 依赖库

确保本地 Python 环境已安装以下库：

| 库名            | 安装命令                      |
| --------------- | --------------------------- |
| `openpyxl`      | `pip install openpyxl`      |
| `python-docx`   | `pip install python-docx`   |
| `pypdf`         | `pip install pypdf`         |
| `markdown`      | `pip install markdown`      |

**执行脚本**：

```bash
python scripts/write_excel_from_json.py --data tmp/testcases.json --output testcases.xlsx
```

---

## 参考文档

| 文档                                | 说明             |
| --------------------------------- | ---------------- |
| `references/testcase-standard.md`       | 功能测试用例标准           |
| `references/MEMORY-SCHEMA.md`           | 记忆数据结构定义           |
| `references/INTERACTION-PATTERNS.md`    | 交互模式与问题模板         |
| `references/TRACEABILITY.md`            | 需求追溯矩阵与覆盖率计算   |

---

## 示例

### 示例1：根据PRD生成登录模块测试用例
1. 用户提供 PRD 文档
2. Phase 0 检测 `.memory/` 是否存在，不存在则初始化
3. Phase 1 读取 PRD 内容
4. Phase 2 加载记忆 → 解析需求 → 生成测试场景（等价类 + 边界值 + 场景法 + 错误推测）→ 去重
5. Phase 2.5 确认解析结果（无异常则自动继续）
6. Phase 2.8 质量预审
7. Phase 3 生成 JSON → 调用 `write_excel_from_json.py` 输出 Excel
8. Phase 4 更新记忆（写入生成历史、更新术语等）
9. 输出：`testcases_<时间戳>.xlsx` 在项目根目录

### 示例2：在线文档URL输入
1. 用户发送一个 URL
2. 自动抓取网页内容
3. 同上流程生成测试用例 Excel

---

## 目录结构

```
testcase-generator3/
├── .memory/                       # 持久化记忆（自动生成，勿手动修改）
│   ├── project-context.json
│   ├── terminology.json
│   ├── generation-history.json
│   ├── user-preferences.json
│   └── ambiguity-decisions.json
├── assets/                        # 模板资源
│   ├── template-config.json
│   └── 测试用例模板.xlsx
├── references/                    # 规范文档
│   ├── testcase-standard.md
│   └── MEMORY-SCHEMA.md
├── scripts/                       # 工具脚本
│   ├── write_excel_from_json.py
│   └── memory_manager.py
├── tmp/                           # 中间JSON文件（自动管理）
├── SKILL.md                       # Skill 定义文件
├── STAR.md                        # 启动入口文件
└── .gitignore
```

---


## 注意事项

1. **文档质量**：输入文档越完整，生成用例越准确
2. **人工评审**：生成后建议人工评审业务细节
3. **字段限制**：如有字段限制文档请一并提供
4. **用例筛选**：用触发词精准控制用例类型
5. **记忆持久化**：`.memory/` 文件夹自动管理，请勿手动修改
6. **时间戳格式**：文件命名中的 `<时间戳>` 必须使用 `YYYYmmddHHMMSS`（14 位）
