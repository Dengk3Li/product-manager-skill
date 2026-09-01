# Product Manager Skill

先把产品问题说清楚，再决定需要一段结论、一份简短方案，还是完整的发布控制。

Product Manager is an Agent Skill for turning ambiguous requests into clear product decisions without turning every change into a PRD.

## 项目背景

这个 Skill 来自 Personal AI OS 的内部开发实践。Personal AI OS 需要在多轮对话中处理产品规划、功能开发、长期任务和验收。随着项目变多，产品管理本身开始出现两个问题。

一是小任务经常被过度规划。改一个字段、补一个入口，也可能生成 PRD、WBS、依赖图、验收卡和多层审批。文档多了，真正需要决定的事反而更难找到。

二是大任务又容易失去边界。一个对话接手多个项目后，会把“想解决什么”“先做什么”“代码怎么拆”“任务怎么登记”混成一件事。结果往往是范围不断扩大，旧需求被新方案覆盖，产品经理也开始代替架构师和开发者做决定。

这个仓库把产品经理角色单独提取出来。它只负责产品决定：问题、目标、优先级、范围、非目标、发布边界和验收结果。私有项目内容没有进入本仓库。

## 它解决什么问题

Product Manager 会先判断当前还缺哪一个产品决定，再选择足够完成这次工作的最轻模式。

- 明确要改变的用户或业务结果；
- 区分必须做、可以晚做和明确不做的内容；
- 只有在真实协作关系存在时才拆分任务；
- 把验收写成可观察结果，而不是过程清单；
- 在产品问题已经解决时停止继续写文档；
- 把模块边界、编码和任务管理交给对应角色。

它的目标不是产出更多产品文档，而是减少尚未解决的产品分歧。

## 工作方式

```text
读取已有事实
  ↓
找出会改变结果、范围或发布决定的问题
  ↓
选择 Direct、Coordinated 或 Controlled
  ↓
给出决定、范围、非目标和验收
  ↓
把架构与实现交给对应角色
```

### Direct

这是默认模式。适合一个结果、一个修改范围、没有重要未决选择的工作。

输出只需要包括结果、范围、可观察验收和马上可以执行的动作。它不会为了显得完整而创建 PRD、WBS、依赖图或单独的 Gate。

例如：“把设置页的保存按钮改成提交。”如果文案和验收已经清楚，这是一项直接改动，不需要重新规划设置页。

### Coordinated

适合至少两个可以独立交付的结果，或确实存在多个负责人、并行分支、阻塞关系和汇合点的工作。

输出是一份简短产品说明和 L1/L2 拆分。只有拥有独立产物、负责人或验收边界的内容，才成为子任务。

例如：“新增研究看板，并导入旧项目历史。”看板与历史导入可以分别实现和验收，但必须约定数据接入顺序。这时需要协调，不需要把按钮、测试和样式继续拆成三级任务。

### Controlled

适合公开发布、数据迁移、隐私或安全、不可逆成本、权限变更、跨模块发布合同，以及多个写入者发生冲突的工作。

它会增加必要的权限边界、回滚办法和独立复核，但不会因为风险较高就自动制造一棵庞大的 WBS。一个边界清楚的高风险交付仍然可以是一项任务。

## 如何决定拆不拆

| 实际情况 | 处理方式 |
|---|---|
| 一个明确结果 | Direct，不建 WBS |
| 两个以上可独立交付的结果 | Coordinated，拆到 L1/L2 |
| 独立负责人、产物、验收和交接都成立 | 可以拆到 L3 |
| 真实存在并行、依赖、汇合或退出条件 | 补执行关系 |
| 只是测试、按钮、样式、风险说明或回执 | 留在交付内 |

这种判断来自一个简单标准：拆出来的内容是否真的可以单独排期、单独负责、单独验收。不能满足这个标准，就不把它包装成独立产品模块。

## 与其他角色的分工

| 角色 | 决定什么 | 交付什么 |
|---|---|---|
| 产品经理 | 为什么做、先做什么、做到哪里 | 产品决定、范围、非目标、验收结果 |
| 系统架构师 | 放在哪个模块、占多少界面、怎样连接 | 模块归属、文件边界、共享区域、接口合同 |
| 模块开发者 | 如何在边界内实现 | 代码、测试和验证结果 |
| 任务系统 | 如何持续跟踪和交接 | 经授权的任务状态和负责人 |

