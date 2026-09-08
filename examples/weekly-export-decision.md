# Weekly support export / 每周工单导出

Illustrative scenario, not a customer case or a measured business result.
虚构场景，用于说明输出方式，不代表客户案例或已测得的业务收益。

## Request / 输入

A support team wants a weekly CSV of unresolved tickets, filtered by owner, status, and update date. Those fields already exist in its database. The proposed solution is an AI agent that prepares the report.

客服团队需要每周导出未解决工单，按负责人、状态和更新时间筛选。数据库已有这些字段，最初提出的方案是让 AI Agent 生成报告。

## Decision / 决定

Start with **NO_AI**: saved filters and a CSV export meet the stated outcome. Add AI only if a later need involves interpreting free-text messages and evidence shows that interpretation improves the workflow.

第一版采用 **NO_AI**：保存筛选条件并导出 CSV，满足当前目标。后续确实需要理解自由文本，且有证据表明它能改善工作流程时，再评估 AI。

## First release / 首版范围

- Select owner, status, and date range; preview the matching ticket count.
- Download the matching tickets with stable column names and an explicit reporting timezone.
- Explain an empty result and allow filters to be adjusted.

- 选择负责人、状态和日期范围，预览符合条件的工单数量。
- 下载对应记录，保持列名稳定，并明确报表时区。
- 没有结果时说明当前状态，并允许调整条件。

Automatic classification, drafted replies, and external email delivery are outside this release. Scheduling can follow after the manual export is useful and the schedule and destination are established.

自动分类、代写回复和对外发送邮件不属于首版。手动导出有用后，在明确计划和目标位置的基础上增加定时执行。

## Acceptance / 验收

Each exported row matches the selected filters; displayed and exported counts agree; date boundaries use the stated timezone; an empty result produces a clear state rather than a misleading success message. Record actual checks when they are run. These criteria are not a claim that this example implements or has tested an export service.

导出记录符合筛选条件，预览与导出数量一致，日期边界使用约定时区，空结果有清楚说明。执行检查后记录实际证据；这些标准不表示本示例已经实现或测试了导出服务。
