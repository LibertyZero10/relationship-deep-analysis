# {{title}}

> 数据基底：{{meta.total_messages}}条消息 | {{meta.total_days}}天 | {{meta.date_range.start}} - {{meta.date_range.end}}
> 分析对象：{{party_a_name}}（{{meta.party_a.pct}}%） × {{party_b_name}}（{{meta.party_b.pct}}%）
> 分析方法：24个心理学框架 × 6个维度 × 量化数据采集 + 心理推演

---

## 数据概览

| 指标 | {{party_a_name}} | {{party_b_name}} |
|------|------------------|------------------|
| 消息数 | {{meta.party_a.messages}} ({{meta.party_a.pct}}%) | {{meta.party_b.messages}} ({{meta.party_b.pct}}%) |
| 中位消息长度 | {{additional.message_stats.a.median_length}}字 | {{additional.message_stats.b.median_length}}字 |
| 中位回复时间 | {{additional.response_time.a.median}}秒 | {{additional.response_time.b.median}}秒 |
| 活跃时段 | {{additional.time_of_day.peak_hour_a}} | {{additional.time_of_day.peak_hour_b}} |
| 深夜活跃占比 | {{additional.time_of_day.late_night_pct_a}}% | {{additional.time_of_day.late_night_pct_b}}% |
| 对话发起率 | {{additional.conversations.a_initiate_pct}}% | {{additional.conversations.b_initiate_pct}}% |
| 对话结束率 | {{additional.conversations.a_ends}} | {{additional.conversations.b_ends}} |

---

## A层：沟通模式分析

### A1. 戈特曼四骑士（Gottman's Four Horsemen）

> John Gottman发现四种沟通模式能以93%准确率预测关系终结。

**数据总览：**

| 骑士 | {{party_a_name}} | {{party_b_name}} | 总计 | A每千条 | B每千条 |
|------|-------|------|------|---------|---------|
| 批评(Criticism) | {{A1.criticism.a}} | {{A1.criticism.b}} | {{A1.criticism_total}} | {{A1.criticism.a_per_1k}} | {{A1.criticism.b_per_1k}} |
| 蔑视(Contempt) | {{A1.contempt.a}} | {{A1.contempt.b}} | {{A1.contempt_total}} | {{A1.contempt.a_per_1k}} | {{A1.contempt.b_per_1k}} |
| 防御(Defense) | {{A1.defense.a}} | {{A1.defense.b}} | {{A1.defense_total}} | {{A1.defense.a_per_1k}} | {{A1.defense.b_per_1k}} |
| 筑墙(Stonewalling) | {{A1.stonewall.a}} | {{A1.stonewall.b}} | {{A1.stonewall_total}} | {{A1.stonewall.a_per_1k}} | {{A1.stonewall.b_per_1k}} |

**蔑视/批评比值**（最强分手预测因子）：{{party_a_name}} {{A1.contempt_criticism_ratio_a}}，{{party_b_name}} {{A1.contempt_criticism_ratio_b}}。{{A1.contempt_warning}}

**戈特曼比率**（积极/消极互动）：
- {{party_a_name}}：{{A1.gottman_ratio_a}} → {{A1.gottman_status_a}}
- {{party_b_name}}：{{A1.gottman_ratio_b}} → {{A1.gottman_status_b}}
- 关系整体：{{A1.gottman_ratio_total}} → {{A1.gottman_status_total}}

{{A1.monthly_trend_section}}

**深度推演**：
{{A1.interpretation}}

### A2. 非暴力沟通（NVC）

> Marshall Rosenberg的NVC模型区分暴力与非暴力沟通。

