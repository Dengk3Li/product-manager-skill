# Product Manager Skill Suite

[English](README.md) | 简体中文

[![CI](https://github.com/Dengk3Li/product-manager-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/Dengk3Li/product-manager-skill/actions/workflows/ci.yml)

一组把客户证据和业务目标连接到产品决定、分层需求、路线图、交付覆盖与结果反馈的 Agent Skill；技术架构仍由架构师负责。

## 快速开始

使用通用 Skills CLI 安装：

```bash
npx skills add Dengk3Li/product-manager-skill --skill product-manager
npx skills add Dengk3Li/product-manager-skill --skill product-roadmap
npx skills add Dengk3Li/product-manager-skill --skill product-requirements
```

安装后可以这样调用：

```text
Use $product-manager to decide whether this request needs a PRD.
Use $product-manager to define the scope and acceptance for this release.
Use $product-manager to split this roadmap only where outputs are independently valuable.
Use $product-roadmap to create an evidence-based Now/Next/Later roadmap.
Use $product-requirements to approve one requirement baseline, trace delivery automatically, and ask me only for material decisions.
```

入口 Skill 负责产品逻辑，并在需要时把路线图或需求追溯交给对应的伴生 Skill。

实现阶段可以这样检查需求模型。警告会进入报告，不会中断其他工作：

```bash
python3 skills/product-requirements/scripts/check_requirements_traceability.py \
  requirements-traceability.json --phase delivery
```

## 它能做什么

Product Manager 帮助 Agent：

- 连接客户证据、商业背景、产品战略和目标结果；
- 找到请求背后的用户结果或业务结果；
- 在承诺方案前比较客户机会和替代路径；
- 区分必须完成、可以延后和明确不做的范围；
- 用证据、置信度、风险和机会成本说明优先级；
- 生成不虚构日期、可供业务方讨论的路线图；
- 给需求稳定 ID、层级、支撑关系和可观察的验收标准；
- 按已批准需求审计实现覆盖、阻塞、验证和人工验收；
- 发布后用真实结果重新审视产品假设；
- 权限、负责人、来源或发布状态未经确认时保留 `UNKNOWN`；
- 把架构、编码和任务维护交给对应角色。

它用于解决产品决定，不是一套包办所有工作的项目管理框架。

## 我们在解决什么

编码 Agent 经常从一句混合了业务目标、功能设想和实现猜测的话直接开工。代码可能已经完成，却没有解决原始问题。项目继续推进后，也很难回答某个模块对应哪项需求、某条支撑性需求为什么存在。

常见的修正方式又会制造审核负担：每个条目都有状态、Gate、人工批准和人工验收。人类花时间审核 Agent 生成的过程记录，却没有把精力留给真正的产品判断。

这套 Skill 保留从业务结果、产品需求到实现证据的责任链。人类只批准一次需求基线。Agent 维护需求层级、支撑关系、模块映射、交付状态、证据和阻塞摘要。只有范围、优先级、风险、成本、用户体验或最终验收需要判断时，工作才回到人类。

明确的小改动继续直接执行。多模块或跨阶段工作获得足够的追溯能力，但不会多出一套平行项目管理系统。

## 人类需要审核什么

| 时点 | 人类负责 | Agent 负责 |
|---|---|---|
| 重要工作开工前 | 批准一次需求基线，决定仍然开放的关键问题 | 查找事实、整理层级和支撑关系，只提出会改变产品承诺的问题 |
| 实现过程中 | 决定范围或产品含义的变化 | 自动维护模块映射、证据、覆盖情况和阻塞摘要 |
| 模块或版本验收 | 判断最终业务结果 | 用测试、运行观察和合同核对必须满足的标准 |

支撑性需求默认继承基线和版本验收。只有它引入独立的产品后果时，才需要单独判断。

## 三种规划模式

| 模式 | 适用情况 | 常见输出 |
|---|---|---|
| **Direct** | 一个明确结果、一个修改范围，没有重要产品问题待决定 | 结果、范围、验收、下一动作 |
| **Coordinated** | 两个以上可独立交付的结果、多个负责人或真实依赖 | 简短产品说明、L1/L2 拆分、真实依赖 |
| **Controlled** | 隐私、合规、公开发布、不可逆成本或用户信任后果 | 决策权、产品风险、发布边界和验收证据 |

Controlled 不代表必须拆得更深。一个边界清楚的高风险交付仍然可以是一项任务。

## 使用例子

### 让小改动保持简单

```text
把设置页的“保存”按钮改成“提交”，顺便写一份完整 PRD、三级 WBS、
风险 Gate 和任务卡。
```

Skill 会选择 **Direct**。范围只包含按钮文案，原有保存行为保持不变，并增加一项最小验收。额外材料不能解决新的产品决定，因此不会创建。

### 协调可以独立交付的结果

```text
新增研究看板，并导入旧项目历史。
```

看板和历史导入可以分别开发和验收。Skill 会选择 **Coordinated**，用一份简短说明记录两项交付，以及它们之间真实存在的数据或顺序依赖。

### 为风险增加控制，但不制造庞大 WBS

```text
公开发布这份数据集，并把现有用户数据迁移到新结构。
```

公开发布和持久数据迁移改变了产品承诺，因此 Skill 会选择 **Controlled**。它会明确决策权、用户与业务风险、发布边界和放行证据，再把技术控制交给对应流程。

## 工作方式

1. 阅读客户、产品、业务、路线图、交付和历史决定证据。
2. 明确目标客户、问题、预期结果、业务价值、约束和一份可审核的需求基线。
3. 比较客户机会和替代方案，识别最危险的假设。
4. 推荐方向并塑造最小有效发布。
5. 一次性批准基线，把模块落点和接口交给系统架构师。
6. 实现期间由 Agent 自动维护需求覆盖、证据和阻塞摘要。
7. 核对必须满足的结果，请人类完成一次模块或版本验收，再根据上线结果复盘产品假设。

需求检查器提供 `report`、`align`、`delivery` 和 `acceptance` 四个阶段。结构矛盾始终阻塞；实现阶段的证据缺口通常只警告；正式验收只阻塞必须验证但尚未验证的结果，以及缺少版本级人工决定的情况。

## 角色边界

| 角色 | 负责内容 |
|---|---|
| 产品经理 | 问题、优先级、范围、非目标、发布边界、验收 |
| 产品路线图 | 战略到结果的顺序、时间区间、置信度和路线图反馈 |
| 产品需求 | 一次批准的基线、需求层级、自动交付追溯、异常反馈和版本级验收 |
| 系统架构师 | 模块落点、页面占比、文件归属、共享区域、接口 |
| 开发者 | 在约定边界内完成代码和测试 |
| 任务系统 | 经授权的跟踪、分配和跨会话交接 |

产品讨论本身不授权创建任务或修改代码。

模块归属和整合接口由配套的 [System Architect Skill](https://github.com/Dengk3Li/system-architect-skill) 处理。

## 适用场景

适合：

- 需求仍然模糊；
- 需要 PRD、路线图、优先级或版本范围；
- 多项结果需要分别排期或验收；
- 风险会改变发布方式；
- 开工前需要对齐需求，或模块完成后需要核对覆盖与阻塞；
- 已经有许多任务材料，但仍缺少明确产品决定。

以下工作不需要重新触发产品规划：

- 范围明确的编码；
- 常规缺陷修复；
- 文档整理；
- 不需要读取需求基线的独立验收检查；
- 任务卡维护；
- 分支或 worktree 生命周期操作。

## 仓库内容

```text
.codex-plugin/plugin.json
skills/product-manager/
  SKILL.md
  agents/openai.yaml
  references/product-sources.md
skills/product-roadmap/
  SKILL.md
  agents/openai.yaml
  references/roadmap-method.md
skills/product-requirements/
  SKILL.md
  agents/openai.yaml
  assets/requirements-traceability.template.json
  references/requirements-model.md
  scripts/check_requirements_traceability.py
tests/test_package.py
tests/test_requirements_traceability.py
```

`SKILL.md` 是 Agent 运行时读取的指令。仓库 README 面向评估和安装这个 Skill 的使用者。

## 参考资料

规则参考了以下公开方法：

- [GOV.UK：从用户需求开始](https://www.gov.uk/service-manual/user-research/start-by-learning-user-needs)
- [Intercom：从问题开始](https://www.intercom.com/blog/intercom-product-principles-start-with-the-problem/)
- [Intercom：交付结果](https://www.intercom.com/blog/intercom-product-principles-deliver-outcomes/)
- [SVPG：四类产品风险](https://www.svpg.com/four-big-risks/)
- [Basecamp Shape Up：设置边界](https://basecamp.com/shapeup/1.2-chapter-03)
- [Intercom：保持简单](https://www.intercom.com/blog/intercom-product-principles-keep-it-simple/)
- [GOV.UK：产品经理职责](https://www.gov.uk/service-manual/the-team/product-manager)
- [Atlassian：产品需求模板](https://www.atlassian.com/software/confluence/templates/product-requirements)
- [Atlassian：敏捷产品路线图](https://www.atlassian.com/agile/product-management/roadmaps)
- [Atlassian：产品发现](https://www.atlassian.com/agile/product-management/discovery)
- [Product Talk：发现解决方案](https://www.producttalk.org/discovering-solutions/)

每项资料怎样转化为具体规则，见 [product-sources.md](skills/product-manager/references/product-sources.md)。

## 开发与验证

运行测试：

```bash
python3 -m unittest discover -s tests -v
```

检查 Skill 和插件清单：

```bash
python3 <skill-creator>/scripts/quick_validate.py skills/product-manager
python3 <skill-creator>/scripts/quick_validate.py skills/product-requirements
python3 <plugin-creator>/scripts/validate_plugin.py .
```

除兼容 Agent Skills 的宿主外，这个包没有其他运行依赖。

## License

仓库公开可见，但目前没有授予开源许可证。