[System Architect Skill](https://github.com/Dengk3Li/system-architect-skill) 是配套角色。产品经理确认做什么；系统架构师决定它进入哪个模块，以及这个模块能修改什么。

## 提供的能力

### 从模糊请求中找出真正的决定

Skill 会先读取已有产品材料、代码、任务状态和历史决定，只询问会改变结果、范围或发布边界的问题。已经有答案的内容不要求用户再讲一遍。

### 选择合适的规划深度

Direct、Coordinated 和 Controlled 不是项目规模标签，而是三种不同的处理强度。小而高风险的公开发布可以是 Controlled；体量不小但边界已经明确的单模块开发仍然可以 Direct。

### 保持未知状态

权限、来源、完成状态、负责人或版本信息没有证据时，保留 `UNKNOWN`。产品文档不能用猜测填补这些字段。

### 及时退出产品讨论

目标、范围、非目标、验收和下一动作已经明确后，Skill 停止继续扩写。后续编码、验收和任务维护由相应流程处理。

## 安装

使用兼容 Agent Skills 的安装器安装完整的 `skills/product-manager` 目录。也可以把该目录复制到所用 Agent 工具的 skills 目录。

仓库根目录提供 Codex 插件清单：`.codex-plugin/plugin.json`。

安装后可以这样调用：

```text
Use $product-manager to decide whether this feature needs a PRD.
Use $product-manager to define the scope and acceptance for this release.
Use $product-manager to split this roadmap only where outputs are independently valuable.
```

## 适用范围

- 用户提出的是产品问题，但需求、优先级或发布范围还不清楚；
- 需要 PRD、路线图、功能拆分或版本范围；
- 多个结果需要分别排序、排期或验收；
- 风险会改变发布方式；
- 团队已经有很多任务材料，却缺少一项明确决定。

已经限定范围的编码、缺陷修复、材料整理、验收检查和任务卡维护，不需要重新触发产品规划。

## 仓库结构

```text
.codex-plugin/plugin.json
skills/product-manager/
  SKILL.md
  agents/openai.yaml
  references/component-versioning.md
  references/product-sources.md
tests/test_package.py
```

## 参考资料

这个 Skill 参考了以下公开方法，但没有复制任何一套完整流程：

- [GOV.UK: Start by learning user needs](https://www.gov.uk/service-manual/user-research/start-by-learning-user-needs)：先理解用户需要，再决定服务和功能。
- [Intercom: Start with the problem](https://www.intercom.com/blog/intercom-product-principles-start-with-the-problem/)：先判断问题是否值得解决，再讨论方案。
- [Intercom: Deliver outcomes](https://www.intercom.com/blog/product-principles-deliver-outcomes/)：用期望发生的变化描述目标，而不是只列功能。
- [SVPG: Four Big Risks](https://www.svpg.com/four-big-risks/)：分别检查价值、易用性、可行性和商业可持续性。
- [Basecamp Shape Up: Set Boundaries](https://basecamp.com/shapeup/1.2-chapter-03)：先确定愿意投入的时间，再在边界内调整范围。
- [Intercom: Keep it simple](https://www.intercom.com/blog/intercom-product-principles-keep-it-simple/)：选择足以解决问题的简单方案。
- [GOV.UK: Product manager](https://www.gov.uk/service-manual/the-team/product-manager)：产品经理负责愿景、策略、优先级，以及用户和组织需求之间的平衡。
- [Atlassian: Product requirements template](https://www.atlassian.com/software/confluence/templates/product-requirements)：提供目标、假设、用户故事、设计和未决问题的实用结构。

每项资料怎样转化为本 Skill 的规则，见 [product-sources.md](skills/product-manager/references/product-sources.md)。

## 开发与验证

运行包测试：

```bash
python3 -m unittest discover -s tests -v
```

检查 Skill 和插件结构：

```bash
python3 <skill-creator>/scripts/quick_validate.py skills/product-manager
python3 <plugin-creator>/scripts/validate_plugin.py .
```

这个仓库目前只包含 Markdown、YAML、JSON 和 Python 标准库测试，不需要安装运行依赖。

## License

仓库当前公开可见，但尚未授予开源许可证。