| 类型 | {{party_a_name}} | {{party_b_name}} |
|------|-------|------|
| 暴力-评价代替观察 | {{A2.eval_judg.a}} | {{A2.eval_judg.b}} |
| 暴力-想法伪装感受 | {{A2.fake_feeling.a}} | {{A2.fake_feeling.b}} |
| 暴力-指责代替需要 | {{A2.blame_need.a}} | {{A2.blame_need.b}} |
| 暴力-命令代替请求 | {{A2.command.a}} | {{A2.command.b}} |
| **暴力小计** | **{{A2.violence_total_a}}** | **{{A2.violence_total_b}}** |
| 非暴力-纯观察 | {{A2.pure_obs.a}} | {{A2.pure_obs.b}} |
| 非暴力-真实感受 | {{A2.real_feeling.a}} | {{A2.real_feeling.b}} |
| 非暴力-表达需要 | {{A2.express_need.a}} | {{A2.express_need.b}} |
| 非暴力-明确请求 | {{A2.clear_request.a}} | {{A2.clear_request.b}} |
| **非暴力小计** | **{{A2.nvc_total_a}}** | **{{A2.nvc_total_b}}** |

**NVC成熟度**：{{party_a_name}} {{A2.maturity_a}}/10，{{party_b_name}} {{A2.maturity_b}}/10。{{A2.maturity_note}}

**深度推演**：
{{A2.interpretation}}

### A3. 交互分析（Transactional Analysis, PAC模型）

> Eric Berne的PAC模型：Parent（教导/批评）、Adult（理性/客观）、Child（情感/直觉）。

**PAC状态分布：**

| 状态 | {{party_a_name}} | {{party_a_name}}占比 | {{party_b_name}} | {{party_b_name}}占比 |
|------|-------|------|------|------|
| Parent (P) | {{A3.state_P.a}} | {{A3.pct_P_a}}% | {{A3.state_P.b}} | {{A3.pct_P_b}}% |
| Adult (A) | {{A3.state_A.a}} | {{A3.pct_A_a}}% | {{A3.state_A.b}} | {{A3.pct_A_b}}% |
| Child (C) | {{A3.state_C.a}} | {{A3.pct_C_a}}% | {{A3.state_C.b}} | {{A3.pct_C_b}}% |

**交易模式Top 5：**
{{A3.top_transactions}}

**交叉交易率**：{{A3.cross_rate}}%（冲突指标，>30%为高冲突）

**深度推演**：
{{A3.interpretation}}

### A4. 卡普曼戏剧三角（Drama Triangle）

> Stephen Karpman：迫害者、拯救者、受害者的角色循环。

| 角色 | {{party_a_name}} | {{party_b_name}} |
|------|-------|------|
| 迫害者(Persecutor) | {{A4.persecutor.a}} ({{A4.persecutor_pct_a}}%) | {{A4.persecutor.b}} ({{A4.persecutor_pct_b}}%) |
| 拯救者(Rescuer) | {{A4.rescuer.a}} ({{A4.rescuer_pct_a}}%) | {{A4.rescuer.b}} ({{A4.rescuer_pct_b}}%) |
| 受害者(Victim) | {{A4.victim.a}} ({{A4.victim_pct_a}}%) | {{A4.victim.b}} ({{A4.victim_pct_b}}%) |

**深度推演**：
{{A4.interpretation}}

---

## B层：心理结构分析

### B5. 图式治疗（Schema Therapy）

> Jeffrey Young的早期适应不良图式(EMS)。

**{{party_a_name}}的图式谱（按强度排序）：**

| 图式 | 频次 | 解读 |
|------|------|------|
{{B5.schema_table_a}}

**{{party_b_name}}的图式谱：**

| 图式 | 频次 | 解读 |
|------|------|------|
{{B5.schema_table_b}}

**深度推演**：
{{B5.interpretation}}

### B6. 心理防御机制（Defense Mechanisms）

> Anna Freud & George Vaillant的防御层次模型。

**{{party_a_name}}的防御层次：**
{{B6.defense_breakdown_a}}

**{{party_b_name}}的防御层次：**
{{B6.defense_breakdown_b}}

**深度推演**：
{{B6.interpretation}}

### B7. 内在小孩分析（Inner Child）

**退行行为频率：**
{{B7.data_table}}

**深度推演**：
{{B7.interpretation}}

### B8. 乔哈里窗（Johari Window）

**公开区**（双方都频繁讨论）：{{B8.public_summary}}

**隐藏区**（一方从未对另一方表达）：{{B8.hidden_summary}}

