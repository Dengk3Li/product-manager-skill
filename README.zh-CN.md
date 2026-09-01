# Product Manager Skill

[English](README.md) | 简体中文

[![CI](https://github.com/Dengk3Li/product-manager-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/Dengk3Li/product-manager-skill/actions/workflows/ci.yml)

一个把模糊产品请求整理成明确范围和验收结果的 Agent Skill。它不会为每项改动都生成一份 PRD。

## 快速开始

使用通用 Skills CLI 安装：

```bash
npx skills add Dengk3Li/product-manager-skill --skill product-manager
```

安装后可以这样调用：

```text
Use $product-manager to decide whether this request needs a PRD.
Use $product-manager to define the scope and acceptance for this release.
Use $product-manager to split this roadmap only where outputs are independently valuable.
```

Skill 会选择一种规划模式，写出解决当前决定所需的最小材料，并在实现可以开始时停止产品讨论。

## 它能做什么

Product Manager 帮助 Agent：

- 找到请求背后的用户结果或业务结果；
- 区分必须完成、可以延后和明确不做的范围；
- 根据真实协作关系选择规划深度；
- 把验收写成可以观察的结果；
- 权限、负责人、来源或发布状态未经确认时保留 `UNKNOWN`；
- 把架构、编码和任务维护交给对应角色。

它用于解决产品决定，不是一套包办所有工作的项目管理框架。

## 为什么需要这个 Skill

编码 Agent 处理产品工作时，常出现两种相反的问题。

一种是过度规划。一个已经明确的小改动，也可能产生完整 PRD、多级 WBS、风险 Gate、任务卡和多份评审材料。规划成本很快超过改动本身。

另一种是提前实现。面对宽泛请求，Agent 还没有确认目标、发布边界和非目标，就开始修改代码。产品决定、架构决定和交付动作随之混在一起，范围不断扩大。

这个 Skill 按决定的复杂度增加结构。只有真实产品分歧、独立交付结果或已经确认的风险，才会带来更多规划材料。

## 三种规划模式

| 模式 | 适用情况 | 常见输出 |
|---|---|---|
| **Direct** | 一个明确结果、一个修改范围，没有重要产品问题待决定 | 结果、范围、验收、下一动作 |
| **Coordinated** | 两个以上可独立交付的结果、多个负责人或真实依赖 | 简短产品说明、L1/L2 拆分、真实依赖 |
| **Controlled** | 公开发布、数据迁移、安全、隐私、权限变化、破坏性操作或写入冲突 | 产品决定，以及必要的控制、复核和回滚 |

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

公开发布和持久数据迁移改变了发布边界，因此 Skill 会选择 **Controlled**。负责人、回滚和独立复核会进入交付要求，任务拆分仍以真实产物为准。

## 工作方式

1. 阅读已有产品材料、代码、任务状态和历史决定。
2. 找出会改变结果、范围、验收或发布方式的未决问题。
3. 只询问能够改变这项决定的信息。
4. 选择 Direct、Coordinated 或 Controlled。
5. 给出决定，然后退出产品讨论。

只有产品目标或发布边界发生实质变化时，才重新进入产品规划。

## 角色边界

| 角色 | 负责内容 |
|---|---|
| 产品经理 | 问题、优先级、范围、非目标、发布边界、验收 |
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
- 已经有许多任务材料，但仍缺少明确产品决定。

以下工作不需要重新触发产品规划：

- 范围明确的编码；
- 常规缺陷修复；
- 文档整理；
- 验收检查；
- 任务卡维护；
- 分支或 worktree 生命周期操作。

## 仓库内容

```text
.codex-plugin/plugin.json
skills/product-manager/
  SKILL.md
  agents/openai.yaml
  references/component-versioning.md
  references/product-sources.md
tests/test_package.py
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

每项资料怎样转化为具体规则，见 [product-sources.md](skills/product-manager/references/product-sources.md)。

## 开发与验证

运行测试：

```bash
python3 -m unittest discover -s tests -v
```

检查 Skill 和插件清单：

```bash
python3 <skill-creator>/scripts/quick_validate.py skills/product-manager
python3 <plugin-creator>/scripts/validate_plugin.py .
```

除兼容 Agent Skills 的宿主外，这个包没有其他运行依赖。

## License

仓库公开可见，但目前没有授予开源许可证。