**未知区**（双方都回避的话题）：

| 话题 | {{party_a_name}} | {{party_b_name}} | 总计 | 状态 |
|------|-------|------|------|------|
{{B8.unknown_table}}

**深度推演**：
{{B8.interpretation}}

---

## C层：关系动力学分析

### C9. 关系辩证理论（Relational Dialectics）

**三对永恒张力：**

| 张力 | 数据 | 解读 |
|------|------|------|
| 自主vs连接 | {{C9.autonomy_connection}} | {{C9.autonomy_note}} |
| 新奇vs可预测 | {{C9.novelty_predictability}} | {{C9.novelty_note}} |
| 开放vs封闭 | {{C9.openness_closedness}} | {{C9.openness_note}} |

**深度推演**：
{{C9.interpretation}}

### C10. 社会交换理论（Social Exchange Theory）

| 维度 | {{party_a_name}} | {{party_b_name}} |
|------|-------|------|
| 深度消息(>50字) | {{C10.deep_messages.a}} | {{C10.deep_messages.b}} |
| 表达爱 | {{C10.love_expr.a}} | {{C10.love_expr.b}} |
| 表达想念 | {{C10.miss_expr.a}} | {{C10.miss_expr.b}} |
| 金钱净额 | {{C10.money_a}} | {{C10.money_b}} |

**深度推演**：
{{C10.interpretation}}

### C11. 五种权力基础（Five Bases of Power）

| 权力类型 | {{party_a_name}} | {{party_b_name}} |
|----------|-------|------|
| 奖励权力 | {{C11.reward.a}} | {{C11.reward.b}} |
| 强制权力 | {{C11.coercive.a}} | {{C11.coercive.b}} |
| 合法权力 | {{C11.legitimate.a}} | {{C11.legitimate.b}} |
| 参照权力 | {{C11.referent.a}} | {{C11.referent.b}} |
| 专家权力 | {{C11.expert.a}} | {{C11.expert.b}} |

**深度推演**：
{{C11.interpretation}}

### C12. 依恋多维模型（Attachment Model）

| 维度 | {{party_a_name}} | {{party_b_name}} |
|------|-------|------|
| 自我否定:肯定 | {{C12.self_ratio_a}} | {{C12.self_ratio_b}} |
| 不信任:信任 | {{C12.trust_ratio_a}} | {{C12.trust_ratio_b}} |
| 回避:趋近 | {{C12.avoid_ratio_a}} | {{C12.avoid_ratio_b}} |

**依恋四象限定位**：{{party_a_name}} → {{C12.attachment_type_a}} | {{party_b_name}} → {{C12.attachment_type_b}}

**深度推演**：
{{C12.interpretation}}

### C13. 戈特曼信任公式（Gottman Trust Formula）

| 维度 | 数据 | 评分 |
|------|------|------|
| 可预测性 | {{C13.predictability_data}} | {{C13.predictability_score}}/10 |
| 可依赖性 | {{C13.dependability_data}} | {{C13.dependability_score}}/10 |
| 信心-未来词频 | {{C13.faith_data_a}} | {{C13.faith_score_a}}/10 |
| 信心-未来词频 | {{C13.faith_data_b}} | {{C13.faith_score_b}}/10 |

**信任总分：{{C13.trust_total}}/10**

**深度推演**：
{{C13.interpretation}}

---

## D层：情感与需求分析

### D14. 自我决定理论（Self-Determination Theory）

| 需求 | {{party_a_name}} | {{party_b_name}} | 评估 |
|------|-------|------|------|
| 自主 | {{D14.autonomy_a}} | {{D14.autonomy_b}} | {{D14.autonomy_note}} |
| 胜任 | {{D14.competence_a}} | {{D14.competence_b}} | {{D14.competence_note}} |
| 关联 | {{D14.relatedness_a}} | {{D14.relatedness_b}} | {{D14.relatedness_note}} |

**深度推演**：
{{D14.interpretation}}

### D15. 情绪调节策略（Emotion Regulation）

| 策略 | {{party_a_name}} | {{party_b_name}} |
|------|-------|------|
| 压抑 | {{D15.suppression.a}} ({{D15.suppression_pct_a}}%) | {{D15.suppression.b}} ({{D15.suppression_pct_b}}%) |
| 表达 | {{D15.expression.a}} ({{D15.expression_pct_a}}%) | {{D15.expression.b}} ({{D15.expression_pct_b}}%) |
| 重评 | {{D15.reappraisal.a}} ({{D15.reappraisal_pct_a}}%) | {{D15.reappraisal.b}} ({{D15.reappraisal_pct_b}}%) |
| 回避 | {{D15.avoidance.a}} ({{D15.avoidance_pct_a}}%) | {{D15.avoidance.b}} ({{D15.avoidance_pct_b}}%) |

**深度推演**：
{{D15.interpretation}}

### D16. 马斯洛需求层次（Maslow's Hierarchy）

| 层次 | {{party_a_name}} | {{party_b_name}} |
|------|-------|------|
| 生理需求 | {{D16.physiological.a}} ({{D16.physiological_pct_a}}%) | {{D16.physiological.b}} ({{D16.physiological_pct_b}}%) |
| 安全需求 | {{D16.safety.a}} ({{D16.safety_pct_a}}%) | {{D16.safety.b}} ({{D16.safety_pct_b}}%) |
| 归属与爱 | {{D16.love_belonging.a}} ({{D16.love_belonging_pct_a}}%) | {{D16.love_belonging.b}} ({{D16.love_belonging_pct_b}}%) |
| 尊重需求 | {{D16.esteem.a}} ({{D16.esteem_pct_a}}%) | {{D16.esteem.b}} ({{D16.esteem_pct_b}}%) |
| 自我实现 | {{D16.self_actual.a}} ({{D16.self_actual_pct_a}}%) | {{D16.self_actual.b}} ({{D16.self_actual_pct_b}}%) |

**深度推演**：
{{D16.interpretation}}

### D17. 九型人格关系动态（Enneagram）

**{{party_a_name}}疑似类型**：{{D17.type_a}}（{{D17.type_a_count}}次）
- 关键词：{{D17.type_a_keywords}}
- **{{party_a_name}} = {{D17.full_type_a}}**

**{{party_b_name}}疑似类型**：{{D17.type_b}}（{{D17.type_b_count}}次）
- 关键词：{{D17.type_b_keywords}}
- **{{party_b_name}} = {{D17.full_type_b}}**

**类型互动**：{{D17.interaction}}

**深度推演**：
{{D17.interpretation}}

---

## E层：暗黑面与病理分析

### E18. 煤气灯效应检测（Gaslighting Detection）

| 类型 | {{party_a_name}} | {{party_b_name}} |
|------|-------|------|
| 制造困惑 | {{E18.confuse.a}} | {{E18.confuse.b}} |
| 否认说过 | {{E18.deny_said.a}} | {{E18.deny_said.b}} |
| 扭曲记忆 | {{E18.twist_memory.a}} | {{E18.twist_memory.b}} |
| 淡化感受 | {{E18.minimize_feelings.a}} | {{E18.minimize_feelings.b}} |
| 转移责任 | {{E18.shift_blame.a}} | {{E18.shift_blame.b}} |
| **总计** | **{{E18.total_a}}** | **{{E18.total_b}}** |

**阶段判定**：{{E18.stage}}

**深度推演**：
{{E18.interpretation}}

### E19. 创伤绑定深度评估（Trauma Bond Assessment）

| 维度 | 数据 | 评分 |
|------|------|------|
| 间歇强化 | {{E19.intermittent_data}} | {{E19.intermittent_score}}/10 |
| 权力不对等 | {{E19.power_data}} | {{E19.power_score}}/10 |
| 情绪极化 | {{E19.polarization_data}} | {{E19.polarization_score}}/10 |
| 分手-复合循环 | {{E19.cycle_data}} | {{E19.cycle_score}}/10 |

**创伤绑定总分：{{E19.total_score}}/10 —— {{E19.severity}}**

**深度推演**：
{{E19.interpretation}}

### E20. 沉默对待作为武器（Silent Treatment as Weapon）

| 类型 | 次数 | 比例 |
|------|------|------|
| 惩罚性沉默（>6h，无解释） | {{E20.punitive.count}} | {{E20.punitive_ratio}}% |
| 保护性沉默（>6h，有解释） | {{E20.protective.count}} | {{E20.protective_ratio}}% |

**深度推演**：
{{E20.interpretation}}

### E21. 关系成瘾/共依赖（Codependency）

| 维度 | {{party_a_name}} | {{party_b_name}} |
|------|-------|------|
| 控制行为 | {{E21.control_behaviors.a}} | {{E21.control_behaviors.b}} |
| 否认需求 | {{E21.deny_needs.a}} | {{E21.deny_needs.b}} |
| 过度负责 | {{E21.over_responsible.a}} | {{E21.over_responsible.b}} |
| 自我价值依赖 | {{E21.self_worth_dep.a}} | {{E21.self_worth_dep.b}} |
| 边界模糊 | {{E21.boundary_blur.a}} | {{E21.boundary_blur.b}} |
| **总计** | **{{E21.total_a}}** | **{{E21.total_b}}** |

**深度推演**：
{{E21.interpretation}}

---

## F层：行为模式分析

### F22. 习惯回路分析（Habit Loop）

**核心习惯循环1：追逐-回避循环**
- 线索(Cue)：{{party_a_name}}不回复/消失
- 惯例(Routine)：{{party_b_name}}刷屏追问（{{F22.chase_sequences.b}}次追逐序列，平均{{F22.chase_avg_msgs.b}}条/次）
- 奖赏(Reward)：{{party_a_name}}最终回复→{{party_b_name}}获得安全感
- **破坏性：{{F22.chase_destructiveness}}/10**

**核心习惯循环2：争吵-消失-和好循环**
- 线索：争吵信号
- 惯例：{{party_a_name}}消失（{{F22.fight_disappear}}次在争吵后消失>2h）
- 奖赏：{{party_b_name}}道歉/挽留→和好
- **破坏性：{{F22.fight_destructiveness}}/10**

**深度推演**：
{{F22.interpretation}}

### F23. 行为激活/抑制系统（BIS/BAS）

| 系统 | {{party_a_name}} | {{party_b_name}} |
|------|-------|------|
| BIS（抑制/回避） | {{F23.bis.a}} | {{F23.bis.b}} |
| BAS（激活/趋近） | {{F23.bas.a}} | {{F23.bas.b}} |
| BIS:BAS | {{F23.ratio_a}} | {{F23.ratio_b}} |

**深度推演**：
{{F23.interpretation}}

### F24. 关系韧性量表（Gottman Sound Relationship House）

| 层次 | 评分 | 解读 |
|------|------|------|
| 1. 爱情地图 | {{F24.love_maps_score}}/10 | {{F24.love_maps_note}} |
| 2. 表达喜爱与欣赏 | {{F24.fondness_score}}/10 | {{F24.fondness_note}} |
| 3. 转向对方 | {{F24.turning_score}}/10 | {{F24.turning_note}} |
| 4. 正面视角 | {{F24.positive_score}}/10 | {{F24.positive_note}} |
| 5. 冲突管理 | {{F24.repair_score}}/10 | {{F24.repair_note}} |
| 6. 支持梦想 | {{F24.support_score}}/10 | {{F24.support_note}} |
| 7. 共同意义 | {{F24.shared_score}}/10 | {{F24.shared_note}} |

**整体韧性评分：{{F24.total_score}}/10 —— {{F24.severity}}**

**深度推演**：
{{F24.interpretation}}

---

## 情感爆发分析

> 情感爆发 = 连续≥5条含负面情绪词的消息序列。爆发强度 = 消息数 × 平均负面词密度。

| 指标 | {{party_a_name}} | {{party_b_name}} |
|------|-------|------|
| 爆发次数 | {{bursts.a_count}} | {{bursts.b_count}} |
| 平均强度 | {{bursts.a_avg_intensity}} | {{bursts.b_avg_intensity}} |
| 平均长度 | {{bursts.a_avg_length}} | {{bursts.b_avg_length}} |

**Top 5 最强爆发事件：**
{{bursts.top_5_table}}

---

## 跨框架相关矩阵

> 基于月度时间序列的Pearson相关系数，|r| > 0.5的强相关对。

{{correlations.table}}

**关键发现**：{{correlations.key_findings}}

---

## 月度趋势分析

> 关键指标随时间变化趋势。趋势方向比静态聚合值更有预测力。

{{monthly_trends.table}}

**趋势解读**：{{monthly_trends.interpretation}}

---

## 综合诊断

### 关系本质判断

{{diagnosis.essence}}

**三个核心特征：**

1. **{{diagnosis.feature_1_title}}**
   {{diagnosis.feature_1_detail}}

2. **{{diagnosis.feature_2_title}}**
   {{diagnosis.feature_2_detail}}

3. **{{diagnosis.feature_3_title}}**
   {{diagnosis.feature_3_detail}}

### 核心矛盾清单
{{diagnosis.contradictions}}

### 双方各自需要疗愈的

**{{party_a_name}}需要：**
{{diagnosis.healing_a}}

**{{party_b_name}}需要：**
{{diagnosis.healing_b}}

### 关系走向预测

基于戈特曼研究的数据预测：

{{diagnosis.prediction}}

---

## 附录：24框架数据速览

| # | 框架 | 层 | 核心指标 | 评估 |
|---|------|----|---------|------|
| 1 | 戈特曼四骑士 | A | {{summary.A1}} | {{summary.A1_status}} |
| 2 | 非暴力沟通 | A | {{summary.A2}} | {{summary.A2_status}} |
| 3 | 交互分析PAC | A | {{summary.A3}} | {{summary.A3_status}} |
| 4 | 戏剧三角 | A | {{summary.A4}} | {{summary.A4_status}} |
| 5 | 图式治疗 | B | {{summary.B5}} | {{summary.B5_status}} |
| 6 | 防御机制 | B | {{summary.B6}} | {{summary.B6_status}} |
| 7 | 内在小孩 | B | {{summary.B7}} | {{summary.B7_status}} |
| 8 | 乔哈里窗 | B | {{summary.B8}} | {{summary.B8_status}} |
| 9 | 关系辩证 | C | {{summary.C9}} | {{summary.C9_status}} |
| 10 | 社会交换 | C | {{summary.C10}} | {{summary.C10_status}} |
| 11 | 权力基础 | C | {{summary.C11}} | {{summary.C11_status}} |
| 12 | 依恋模型 | C | {{summary.C12}} | {{summary.C12_status}} |
| 13 | 信任公式 | C | {{summary.C13}} | {{summary.C13_status}} |
| 14 | 自我决定 | D | {{summary.D14}} | {{summary.D14_status}} |
| 15 | 情绪调节 | D | {{summary.D15}} | {{summary.D15_status}} |
| 16 | 马斯洛 | D | {{summary.D16}} | {{summary.D16_status}} |
| 17 | 九型人格 | D | {{summary.D17}} | {{summary.D17_status}} |
| 18 | 煤气灯效应 | E | {{summary.E18}} | {{summary.E18_status}} |
| 19 | 创伤绑定 | E | {{summary.E19}} | {{summary.E19_status}} |
| 20 | 沉默武器 | E | {{summary.E20}} | {{summary.E20_status}} |
| 21 | 共依赖 | E | {{summary.E21}} | {{summary.E21_status}} |
| 22 | 习惯回路 | F | {{summary.F22}} | {{summary.F22_status}} |
| 23 | BIS/BAS | F | {{summary.F23}} | {{summary.F23_status}} |
| 24 | 关系韧性 | F | {{summary.F24}} | {{summary.F24_status}} |

---

*本报告基于{{meta.total_messages}}条聊天记录的量化分析，所有结论为基于数据的心理推演，非临床诊断。*
*分析工具：relationship-deep-analysis skill v2.0 | scripts/run_analysis.py*
