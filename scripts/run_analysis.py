#!/usr/bin/env python3
"""
Relationship Deep Analysis - 24 Framework Data Collection Script
Version: 2.0.0

Usage:
    python run_analysis.py <json_path> [options]

Options:
    --output, -o       Output JSON file path (default: <input>_analysis.json)
    --sender-a NAME    Sender A (user) identifier
    --sender-b NAME    Sender B (partner) identifier
    --quiet            Only save JSON, no console output

Features:
    - 24 psychology frameworks in one pass
    - Monthly trends for key metrics
    - Per-1k-message normalization
    - Emotional burst detection
    - Cross-framework correlation matrix
    - Response time, conversation, time-of-day analysis

Self-contained: only Python stdlib required.
"""

import json, re, sys, os, argparse, math, statistics
from datetime import datetime
from collections import defaultdict, Counter

# ============================================================================
# PATTERN LIBRARY - All 24 frameworks
# ============================================================================

# --- A1: Gottman Four Horsemen ---
A1 = {
    'criticism': [r'你就是.*的人', r'你总是', r'你从来不', r'你每次都',
        r'你这种人', r'你永远', r'你根本', r'你就是个',
        r'你从来不知道', r'你从来不会', r'你从来不懂', r'你一直'],
    'contempt': [r'呵呵', r'可笑', r'搞笑', r'弱智', r'白痴', r'神经病',
        r'你有病', r'你配吗', r'你也配', r'就你', r'得了吧',
        r'^切$', r'^算了吧$', r'随你', r'爱咋咋', r'懒得理你',
        r'你算什么', r'什么东西', r'不要脸', r'厚脸皮', r'丢人', r'丢脸', r'恶心'],
    'defense': [r'我不是', r'我没有', r'你冤枉', r'你误会',
        r'你自己不也', r'你不也一样', r'你管好自己', r'怪我咯',
        r'我又不是', r'关我什么事', r'又不是我', r'我也没办法',
        r'我又不是故意的', r'我也想啊'],
    'stonewall_exact': ['嗯','哦','好','行','嗯嗯','嗯呐','哦哦','好吧',
        '知道了','收到了','没事','没什么','不想说','随你','随便','无所谓'],
    'positive_kw': ['爱','想','宝贝','老婆','老公','乖','好棒','厉害',
        '谢谢','辛苦','心疼','抱抱','拥抱','亲','可爱','开心','幸福','快乐',
        '早安','晚安','吃饭了吗','注意安全','加油'],
    'negative_kw': ['生气','烦','滚','分手','哭','难过','累','不想','讨厌','恨',
        '气','崩溃','绝望','死','滚开','闭嘴','够了']
}

# --- A2: NVC ---
A2 = {
    'eval_judg': [r'你总是', r'你从来不', r'你每次都', r'你就是.*人',
        r'你永远', r'你根本', r'你就是个', r'你从来不懂', r'太.*了$', r'每次都'],
    'fake_feeling': [r'我觉得你', r'我觉得他', r'我觉得你不', r'我觉得他不',
        r'感觉你.*不在乎', r'感觉你.*不.*我', r'觉得你.*不爱', r'觉得你.*不在乎'],
    'blame_need': [r'你就是不.*我', r'你根本不.*我', r'你从来.*不.*我',
        r'都是你的错', r'都怪你', r'你害', r'因为你'],
    'command': [r'你必须', r'你给我', r'你不准', r'你不许', r'你一定要',
        r'你马上', r'你立刻', r'不准.*', r'你必须.*听'],
    'pure_obs': [r'\d+点', r'今天.*次', r'这周.*次', r'刚才', r'昨天', r'上次', r'那天'],
    'real_feeling': [r'我感到', r'我.*开心', r'我.*难过', r'我.*生气', r'我.*害怕',
        r'我.*焦虑', r'我.*委屈', r'我.*失望', r'我.*心疼', r'我.*累', r'我.*孤独'],
    'express_need': [r'我需要', r'我希望', r'我想要', r'我渴望', r'我期待'],
    'clear_request': [r'能不能', r'可不可以', r'你.*好吗', r'你.*行吗',
        r'我们.*好不好', r'下次.*好不好']
}

# --- A3: PAC (Transactional Analysis) ---
A3 = {
    'parent_p': [r'你应该', r'你不应该', r'你怎么又', r'跟你说了', r'叫你.*不听',
        r'让你.*你不', r'你要.*知道', r'你必须', r'不准', r'不许',
        r'你要听话', r'乖', r'听话', r'记住', r'我跟你讲', r'听我的',
        r'你要明白', r'你要懂得', r'你得',
        r'帮你', r'我来帮你', r'我来教', r'让我来', r'我给你',
        r'注意身体', r'多穿', r'记得吃', r'早点睡', r'别熬夜',
        r'按时吃', r'天冷', r'加衣服', r'路上小心',
        r'到家.*说', r'到了.*说', r'到家了吗', r'吃饭了吗', r'吃了吗',
        r'在干嘛', r'去哪了', r'跟谁', r'几点.*回', r'回来.*告诉我'],
    'adult_a': [r'多少钱', r'几点', r'在哪', r'什么时候', r'怎么去',
        r'你说的.*是', r'我理解', r'我认为', r'事实上', r'实际情况',
        r'具体.*情况', r'分析', r'方案', r'计划', r'安排', r'确认',
        r'需要.*信息', r'关于.*问题', r'从.*角度', r'逻辑', r'理性', r'客观'],
    'child_c': [r'我好.*', r'我不要', r'我不嘛', r'你陪我', r'呜呜', r'哼',
        r'啦啦', r'嘻嘻', r'嘿嘿', r'哈哈',
        r'好开心', r'好难过', r'好害怕', r'好紧张', r'好激动',
        r'我害怕', r'我开心', r'我难过', r'我想你', r'我要',
        r'我要.*嘛', r'求求', r'好不好嘛', r'可以吗', r'行不行',
        r'我要.*你', r'我不管', r'我就要', r'我偏要', r'我不听', r'我不看', r'我不理',
        r'讨厌', r'^哼$', r'嘛$', r'呀$', r'呢$', r'啦$']
}

# --- A4: Drama Triangle ---
A4 = {
    'persecutor': [r'你总是', r'你从来不', r'你每次都', r'你就是.*人', r'你永远',
        r'你根本', r'都是你的错', r'都怪你', r'你害',
        r'你能不能.*别', r'你能不能.*不要', r'不要.*了', r'别.*了',
        r'你烦不烦', r'你够了', r'滚', r'闭嘴', r'你有完没完',
        r'你怎么.*这么', r'你为什么.*总是', r'你为什么.*不能',
        r'你就不能', r'你为什么.*不', r'你就不能.*安静', r'你就不能.*懂事'],
    'rescuer': [r'我帮你', r'我来.*帮你', r'让我来', r'我给你',
        r'你应该.*这样', r'你听我的', r'听我的', r'我教',
        r'我告诉你', r'你应该.*做', r'你不如.*这样', r'我建议你',
        r'你.*要.*才行', r'我给你.*建议', r'我给你.*方案',
        r'我帮你.*解决', r'我帮你.*处理', r'我来.*处理', r'我来.*解决',
        r'我来.*安排', r'你听.*我', r'你按.*说的', r'按我说的'],
    'victim': [r'为什么.*总是我', r'我没办法', r'我能怎么办', r'我也不想.*但是',
        r'我也不想啊', r'我也不想的', r'怪我.*咯', r'都怪我', r'是我.*不好',
        r'是我.*不对', r'我不好', r'我对不起', r'是我的错', r'我错了',
        r'我活该', r'没有人.*在乎', r'没有人.*关心', r'没有人.*要我',
        r'没人在乎', r'没人.*理', r'没人.*管', r'我活不下去',
        r'没你我活不了', r'没有你.*不行', r'我怎么办', r'我怎么办.*才好',
        r'谁来.*救', r'谁来.*帮', r'我好可怜', r'为什么.*我', r'为什么.*对我']
}

# --- B5: Schema Therapy ---
B5 = {
    'abandonment': [r'你会.*走', r'你是不是.*不要我', r'你不要我', r'你走了',
        r'你离开我', r'你会.*离开', r'你迟早.*走', r'你会.*厌倦', r'你会.*腻',
        r'你是不是.*烦了', r'嫌我', r'你会.*抛弃', r'不要走', r'别走',
        r'求你.*别走', r'你会.*找.*别人', r'你会.*喜欢.*别人', r'分手'],
    'emotional_deprivation': [r'你从来.*不懂', r'你不懂.*我', r'没人.*理解',
        r'没人.*懂', r'你不懂我', r'你不了解我', r'你从来.*不关心',
        r'你不在乎.*我', r'你从来.*不在乎', r'你感受不到', r'你无法.*理解',
        r'你给不了.*我要', r'你从来.*不给'],
    'defectiveness': [r'我不够好', r'我不配', r'你终.*发现.*我不行',
        r'我不值得', r'我不好', r'我太差', r'我太弱',
        r'我不够.*漂亮', r'我不够.*优秀', r'我配不上',
        r'你值得.*更好', r'你应该.*找.*更好', r'我不行', r'我没用',
        r'我是个.*废物', r'我什么都.*做不好'],
    'mistrust': [r'你是不是.*跟.*人', r'你是不是.*别人', r'你跟.*谁',
        r'你在.*跟谁', r'你是不是.*骗我', r'你骗我', r'你说的是.*真的',
        r'我不信', r'真的吗', r'你是不是.*说谎', r'你以前.*也.*说',
        r'你上次.*也.*说', r'你又骗', r'你是不是.*她', r'那个.*女',
        r'谁.*发.*消息', r'谁.*打电话'],
    'dependence': [r'没有你.*活不了', r'没你.*不行', r'你不能.*走',
        r'你不在.*我.*怎么办', r'我离不开你', r'我离不了你',
        r'没有你.*活不下去', r'你是.*唯一的', r'你是我.*全部',
        r'你是.*唯一.*靠', r'我只能.*靠你', r'除了你.*没人'],
    'self_sacrifice': [r'我没事.*你忙', r'我没事.*你去', r'你忙你的',
        r'不用管我', r'我无所谓', r'我没关系', r'你开心.*就好',
        r'你高兴.*就好', r'我都行', r'听你的', r'你说了算', r'你决定'],
    'subjugation': [r'听你的', r'你说了算', r'你决定', r'我不敢.*说',
        r'我不敢.*问', r'我不敢.*提', r'怕.*你.*生气',
        r'怕.*惹.*不高兴', r'我不敢.*反对', r'我不敢.*拒绝'],
    'emotional_inhibition': [r'没事', r'我很好', r'我没事', r'没什么',
        r'不想说', r'不想提', r'算了', r'无所谓', r'随便', r'都行',
        r'没什么.*好说', r'没什么.*好聊', r'不想.*谈', r'没什么.*大不了'],
    'unrelenting_standards': [r'你应该.*更好', r'你怎么.*不能',
        r'你就不能.*努力', r'你应该.*做到', r'你为什么.*不能.*像',
        r'别人.*都.*能', r'你看.*人家', r'你应该.*学学',
        r'你不够.*努力', r'你不够.*上进'],
    'entitlement': [r'你必须', r'你给我', r'你不准', r'你必须.*听',
        r'我不管.*你必须', r'我就要', r'我偏要', r'我说了算',
        r'你照做', r'没得商量', r'不容商量', r'你不配.*拒绝'],
    'insufficient_self_control': [r'我控制不住', r'我忍不住',
        r'我没办法.*控制', r'我管不住.*自己', r'我忍不住.*想', r'我又.*忍不住']
}

# --- B6: Defense Mechanisms ---
B6 = {
    'denial': [r'我没有', r'不是这样的', r'你记错了', r'我没说过',
        r'不可能', r'不是.*我的错', r'不是.*我.*做的', r'我冤枉', r'你冤枉我'],
    'projection': [r'你才是', r'你自己不也', r'你不也一样', r'你比我还',
        r'你也.*一样', r'你有什么.*资格', r'你先.*管好.*自己', r'你有什么.*脸'],
    'passive_aggressive': [r'^哦$', r'好吧', r'随便.*你', r'随你', r'爱咋咋',
        r'我无所谓', r'我没事.*你忙', r'你开心.*就好', r'行吧.*算了'],
    'withdrawal': [r'算了', r'不说了', r'不想.*说', r'不想.*聊', r'不想.*谈',
        r'没什么.*好说', r'没什么.*好聊', r'不想.*理你'],
    'rationalization': [r'我是.*为了.*好', r'我是.*因为.*工作',
        r'我.*没办法', r'我.*身不由己', r'不是.*我.*想',
        r'我也想.*但.*不能', r'客观.*原因', r'特殊.*情况', r'我.*也.*不想.*这样'],
    'displacement': [r'要不是.*你', r'都怪.*你', r'因为你.*我才',
        r'是你.*让我', r'你逼我', r'你害我'],
    'reaction_formation': [r'无所谓', r'不在乎', r'我不.*在乎', r'随便',
        r'我.*根本.*不.*在乎', r'谁.*稀罕', r'我.*才不.*在乎'],
    'intellectualization': [r'从.*角度.*分析', r'客观.*来说', r'理性.*来看',
        r'理论上', r'逻辑.*上', r'事实.*上.*来说'],
    'humor': [r'哈哈', r'呵呵', r'笑死', r'搞笑', r'逗', r'笑.*我'],
    'sublimation': [r'我会.*努力', r'我会.*改', r'我.*变得.*更好', r'我会.*证明']
}

# --- B7: Inner Child ---
B7 = {
    'abandonment_trigger': [r'你别走', r'不要走', r'别离开我',
        r'你走了.*我怎么办', r'你不在.*怎么办', r'求你.*别走',
        r'不要.*丢下', r'别丢下我', r'别扔下我', r'你走了.*不要我'],
    'neglect_trigger': [r'你为什么不.*回', r'你为什么不.*理我',
        r'你为什么不.*答', r'你为什么不.*说话', r'你为什么不.*找我',
        r'你是不是.*不想.*理我', r'你理.*都不理', r'你不管.*我',
        r'你不在乎.*我', r'当.*空气', r'当.*透明', r'把我.*当.*空气'],
    'criticism_trigger': [r'你为什么.*说我', r'你凭什么.*说我',
        r'你有什么.*资格.*说', r'你不用.*说我', r'你能不能.*别说我',
        r'你能不能.*不要.*说我', r'你老是.*说我', r'你总是.*嫌弃'],
    'regression_baby': [r'我要.*嘛', r'我不嘛', r'好不好嘛', r'求求.*嘛',
        r'你陪我.*嘛', r'我要.*你.*嘛', r'我就要.*嘛', r'我不要.*嘛',
        r'抱抱', r'抱抱.*嘛', r'亲亲', r'你.*抱抱我', r'举高高',
        r'撒娇', r'哼.*不理你', r'哼.*你.*坏'],
    'compensation_seeking': [r'你.*说.*爱我', r'你说.*你是不是.*爱',
        r'你说.*你想我', r'你说.*你在乎', r'你.*证明.*爱我',
        r'你.*发誓', r'你.*发誓.*爱我', r'你.*承诺', r'你.*保证',
        r'你.*发誓.*永远'],
    'fear_rejection': [r'你是不是.*嫌弃', r'你是不是.*讨厌', r'你是不是.*烦',
        r'你是不是.*不要', r'你是不是.*想分', r'你是不是.*不爱',
        r'你是不是.*厌倦', r'你嫌.*我', r'你讨厌.*我', r'你烦.*我']
}

# --- B8: Johari Window ---
B8_UNKNOWN_TOPICS = [
    '结婚','婚后','领证','见父母','买房','孩子','宝宝','怀孕',
    '未来规划','以后打算','三年计划','五年计划',
    '存款','理财','投资','性','性生活','避孕'
]
B8_PUBLIC_TOPICS = [
    '爱','想你','早安','晚安','吃饭','回家','工作','累',
    '开心','难过','视频','电话','亲','抱','梦','礼物',
    '生日','节日','红包','转账'
]

# --- C9: Relational Dialectics ---
# Uses long_msg detection (>50 chars) and unique word counting

# --- C10: Social Exchange ---
C10_DEEP_WORDS = ['我爱你','我想你','我需要你','我不能没有你','你对我很重要',
    '我好想你','我好爱你','我舍不得','我不想失去']
C10_LOVE_EXPR = ['爱','爱你','想你','喜欢你','在乎你','舍不得']
C10_MISS_EXPR = ['想你','想你','想念','思念','好久不见','什么时候见']

# --- C11: Five Bases of Power ---
C11 = {
    'reward': [r'给你', r'买.*给你', r'帮你.*买', r'送你', r'红包',
        r'转账', r'我请', r'我付', r'我出', r'给你.*钱'],
    'coercive': [r'分手', r'我不理你', r'我走了', r'再见', r'拉黑',
        r'删了', r'不联系', r'不要.*联系', r'你.*再.*这样.*我就',
        r'你.*再.*不.*改.*我.*就'],
    'legitimate': [r'你应该', r'你应该.*做', r'作为.*男朋友',
        r'作为.*女朋友', r'你有.*义务', r'你有.*责任', r'你应该.*负责'],
    'referent': [r'你像', r'跟你.*一样', r'学你', r'我想.*像你',
        r'我要.*像你', r'你.*好厉害', r'你.*好棒', r'你.*真厉害'],
    'expert': [r'我告诉你', r'我跟你说', r'你听.*我说', r'我知道',
        r'我懂', r'我了解', r'我教你', r'听我的.*没错', r'我说.*对', r'我说的.*没错']
}

# --- C12: Attachment Multi-Dimensional ---
C12 = {
    'self_neg': ['我不够好','我不行','我没用','我不配','我太差','我不好',
        '我对不起','是我的错','我错了','我活该','我自卑','我差','我弱',
        '我丑','我笨','我傻','我蠢'],
    'self_pos': ['我很棒','我很好','我值得','我配得上','我能行','我可以',
        '我很强','我厉害','我优秀','我漂亮','我好看','我聪明'],
    'trust': ['相信你','信你','信任你','你说的对','我知道你','你不会骗我'],
    'distrust': ['真的吗','你骗我','我不信','你骗','你说谎','你骗人的',
        '你肯定','你是不是','你真的','你又骗','我不信你'],
    'approach': ['你陪我','我陪你','想见你','见面','你过来','我过去',
        '你等我','等我','抱抱','亲亲','牵'],
    'avoid': ['算了','不说了','不想说','别管我','让我静静','我想一个人',
        '别理我','不想.*见']
}

# --- C13: Gottman Trust Formula ---
C13_FUTURE = [r'以后', r'未来', r'永远', r'一辈子', r'一直.*在一起']
C13_BREAKUP = [r'分手', r'分开', r'结束', r'不要.*了', r'散了吧']
C13_CRY_SIGNALS = ['哭','呜呜','好难过','崩溃','绝望','不想活','死']

# --- D14: Self-Determination Theory ---
D14 = {
    'controlled': [r'你必须', r'你给我', r'你不准', r'你不许', r'你一定要',
        r'听我的', r'你说了算', r'你决定', r'你应该.*听', r'按我说的', r'你照做'],
    'autonomous': [r'我选择', r'我决定', r'我想', r'我愿意', r'我自愿',
        r'我自己', r'我决定.*了'],
    'praised': [r'好棒', r'厉害', r'真厉害', r'聪明', r'你.*真棒',
        r'你.*好厉害', r'为你骄傲', r'你真行', r'牛', r'优秀', r'你做得好', r'做得好'],
    'criticized': [r'你怎么.*这么', r'你为什么.*不能', r'你太差', r'你不行',
        r'你没用', r'你废物', r'你什么都.*做不好', r'你.*真差', r'你笨'],
    'connected': [r'爱你', r'想你', r'抱抱', r'亲亲', r'陪我', r'一起', r'我们在', r'我们的'],
    'isolated': [r'别管我', r'让我.*静静', r'我想.*一个人', r'不想.*见', r'别理我']
}

# --- D15: Emotion Regulation ---
D15 = {
    'suppression': [r'没事', r'我很好', r'没什么', r'不想说', r'不想提',
        r'算了', r'无所谓', r'随便', r'都行', r'没什么.*好说'],
    'expression': [r'我生气', r'我难过', r'我害怕', r'我焦虑', r'我委屈',
        r'我失望', r'我愤怒', r'我开心', r'我好.*累', r'我哭', r'呜呜', r'我崩溃', r'我受不了'],
    'reappraisal': [r'其实.*没什么', r'换个角度', r'也.*不是.*坏事',
        r'往好处想', r'也许.*是.*好事', r'算了.*也好', r'换个想法'],
    'avoidance': [r'不说了', r'别.*说了', r'转移话题', r'你.*说.*别的',
        r'不说.*这个', r'聊点.*别的', r'换个话题']
}

# --- D16: Maslow Hierarchy ---
D16 = {
    'physiological': [r'吃饭', r'睡觉', r'饿', r'困', r'累', r'睡', r'吃',
        r'喝', r'病', r'痛', r'冷', r'热', r'不舒服', r'感冒', r'发烧',
        r'肚子.*疼', r'头晕', r'去医院', r'看医生'],
    'safety': [r'安全', r'保护', r'稳定', r'收入', r'工作', r'钱', r'房',
        r'租', r'工资', r'经济', r'存款', r'未来', r'保障', r'保险',
        r'怕.*没.*钱', r'怕.*失业'],
    'love_belonging': [r'爱', r'想你', r'陪你', r'在乎', r'关心', r'不要.*走',
        r'别.*走', r'别.*离开', r'陪.*我', r'孤单', r'孤独', r'没人.*陪',
        r'想.*见', r'抱抱', r'亲亲'],
    'esteem': [r'尊重', r'认可', r'承认', r'夸', r'你.*真棒', r'你.*厉害',
        r'你.*聪明', r'你.*漂亮', r'你.*好看', r'你.*优秀', r'看不起',
        r'嫌弃', r'丢.*脸', r'没.*面子', r'没.*尊严', r'伤.*自尊', r'自卑'],
    'self_actual': [r'成长', r'进步', r'提升', r'梦想', r'目标', r'理想',
        r'实现', r'追求', r'变得.*更好', r'改变.*自己', r'学习', r'读书', r'锻炼', r'健身']
}

# --- D17: Enneagram ---
D17 = {
    '1_perfectionist': [r'你应该', r'不对', r'错了', r'不应该.*这样',
        r'应该.*更好', r'你怎么.*总是.*这样', r'不规矩', r'不正确', r'应该.*改'],
    '2_helper': [r'我帮你', r'我给你', r'让我来', r'你吃饭了吗', r'注意身体',
        r'多穿', r'早点睡', r'别熬夜', r'我担心你', r'我心疼你', r'你需要.*我'],
    '3_achiever': [r'工作', r'赚钱', r'成功', r'努力', r'上进', r'目标',
        r'效率', r'形象', r'面子', r'别人.*怎么看'],
    '4_individualist': [r'我.*独特', r'不一样', r'没人.*懂我', r'孤独',
        r'我.*太.*敏感', r'情绪', r'悲伤', r'忧郁', r'特殊'],
    '5_observer': [r'我需要.*空间', r'让我.*想想', r'我.*分析', r'理性',
        r'逻辑', r'客观', r'独处', r'不.*想.*被打扰', r'我.*观察'],
    '6_loyalist': [r'真的吗', r'你说的是.*真的', r'你会.*不会.*变',
        r'你是不是.*不爱', r'万一', r'如果.*怎么办', r'我怕', r'不安全', r'担心'],
    '7_enthusiast': [r'好开心', r'好玩', r'有趣', r'新.*东西', r'旅游',
        r'去.*玩', r'新鲜', r'刺激', r'开心.*就好', r'快乐'],
    '8_challenger': [r'你必须', r'你给我', r'我说的.*算', r'你照做',
        r'我不怕', r'我不管', r'你别管', r'听我的', r'我说了算'],
    '9_peacemaker': [r'算了', r'随便', r'都行', r'无所谓', r'没事',
        r'不.*想.*吵', r'随便.*你', r'都.*可以']
}

# --- E18: Gaslighting ---
E18 = {
    'deny_said': [r'我没说过', r'我没说', r'你记错了', r'我根本没说',
        r'我什么时候说过', r'我没那样说', r'你听错了', r'你理解错了'],
    'twist_memory': [r'明明是你', r'是你先', r'是你先说的', r'是你先做的',
        r'你忘了.*是你', r'是你引起的', r'是你挑起的'],
    'minimize_feelings': [r'你想多了', r'太敏感', r'你太敏感', r'小题大做',
        r'至于吗', r'有什么好.*生气', r'有什么好.*哭', r'你至于吗',
        r'这么小.*事', r'多大点事', r'你反应.*太大'],
    'shift_blame': [r'是你逼我的', r'你害的', r'都怪你', r'要不是你',
        r'因为你.*我才', r'是你让我.*这样', r'你造成的'],
    'confuse': [r'我什么时候', r'有吗', r'我说过吗', r'不可能',
        r'你确定吗', r'是吗', r'真的吗.*我']
}

# --- E19: Trauma Bond ---
E19_BREAKUP = [r'分手', r'分开', r'结束吧', r'不要了', r'算了吧', r'散了吧']
E19_RECONCILE = [r'和好', r'不分了', r'我错了', r'原谅', r'回来', r'不走了', r'不要.*分']
E19_EXPLAIN_WORDS = ['对不起','抱歉','刚才','刚刚','不好意思','在忙',
    '没看到','睡着了','开会','在开车','手机']

# --- E20: Silent Treatment ---
# Uses E19_EXPLAIN_WORDS for punitive vs protective classification

# --- E21: Codependency ---
E21 = {
    'self_worth_dep': [r'你.*开心.*我.*才.*开心', r'你不开心.*我也.*不开心',
        r'你.*笑.*我.*才.*笑', r'我.*全.*为你', r'你.*是我.*全部',
        r'没有你.*我.*什么都不是', r'你.*情绪.*影响.*我'],
    'over_responsible': [r'都怪我', r'是我的错', r'我对不起你', r'我错了',
        r'我应该.*做.*更好', r'都是.*我.*不好', r'怪我', r'我应该.*更.*努力'],
    'boundary_blur': [r'你的事.*就是.*我的事', r'你的痛.*我.*也.*痛',
        r'你.*难过.*我.*更.*难过', r'我们.*是一体', r'你的.*就是.*我的'],
    'control_behaviors': [r'你应该', r'你不应该', r'你听我的', r'按我说的',
        r'你必须', r'你给我', r'你不能', r'你不准', r'你需要.*改', r'你应该.*改'],
    'deny_needs': [r'我没事', r'我很好', r'我不需要', r'我无所谓',
        r'我不在乎', r'没关系', r'我.*不.*重要', r'你的.*事.*重要']
}

# --- F22: Habit Loop ---
F22_FIGHT_WORDS = ['生气','分手','滚','够了','闭嘴','烦','讨厌','哭','难过','崩溃']
F22_RECONCILE_WORDS = ['对不起','我错了','原谅','不分','回来','别走','不要分']

# --- F23: BIS/BAS ---
F23_BIS = [r'我害怕', r'我担心', r'我怕', r'万一', r'如果.*怎么办',
    r'不敢', r'犹豫', r'不确定', r'不想.*惹', r'算了', r'还是.*不.*了',
    r'不要.*了', r'别.*了']
F23_BAS = [r'我要', r'我现在.*就要', r'马上', r'立刻', r'现在', r'我来',
    r'我冲', r'我追', r'我不管.*了', r'不等了', r'直接', r'走.*吧',
    r'出发', r'干.*吧', r'做.*吧']

# --- F24: Sound Relationship House ---
F24_LOVE_MAP = ['你在想什么','你今天怎么样','你心情','你感觉','你怎么了',
    '你开心吗','你难过吗']
F24_FONDNESS = ['爱你','想你','好棒','厉害','漂亮','好看','可爱','乖','宝贝']
F24_POSITIVE_ATTR = ['你真好','你最好','你对我最好','你是最','你是唯一']
F24_REPAIR = ['对不起','我错了','原谅','我们和好','不要吵了','别吵了','我们谈谈']
F24_SUPPORT = ['加油','你可以的','支持你','我挺你','去追','去做吧','去试吧','相信你']
F24_SHARED = ['我们的','我们以后','一起','家','未来','一家人']

# --- Emotional Burst Detection ---
EMOTIONAL_BURST_NEG = ['哭','呜呜','难过','崩溃','绝望','死','不想活',
    '生气','气死','烦死','累死','恨','受不了','受不了了',
    '分手','滚','闭嘴','够了','讨厌','恶心']
EMOTIONAL_BURST_THRESHOLD = 5  # minimum consecutive messages for a burst

# --- Conversation Gap ---
CONVERSATION_GAP = 1800  # 30 minutes

# --- Disappearance Thresholds ---
DISAPPEAR_SHORT = 7200   # 2 hours
DISAPPEAR_LONG = 21600   # 6 hours
SILENCE_PUNITIVE = 21600 # 6 hours

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def compile_patterns(pattern_dict):
    """Pre-compile all regex patterns in a dictionary."""
    compiled = {}
    for key, patterns in pattern_dict.items():
        compiled[key] = [re.compile(p) for p in patterns]
    return compiled

def match_any(text, compiled_patterns):
    """Check if text matches any of the compiled patterns."""
    return any(p.search(text) for p in compiled_patterns)

def match_exact(text, exact_list):
    """Check if text (stripped) exactly matches any item."""
    t = text.strip()
    return t in exact_list

def match_keywords(text, keywords):
    """Check if any keyword is in text."""
    return any(kw in text for kw in keywords)

def safe_pct(numerator, denominator):
    """Safe percentage calculation."""
    return round(numerator / denominator * 100, 1) if denominator > 0 else 0.0

def safe_ratio(numerator, denominator):
    """Safe ratio calculation."""
    return round(numerator / denominator, 2) if denominator > 0 else 0.0

def median_response_time(times):
    """Calculate median response time in seconds."""
    if not times:
        return 0
    return statistics.median(times)

def percentile(data, p):
    """Calculate the p-th percentile."""
    if not data:
        return 0
    sorted_data = sorted(data)
    k = (len(sorted_data) - 1) * (p / 100)
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return sorted_data[int(k)]
    return sorted_data[f] + (sorted_data[c] - sorted_data[f]) * (k - f)

def pearson_correlation(x, y):
    """Compute Pearson correlation coefficient."""
    n = len(x)
    if n < 6 or n != len(y):
        return None
    mean_x = statistics.mean(x)
    mean_y = statistics.mean(y)
    numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
    denom_x = math.sqrt(sum((xi - mean_x) ** 2 for xi in x))
    denom_y = math.sqrt(sum((yi - mean_y) ** 2 for yi in y))
    if denom_x == 0 or denom_y == 0:
        return None
    return round(numerator / (denom_x * denom_y), 3)

# Pre-compile all patterns
COMPILED = {}
for name, patterns in [('A1', A1), ('A2', A2), ('A3', A3), ('A4', A4),
                        ('B5', B5), ('B6', B6), ('B7', B7),
                        ('C11', C11), ('C12', C12),
                        ('D14', D14), ('D15', D15), ('D16', D16), ('D17', D17),
                        ('E18', E18), ('E21', E21)]:
    COMPILED[name] = compile_patterns(patterns)

COMPILED['C13_future'] = [re.compile(p) for p in C13_FUTURE]
COMPILED['C13_breakup'] = [re.compile(p) for p in C13_BREAKUP]
COMPILED['F22_fight'] = F22_FIGHT_WORDS
COMPILED['F22_reconcile'] = F22_RECONCILE_WORDS
COMPILED['F23_bis'] = [re.compile(p) for p in F23_BIS]
COMPILED['F23_bas'] = [re.compile(p) for p in F23_BAS]

# ============================================================================
# DATA LOADING
# ============================================================================

def load_data(filepath):
    """Load chat JSON data."""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if isinstance(data, list):
        msgs = data
    elif isinstance(data, dict) and 'messages' in data:
        msgs = data['messages']
    else:
        msgs = data
    
    # Filter messages with valid timestamps
    msgs = [m for m in msgs if m.get('timestamp')]
    # Sort by timestamp
    msgs.sort(key=lambda m: m.get('timestamp', 0))
    return msgs

def identify_parties(msgs, sender_a=None, sender_b=None):
    """Identify the two parties in the conversation."""
    sender_counts = Counter(m.get('sender', '') for m in msgs)
    top_senders = [s for s, _ in sender_counts.most_common(10) if s]
    
    if sender_a and sender_b:
        party_a_id = sender_a
        party_b_id = sender_b
    elif len(top_senders) >= 2:
        # Auto-assign: A = fewer messages, B = more messages
        party_b_id = top_senders[0]  # most messages
        party_a_id = top_senders[1]  # second most
    else:
        party_a_id = top_senders[0] if top_senders else 'A'
        party_b_id = 'B'
    
    a_count = sender_counts.get(party_a_id, 0)
    b_count = sender_counts.get(party_b_id, 0)
    total = a_count + b_count
    
    return {
        'a_id': party_a_id,
        'b_id': party_b_id,
        'a_count': a_count,
        'b_count': b_count,
        'a_pct': safe_pct(a_count, total),
        'b_pct': safe_pct(b_count, total),
    }

def make_is_func(party_id):
    """Create a function that checks if a message is from a given party."""
    def is_party(m):
        return party_id in m.get('sender', '')
    return is_party

# ============================================================================
# FRAMEWORK ANALYSIS (Single Pass)
# ============================================================================

def run_all_frameworks(msgs, is_a, is_b):
    """Run all 24 frameworks in a single pass through messages."""
    
    # Initialize results for all frameworks
    results = defaultdict(lambda: defaultdict(lambda: {'a': 0, 'b': 0}))
    
    # For A3 PAC: need to track consecutive message pairs
    prev_sender = None
    prev_state = None
    pac_transactions = defaultdict(int)
    
    # For C9: daily unique words
    daily_words = defaultdict(set)
    daily_msg_count = defaultdict(int)
    
    # For C13: cry signal response tracking
    cry_signals = []
    
    # For E19/E20: disappearance tracking
    disappearances = []
    last_msg_ts = None
    last_msg_sender_a = None
    
    # For F22: chase sequences
    consecutive_a = 0
    consecutive_b = 0
    chase_sequences = {'a': 0, 'b': 0}
    chase_total_msgs = {'a': 0, 'b': 0}
    
    # For emotional bursts
    burst_data = detect_emotional_bursts(msgs, is_a, is_b)
    
    # Monthly tracking
    monthly = defaultdict(lambda: defaultdict(lambda: {'a': 0, 'b': 0, 'total': 0}))
    
    for i, m in enumerate(msgs):
        content = str(m.get('content', '')).strip()
        ts = m.get('timestamp', 0)
        a = is_a(m)
        b = is_b(m)
        party = 'a' if a else 'b'
        
        # Skip if neither party
        if not a and not b:
            continue
        
        # Monthly tracking
        if ts:
            month = datetime.fromtimestamp(ts).strftime('%Y-%m')
            monthly[month]['messages'][party] += 1
            monthly[month]['messages']['total'] += 1
        
        # Skip pattern matching for empty or very long messages
        if not content or len(content) > 300:
            # Still track conversations and response times
            continue
        
        # --- A1: Gottman ---
        for cat in ['criticism', 'contempt', 'defense']:
            if match_any(content, COMPILED['A1'][cat]):
                results['A1'][cat][party] += 1
                if ts:
                    monthly[month][f'A1_{cat}'][party] += 1
        
        if match_exact(content, A1['stonewall_exact']):
            results['A1']['stonewall'][party] += 1
            if ts:
                monthly[month]['A1_stonewall'][party] += 1
        
        for cat in ['positive_kw', 'negative_kw']:
            if match_keywords(content, A1[cat]):
                results['A1'][cat][party] += 1
        
        # --- A2: NVC ---
        for cat in ['eval_judg', 'fake_feeling', 'blame_need', 'command',
                    'pure_obs', 'real_feeling', 'express_need', 'clear_request']:
            if match_any(content, COMPILED['A2'][cat]):
                results['A2'][cat][party] += 1
        
        # --- A3: PAC ---
        pac_state = None
        if match_any(content, COMPILED['A3']['parent_p']):
            pac_state = 'P'
        elif match_any(content, COMPILED['A3']['adult_a']):
            pac_state = 'A'
        elif match_any(content, COMPILED['A3']['child_c']):
            pac_state = 'C'
        
        if pac_state:
            results['A3'][f'state_{pac_state}'][party] += 1
            
            # Track transactions
            if prev_state:
                transaction = f'{prev_state}->{pac_state}'
                pac_transactions[transaction] += 1
                
                # Cross transaction detection
                if prev_sender != party:
                    is_cross = (prev_state == 'P' and pac_state == 'A') or \
                               (prev_state == 'A' and pac_state in ('P', 'C')) or \
                               (prev_state == 'C' and pac_state == 'A')
                    if is_cross:
                        results['A3']['cross_transactions']['a' if a else 'b'] += 1
                    else:
                        results['A3']['complementary_transactions']['a' if a else 'b'] += 1
            
            prev_state = pac_state
            prev_sender = party
        
        # --- A4: Drama Triangle ---
        for cat in ['persecutor', 'rescuer', 'victim']:
            if match_any(content, COMPILED['A4'][cat]):
                results['A4'][cat][party] += 1
        
        # --- B5: Schema Therapy ---
        for cat in ['abandonment', 'emotional_deprivation', 'defectiveness',
                    'mistrust', 'dependence', 'self_sacrifice', 'subjugation',
                    'emotional_inhibition', 'unrelenting_standards', 'entitlement',
                    'insufficient_self_control']:
            if match_any(content, COMPILED['B5'][cat]):
                results['B5'][cat][party] += 1
        
        # --- B6: Defense Mechanisms ---
        for cat in ['denial', 'projection', 'passive_aggressive', 'withdrawal',
                    'rationalization', 'displacement', 'reaction_formation',
                    'intellectualization', 'humor', 'sublimation']:
            if match_any(content, COMPILED['B6'][cat]):
                results['B6'][cat][party] += 1
        
        # --- B7: Inner Child ---
        for cat in ['abandonment_trigger', 'neglect_trigger', 'criticism_trigger',
                    'regression_baby', 'compensation_seeking', 'fear_rejection']:
            if match_any(content, COMPILED['B7'][cat]):
                results['B7'][cat][party] += 1
        
        # --- B8: Johari Window ---
        for topic in B8_UNKNOWN_TOPICS:
            if topic in content:
                results['B8']['unknown_topics'][party] += 1
                break
        for topic in B8_PUBLIC_TOPICS:
            if topic in content:
                results['B8']['public_topics'][party] += 1
                break
        
        # --- C9: Relational Dialectics ---
        if len(content) > 50:
            results['C9']['long_messages'][party] += 1
        results['C9']['total_messages'][party] += 1
        
        # Daily unique words
        if ts:
            day = datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
            for word in content:
                if '\u4e00' <= word <= '\u9fff':
                    daily_words[day].add(word)
            daily_msg_count[day] += 1
        
        # --- C10: Social Exchange ---
        if len(content) > 50:
            results['C10']['deep_messages'][party] += 1
        if match_keywords(content, C10_LOVE_EXPR):
            results['C10']['love_expr'][party] += 1
        if match_keywords(content, C10_MISS_EXPR):
            results['C10']['miss_expr'][party] += 1
        
        # --- C11: Power Bases ---
        for cat in ['reward', 'coercive', 'legitimate', 'referent', 'expert']:
            if match_any(content, COMPILED['C11'][cat]):
                results['C11'][cat][party] += 1
        
        # --- C12: Attachment ---
        for cat in ['self_neg', 'self_pos', 'trust', 'distrust', 'approach', 'avoid']:
            if match_any(content, COMPILED['C12'][cat]):
                results['C12'][cat][party] += 1
        
        # --- C13: Trust Formula ---
        if match_any(content, COMPILED['C13_future']):
            results['C13']['future_words'][party] += 1
        if match_any(content, COMPILED['C13_breakup']):
            results['C13']['breakup_words'][party] += 1
            if ts:
                monthly[month]['breakup_words'][party] += 1
        if match_keywords(content, C13_CRY_SIGNALS):
            results['C13']['cry_signals'][party] += 1
            cry_signals.append((i, ts, party))
        
        # --- D14: SDT ---
        for cat in ['controlled', 'autonomous', 'praised', 'criticized', 'connected', 'isolated']:
            if match_any(content, COMPILED['D14'][cat]):
                results['D14'][cat][party] += 1
        
        # --- D15: Emotion Regulation ---
        for cat in ['suppression', 'expression', 'reappraisal', 'avoidance']:
            if match_any(content, COMPILED['D15'][cat]):
                results['D15'][cat][party] += 1
        
        # --- D16: Maslow ---
        for cat in ['physiological', 'safety', 'love_belonging', 'esteem', 'self_actual']:
            if match_any(content, COMPILED['D16'][cat]):
                results['D16'][cat][party] += 1
        
        # --- D17: Enneagram ---
        for cat in ['1_perfectionist', '2_helper', '3_achiever', '4_individualist',
                    '5_observer', '6_loyalist', '7_enthusiast', '8_challenger', '9_peacemaker']:
            if match_any(content, COMPILED['D17'][cat]):
                results['D17'][cat][party] += 1
        
        # --- E18: Gaslighting ---
        for cat in ['deny_said', 'twist_memory', 'minimize_feelings', 'shift_blame', 'confuse']:
            if match_any(content, COMPILED['E18'][cat]):
                results['E18'][cat][party] += 1
        
        # --- E19: Trauma Bond ---
        if match_any(content, [re.compile(p) for p in E19_BREAKUP]):
            results['E19']['breakup'][party] += 1
        if match_any(content, [re.compile(p) for p in E19_RECONCILE]):
            results['E19']['reconcile'][party] += 1
        
        # --- E21: Codependency ---
        for cat in ['self_worth_dep', 'over_responsible', 'boundary_blur', 'control_behaviors', 'deny_needs']:
            if match_any(content, COMPILED['E21'][cat]):
                results['E21'][cat][party] += 1
        
        # --- F22: Habit Loop (chase sequences) ---
        if a:
            consecutive_a += 1
            if consecutive_b >= 3:
                chase_sequences['b'] += 1
                chase_total_msgs['b'] += consecutive_b
            consecutive_b = 0
        elif b:
            consecutive_b += 1
            if consecutive_a >= 3:
                chase_sequences['a'] += 1
                chase_total_msgs['a'] += consecutive_a
            consecutive_a = 0
        
        # --- F23: BIS/BAS ---
        if match_any(content, COMPILED['F23_bis']):
            results['F23']['bis'][party] += 1
        if match_any(content, COMPILED['F23_bas']):
            results['F23']['bas'][party] += 1
        
        # --- F24: Sound Relationship House ---
        if match_keywords(content, F24_LOVE_MAP):
            results['F24']['love_maps'][party] += 1
        if match_keywords(content, F24_FONDNESS):
            results['F24']['fondness'][party] += 1
        if match_keywords(content, F24_POSITIVE_ATTR):
            results['F24']['positive_perspective'][party] += 1
        if match_keywords(content, F24_REPAIR):
            results['F24']['repair'][party] += 1
        if match_keywords(content, F24_SUPPORT):
            results['F24']['support'][party] += 1
        if match_keywords(content, F24_SHARED):
            results['F24']['shared_meaning'][party] += 1
        
        # --- Chase sequence monthly tracking ---
        if ts:
            monthly[month]['chase_sequences']['total'] = chase_sequences['a'] + chase_sequences['b']
        
        # --- Disappearance detection ---
        if last_msg_ts and ts:
            gap = ts - last_msg_ts
            if gap > DISAPPEAR_SHORT and last_msg_sender_a != a:
                disappearances.append({
                    'gap': gap,
                    'who_disappeared': 'a' if last_msg_sender_a else 'b',
                    'who_waited': 'b' if last_msg_sender_a else 'a',
                    'timestamp': last_msg_ts,
                })
                if ts:
                    monthly[month]['disappearances']['total'] += 1
        
        last_msg_ts = ts
        last_msg_sender_a = a
    
    # --- Post-processing: Compute derived metrics ---
    
    # C13: Cry signal response rate
    cry_response_count = 0
    for idx, cry_ts, cry_party in cry_signals:
        waiting_party = 'b' if cry_party == 'a' else 'a'
        for j in range(idx + 1, min(idx + 20, len(msgs))):
            other_msg = msgs[j]
            if (waiting_party == 'a' and is_a(other_msg)) or (waiting_party == 'b' and is_b(other_msg)):
                if other_msg.get('timestamp', 0) - cry_ts < 1800:
                    cry_response_count += 1
                break
    
    results['C13']['cry_response_rate'] = {
        'total_cries': len(cry_signals),
        'responses': cry_response_count,
        'rate': safe_pct(cry_response_count, len(cry_signals))
    }
    
    # E20: Silent Treatment
    punitive = 0
    protective = 0
    for i in range(len(msgs) - 1):
        if not is_a(msgs[i]):
            continue
        # Find gap after her message
        her_ts = msgs[i].get('timestamp', 0)
        for j in range(i + 1, min(i + 30, len(msgs))):
            if is_a(msgs[j]):
                gap = msgs[j].get('timestamp', 0) - her_ts
                if gap > SILENCE_PUNITIVE:
                    # Check if explanation in next 3 messages
                    explained = False
                    for k in range(j, min(j + 3, len(msgs))):
                        rc = str(msgs[k].get('content', ''))
                        if any(w in rc for w in E19_EXPLAIN_WORDS):
                            explained = True
                            break
                    if explained:
                        protective += 1
                    else:
                        punitive += 1
                break
    
    results['E20'] = {
        'punitive': {'count': punitive},
        'protective': {'count': protective},
        'punitive_ratio': safe_pct(punitive, punitive + protective)
    }
    
    # C9: Daily stats
    daily_counts = list(daily_msg_count.values())
    if daily_counts:
        results['C9']['daily_stats'] = {
            'mean': round(statistics.mean(daily_counts), 1),
            'stdev': round(statistics.stdev(daily_counts), 1) if len(daily_counts) > 1 else 0,
            'max': max(daily_counts),
            'min': min(daily_counts),
            'cv': round(statistics.stdev(daily_counts) / max(statistics.mean(daily_counts), 1), 2) if len(daily_counts) > 1 else 0,
            'avg_unique_words': round(statistics.mean(len(w) for w in daily_words.values()), 1) if daily_words else 0
        }
    
    # Disappearances summary
    disappear_gaps = [d['gap'] for d in disappearances]
    results['E19']['disappearances'] = {
        'count': len(disappearances),
        'avg_gap_hours': round(sum(disappear_gaps) / max(len(disappear_gaps), 1) / 3600, 1),
        'max_gap_hours': round(max(disappear_gaps) / 3600, 1) if disappear_gaps else 0,
        'min_gap_hours': round(min(disappear_gaps) / 3600, 1) if disappear_gaps else 0
    }
    
    # Chase sequences
    results['F22'] = {
        'chase_sequences': chase_sequences,
        'chase_total_msgs': chase_total_msgs,
        'chase_avg_msgs': {
            'a': round(chase_total_msgs['a'] / max(chase_sequences['a'], 1), 1),
            'b': round(chase_total_msgs['b'] / max(chase_sequences['b'], 1), 1)
        },
        'fight_disappear': 0  # placeholder, computed below
    }
    
    # F22: Fight -> disappear
    fight_disappear_count = 0
    for i, m in enumerate(msgs):
        if is_b(m):
            c = str(m.get('content', ''))
            if any(w in c for w in F22_FIGHT_WORDS):
                for j in range(i + 1, min(i + 30, len(msgs))):
                    if is_a(msgs[j]):
                        if msgs[j].get('timestamp', 0) - m.get('timestamp', 0) > DISAPPEAR_SHORT:
                            fight_disappear_count += 1
                        break
    results['F22']['fight_disappear'] = fight_disappear_count
    
    # PAC transactions
    results['A3']['transactions'] = dict(pac_transactions)
    
    # Convert defaultdict to regular dict
    return dict(results), dict(monthly), burst_data

# ============================================================================
# EMOTIONAL BURST DETECTION
# ============================================================================

def detect_emotional_bursts(msgs, is_a, is_b):
    """Detect emotional burst sequences (>=5 consecutive msgs with negative emotion)."""
    bursts_a = []
    bursts_b = []
    current_burst = []
    current_party = None
    
    for m in msgs:
        content = str(m.get('content', '')).strip()
        if not content or len(content) > 300:
            continue
        
        a = is_a(m)
        b = is_b(m)
        if not a and not b:
            continue
        
        party = 'a' if a else 'b'
        has_negative = any(w in content for w in EMOTIONAL_BURST_NEG)
        
        if has_negative and (current_party is None or current_party == party):
            current_burst.append({
                'content': content[:50],
                'ts': m.get('timestamp', 0)
            })
            current_party = party
        elif not has_negative and current_party == party:
            # Burst ended
            if len(current_burst) >= EMOTIONAL_BURST_THRESHOLD:
                burst = {
                    'party': current_party,
                    'length': len(current_burst),
                    'intensity': round(len(current_burst) * 1.0, 1),  # simplified
                    'start_ts': current_burst[0]['ts'],
                    'sample': [b['content'] for b in current_burst[:3]]
                }
                if current_party == 'a':
                    bursts_a.append(burst)
                else:
                    bursts_b.append(burst)
            current_burst = []
            current_party = None
        elif has_negative and current_party != party:
            # Party switched, end previous burst
            if len(current_burst) >= EMOTIONAL_BURST_THRESHOLD:
                burst = {
                    'party': current_party,
                    'length': len(current_burst),
                    'intensity': round(len(current_burst) * 1.0, 1),
                    'start_ts': current_burst[0]['ts'],
                    'sample': [b['content'] for b in current_burst[:3]]
                }
                if current_party == 'a':
                    bursts_a.append(burst)
                else:
                    bursts_b.append(burst)
            current_burst = [{
                'content': content[:50],
                'ts': m.get('timestamp', 0)
            }]
            current_party = party
    
    # Don't forget the last burst
    if len(current_burst) >= EMOTIONAL_BURST_THRESHOLD:
        burst = {
            'party': current_party,
            'length': len(current_burst),
            'intensity': round(len(current_burst) * 1.0, 1),
            'start_ts': current_burst[0]['ts'],
            'sample': [b['content'] for b in current_burst[:3]]
        }
        if current_party == 'a':
            bursts_a.append(burst)
        else:
            bursts_b.append(burst)
    
    all_bursts = sorted(bursts_a + bursts_b, key=lambda x: -x['intensity'])
    
    return {
        'a_count': len(bursts_a),
        'b_count': len(bursts_b),
        'a_avg_intensity': round(statistics.mean([b['intensity'] for b in bursts_a]), 1) if bursts_a else 0,
        'b_avg_intensity': round(statistics.mean([b['intensity'] for b in bursts_b]), 1) if bursts_b else 0,
        'a_avg_length': round(statistics.mean([b['length'] for b in bursts_a]), 1) if bursts_a else 0,
        'b_avg_length': round(statistics.mean([b['length'] for b in bursts_b]), 1) if bursts_b else 0,
        'top_5_bursts': [
            {
                'date': datetime.fromtimestamp(b['start_ts']).strftime('%Y-%m-%d') if b['start_ts'] else 'unknown',
                'party': b['party'],
                'length': b['length'],
                'intensity': b['intensity'],
                'sample': b['sample']
            }
            for b in all_bursts[:5]
        ]
    }

# ============================================================================
# ADDITIONAL METRICS
# ============================================================================

def compute_additional_metrics(msgs, is_a, is_b):
    """Compute response time, conversation, time-of-day, and message stats."""
    
    # --- Response Time ---
    a_response_times = []
    b_response_times = []
    
    for i in range(len(msgs) - 1):
        msg = msgs[i]
        if not (is_a(msg) or is_b(msg)):
            continue
        a = is_a(msg)
        ts = msg.get('timestamp', 0)
        
        for j in range(i + 1, min(i + 50, len(msgs))):
            next_msg = msgs[j]
            next_a = is_a(next_msg)
            next_b = is_b(next_msg)
            
            if a and next_b:
                gap = next_msg.get('timestamp', 0) - ts
                if 0 < gap < 3600:  # within 1 hour
                    b_response_times.append(gap)
                break
            elif not a and next_a:
                gap = next_msg.get('timestamp', 0) - ts
                if 0 < gap < 3600:
                    a_response_times.append(gap)
                break
    
    # --- Conversation Analysis ---
    conversations = []
    if msgs:
        current_conv = [msgs[0]]
        for i in range(1, len(msgs)):
            gap = msgs[i].get('timestamp', 0) - msgs[i-1].get('timestamp', 0)
            if gap > CONVERSATION_GAP:
                conversations.append(current_conv)
                current_conv = [msgs[i]]
            else:
                current_conv.append(msgs[i])
        conversations.append(current_conv)
    
    a_initiates = sum(1 for c in conversations if c and is_a(c[0]))
    b_initiates = sum(1 for c in conversations if c and is_b(c[0]))
    a_ends = sum(1 for c in conversations if c and is_a(c[-1]))
    b_ends = sum(1 for c in conversations if c and is_b(c[-1]))
    
    conv_lengths = [len(c) for c in conversations]
    
    # --- Time of Day ---
    tod_a = {'morning': 0, 'afternoon': 0, 'evening': 0, 'late_night': 0}
    tod_b = {'morning': 0, 'afternoon': 0, 'evening': 0, 'late_night': 0}
    
    for m in msgs:
        ts = m.get('timestamp', 0)
        if not ts:
            continue
        hour = datetime.fromtimestamp(ts).hour
        if 6 <= hour < 12:
            period = 'morning'
        elif 12 <= hour < 18:
            period = 'afternoon'
        elif 18 <= hour < 24:
            period = 'evening'
        else:
            period = 'late_night'
        
        if is_a(m):
            tod_a[period] += 1
        elif is_b(m):
            tod_b[period] += 1
    
    # --- Message Stats ---
    a_lengths = [len(str(m.get('content', ''))) for m in msgs if is_a(m) and m.get('content')]
    b_lengths = [len(str(m.get('content', ''))) for m in msgs if is_b(m) and m.get('content')]
    
    # --- Message Types ---
    a_types = Counter()
    b_types = Counter()
    for m in msgs:
        mtype = m.get('type', 'text')
        if is_a(m):
            a_types[mtype] += 1
        elif is_b(m):
            b_types[mtype] += 1
    
    # --- Date range ---
    timestamps = [m.get('timestamp', 0) for m in msgs if m.get('timestamp')]
    if timestamps:
        date_start = datetime.fromtimestamp(min(timestamps)).strftime('%Y-%m-%d')
        date_end = datetime.fromtimestamp(max(timestamps)).strftime('%Y-%m-%d')
        total_days = (max(timestamps) - min(timestamps)) / 86400
    else:
        date_start = date_end = 'unknown'
        total_days = 0
    
    return {
        'response_time': {
            'a': {
                'median': round(median_response_time(a_response_times), 1),
                'mean': round(statistics.mean(a_response_times), 1) if a_response_times else 0,
                'p25': round(percentile(a_response_times, 25), 1),
                'p75': round(percentile(a_response_times, 75), 1),
                'count': len(a_response_times)
            },
            'b': {
                'median': round(median_response_time(b_response_times), 1),
                'mean': round(statistics.mean(b_response_times), 1) if b_response_times else 0,
                'p25': round(percentile(b_response_times, 25), 1),
                'p75': round(percentile(b_response_times, 75), 1),
                'count': len(b_response_times)
            }
        },
        'conversations': {
            'total': len(conversations),
            'avg_length': round(statistics.mean(conv_lengths), 1) if conv_lengths else 0,
            'conversations_per_day': round(len(conversations) / max(total_days, 1), 1),
            'a_initiates': a_initiates,
            'b_initiates': b_initiates,
            'a_initiate_pct': safe_pct(a_initiates, a_initiates + b_initiates),
            'b_initiate_pct': safe_pct(b_initiates, a_initiates + b_initiates),
            'a_ends': a_ends,
            'b_ends': b_ends,
        },
        'time_of_day': {
            'a': tod_a,
            'b': tod_b,
            'peak_hour_a': max(tod_a, key=tod_a.get) if any(tod_a.values()) else 'unknown',
            'peak_hour_b': max(tod_b, key=tod_b.get) if any(tod_b.values()) else 'unknown',
            'late_night_pct_a': safe_pct(tod_a['late_night'], sum(tod_a.values())),
            'late_night_pct_b': safe_pct(tod_b['late_night'], sum(tod_b.values())),
        },
        'message_stats': {
            'a': {
                'median_length': round(statistics.median(a_lengths), 1) if a_lengths else 0,
                'mean_length': round(statistics.mean(a_lengths), 1) if a_lengths else 0,
                'p75': round(percentile(a_lengths, 75), 1) if a_lengths else 0,
                'p95': round(percentile(a_lengths, 95), 1) if a_lengths else 0,
                'max': max(a_lengths) if a_lengths else 0,
            },
            'b': {
                'median_length': round(statistics.median(b_lengths), 1) if b_lengths else 0,
                'mean_length': round(statistics.mean(b_lengths), 1) if b_lengths else 0,
                'p75': round(percentile(b_lengths, 75), 1) if b_lengths else 0,
                'p95': round(percentile(b_lengths, 95), 1) if b_lengths else 0,
                'max': max(b_lengths) if b_lengths else 0,
            }
        },
        'message_types': {
            'a': dict(a_types),
            'b': dict(b_types),
        },
        'date_range': {
            'start': date_start,
            'end': date_end,
            'total_days': round(total_days)
        }
    }

# ============================================================================
# NORMALIZATION
# ============================================================================

def normalize_per_1k(results, a_count, b_count):
    """Normalize all metrics per 1,000 messages."""
    normalized = {}
    for framework, categories in results.items():
        if not isinstance(categories, dict):
            continue
        normalized[framework] = {}
        for cat, values in categories.items():
            if isinstance(values, dict) and 'a' in values and 'b' in values:
                normalized[framework][cat] = {
                    'a_per_1k': round(values['a'] / max(a_count, 1) * 1000, 2),
                    'b_per_1k': round(values['b'] / max(b_count, 1) * 1000, 2),
                }
    return normalized

# ============================================================================
# CORRELATION MATRIX
# ============================================================================

def compute_correlations(monthly, framework_results, a_count, b_count):
    """Compute pairwise correlations on monthly time series."""
    
    # Extract key monthly metrics
    months = sorted(monthly.keys())
    if len(months) < 6:
        return {'description': 'Insufficient monthly data (need >= 6 months)', 'pairs': []}
    
    metrics = {}
    
    # Message count
    metrics['msg_count'] = [monthly[m]['messages']['total'] for m in months]
    
    # Gottman ratio (positive/negative)
    gottman_pos = []
    gottman_neg = []
    for m in months:
        pos = monthly[m].get('A1_positive_kw', {}).get('total', 0) + \
              monthly[m].get('A1_positive_kw', {}).get('a', 0) + \
              monthly[m].get('A1_positive_kw', {}).get('b', 0)
        neg = monthly[m].get('A1_negative_kw', {}).get('total', 0) + \
              monthly[m].get('A1_negative_kw', {}).get('a', 0) + \
              monthly[m].get('A1_negative_kw', {}).get('b', 0)
        # Use simple counts as proxy
        pos_count = monthly[m].get('A1_contempt', {}).get('a', 0) + monthly[m].get('A1_contempt', {}).get('b', 0)
        neg_count = monthly[m].get('A1_criticism', {}).get('a', 0) + monthly[m].get('A1_criticism', {}).get('b', 0)
        metrics['contempt_count'] = metrics.get('contempt_count', [])
        metrics['contempt_count'].append(pos_count)
        metrics['criticism_count'] = metrics.get('criticism_count', [])
        metrics['criticism_count'].append(neg_count)
    
    # Breakup words
    metrics['breakup_words'] = [
        monthly[m].get('breakup_words', {}).get('a', 0) + monthly[m].get('breakup_words', {}).get('b', 0)
        for m in months
    ]
    
    # Disappearances
    metrics['disappearances'] = [
        monthly[m].get('disappearances', {}).get('total', 0)
        for m in months
    ]
    
    # Chase sequences
    metrics['chase_sequences'] = [
        monthly[m].get('chase_sequences', {}).get('total', 0)
        for m in months
    ]
    
    # Stonewall count
    metrics['stonewall_count'] = [
        monthly[m].get('A1_stonewall', {}).get('a', 0) + monthly[m].get('A1_stonewall', {}).get('b', 0)
        for m in months
    ]
    
    # Ensure all lists have the same length
    max_len = len(months)
    for key in metrics:
        while len(metrics[key]) < max_len:
            metrics[key].append(0)
    
    # Compute pairwise correlations
    strong_pairs = []
    metric_names = list(metrics.keys())
    
    for i in range(len(metric_names)):
        for j in range(i + 1, len(metric_names)):
            r = pearson_correlation(metrics[metric_names[i]], metrics[metric_names[j]])
            if r is not None and abs(r) > 0.5:
                strong_pairs.append({
                    'metrics': [metric_names[i], metric_names[j]],
                    'r': r,
                    'n': max_len
                })
    
    strong_pairs.sort(key=lambda x: -abs(x['r']))
    
    return {
        'description': f'Pearson correlation on {len(months)} monthly data points. Only |r| > 0.5 shown.',
        'months_analyzed': len(months),
        'strong_pairs': strong_pairs
    }

# ============================================================================
# OUTPUT
# ============================================================================

def save_json(data, filepath):
    """Save results as JSON."""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)

def print_summary(data):
    """Print a compact summary to console."""
    meta = data['meta']
    fw = data['frameworks']
    add = data['additional_metrics']
    
    print("=" * 60)
    print("  RELATIONSHIP DEEP ANALYSIS - 24 Frameworks")
    print("=" * 60)
    print(f"  Messages: {meta['total_messages']:,} | Days: {meta['total_days']}")
    print(f"  Party A: {meta['party_a']['sender']} ({meta['party_a']['messages']:,} msgs, {meta['party_a']['pct']}%)")
    print(f"  Party B: {meta['party_b']['sender']} ({meta['party_b']['messages']:,} msgs, {meta['party_b']['pct']}%)")
    print(f"  Date: {meta['date_range']['start']} -> {meta['date_range']['end']}")
    print()
    
    # Helper
    def g(framework, cat, party='a'):
        try:
            return fw[framework][cat][party]
        except (KeyError, TypeError):
            return 0
    
    print("--- A. Communication Patterns ---")
    print(f"A1. Gottman: crit={g('A1','criticism','a')}+{g('A1','criticism','b')} | "
          f"contempt={g('A1','contempt','a')}+{g('A1','contempt','b')} | "
          f"def={g('A1','defense','a')}+{g('A1','defense','b')} | "
          f"stonewall={g('A1','stonewall','a')}+{g('A1','stonewall','b')}")
    print(f"A2. NVC: see JSON for details")
    print(f"A3. PAC: P={g('A3','state_P','a')}+{g('A3','state_P','b')} | "
          f"A={g('A3','state_A','a')}+{g('A3','state_A','b')} | "
          f"C={g('A3','state_C','a')}+{g('A3','state_C','b')}")
    print(f"A4. Drama: persec={g('A4','persecutor','a')}+{g('A4','persecutor','b')} | "
          f"rescue={g('A4','rescuer','a')}+{g('A4','rescuer','b')} | "
          f"victim={g('A4','victim','a')}+{g('A4','victim','b')}")
    print()
    
    print("--- B. Psychology ---")
    print(f"B5. Schemas: abandon={g('B5','abandonment','a')}+{g('B5','abandonment','b')} | "
          f"inh={g('B5','emotional_inhibition','a')}+{g('B5','emotional_inhibition','b')}")
    print(f"B6. Defenses: denial={g('B6','denial','a')}+{g('B6','denial','b')} | "
          f"pass_agg={g('B6','passive_aggressive','a')}+{g('B6','passive_aggressive','b')} | "
          f"humor={g('B6','humor','a')}+{g('B6','humor','b')}")
    print(f"B7. Inner Child: regression={g('B7','regression_baby','a')}+{g('B7','regression_baby','b')}")
    print(f"B8. Johari: unknown={g('B8','unknown_topics','a')}+{g('B8','unknown_topics','b')} | "
          f"public={g('B8','public_topics','a')}+{g('B8','public_topics','b')}")
    print()
    
    print("--- C. Dynamics ---")
    print(f"C11. Power: reward={g('C11','reward','a')}+{g('C11','reward','b')} | "
          f"coercive={g('C11','coercive','a')}+{g('C11','coercive','b')}")
    print(f"C12. Attachment: distrust={g('C12','distrust','a')}+{g('C12','distrust','b')} | "
          f"trust={g('C12','trust','a')}+{g('C12','trust','b')}")
    print(f"C13. Trust: future={g('C13','future_words','a')}+{g('C13','future_words','b')} | "
          f"breakup={g('C13','breakup_words','a')}+{g('C13','breakup_words','b')}")
    print()
    
    print("--- D. Needs ---")
    print(f"D14. SDT: controlled={g('D14','controlled','a')}+{g('D14','controlled','b')} | "
          f"autonomous={g('D14','autonomous','a')}+{g('D14','autonomous','b')}")
    print(f"D15. Emotion: supp={g('D15','suppression','a')}+{g('D15','suppression','b')} | "
          f"expr={g('D15','expression','a')}+{g('D15','expression','b')}")
    print(f"D16. Maslow: phys={g('D16','physiological','a')}+{g('D16','physiological','b')} | "
          f"love={g('D16','love_belonging','a')}+{g('D16','love_belonging','b')}")
    print(f"D17. Enneagram: 3={g('D17','3_achiever','a')}+{g('D17','3_achiever','b')} | "
          f"9={g('D17','9_peacemaker','a')}+{g('D17','9_peacemaker','b')}")
    print()
    
    print("--- E. Dark Side ---")
    print(f"E18. Gaslight: {g('E18','confuse','a')}+{g('E18','confuse','b')} confuse | "
          f"deny={g('E18','deny_said','a')}+{g('E18','deny_said','b')}")
    e19 = fw.get('E19', {})
    if 'disappearances' in e19:
        d = e19['disappearances']
        print(f"E19. Trauma Bond: disappearances={d['count']}, avg_gap={d['avg_gap_hours']}h")
    print(f"E20. Silent: punitive={fw.get('E20',{}).get('punitive',{}).get('count',0)}, "
          f"ratio={fw.get('E20',{}).get('punitive_ratio',0)}%")
    print(f"E21. Codep: control={g('E21','control_behaviors','a')}+{g('E21','control_behaviors','b')} | "
          f"deny={g('E21','deny_needs','a')}+{g('E21','deny_needs','b')}")
    print()
    
    print("--- F. Behavior ---")
    f22 = fw.get('F22', {})
    if 'chase_sequences' in f22:
        cs = f22['chase_sequences']
        print(f"F22. Habits: chase_a={cs.get('a',0)}, chase_b={cs.get('b',0)}, "
              f"fight_disappear={f22.get('fight_disappear',0)}")
    print(f"F23. BIS/BAS: BIS={g('F23','bis','a')}+{g('F23','bis','b')} | "
          f"BAS={g('F23','bas','a')}+{g('F23','bas','b')}")
    print(f"F24. SRH: fondness={g('F24','fondness','a')}+{g('F24','fondness','b')} | "
          f"shared={g('F24','shared_meaning','a')}+{g('F24','shared_meaning','b')}")
    print()
    
    print("--- Additional Metrics ---")
    rt = add['response_time']
    print(f"Response Time: A={rt['a']['median']}s B={rt['b']['median']}s (median)")
    conv = add['conversations']
    print(f"Conversations: {conv['total']}, avg={conv['avg_length']} msgs, "
          f"A_init={conv['a_initiate_pct']}% B_init={conv['b_initiate_pct']}%")
    tod = add['time_of_day']
    print(f"Time of Day: A_peak={tod['peak_hour_a']} B_peak={tod['peak_hour_b']} | "
          f"late_night A={tod['late_night_pct_a']}% B={tod['late_night_pct_b']}%")
    ms = add['message_stats']
    print(f"Msg Length: A_median={ms['a']['median_length']} B_median={ms['b']['median_length']}")
    print()
    
    eb = data.get('emotional_bursts', {})
    print(f"--- Emotional Bursts ---")
    print(f"A: {eb.get('a_count',0)} bursts, avg_intensity={eb.get('a_avg_intensity',0)}, avg_len={eb.get('a_avg_length',0)}")
    print(f"B: {eb.get('b_count',0)} bursts, avg_intensity={eb.get('b_avg_intensity',0)}, avg_len={eb.get('b_avg_length',0)}")
    print()
    
    corr = data.get('correlations', {})
    if corr.get('strong_pairs'):
        print("--- Strong Correlations (|r| > 0.5) ---")
        for p in corr['strong_pairs'][:5]:
            print(f"  {p['metrics'][0]} <-> {p['metrics'][1]}: r={p['r']} (n={p['n']})")
    print()
    
    output_path = data.get('meta', {}).get('output_file', 'unknown')
    print(f"Results saved to: {output_path}")

# ============================================================================
# MAIN
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Relationship Deep Analysis - 24 Framework Data Collection'
    )
    parser.add_argument('json_path', help='Path to chat JSON file')
    parser.add_argument('--output', '-o', default=None, help='Output JSON file path')
    parser.add_argument('--sender-a', default=None, help='Sender A (user) identifier')
    parser.add_argument('--sender-b', default=None, help='Sender B (partner) identifier')
    parser.add_argument('--quiet', action='store_true', help='Only save JSON, no console output')
    args = parser.parse_args()
    
    # Load data
    print(f"Loading: {args.json_path}")
    msgs = load_data(args.json_path)
    print(f"Loaded {len(msgs):,} messages")
    
    # Identify parties
    parties = identify_parties(msgs, args.sender_a, args.sender_b)
    is_a = make_is_func(parties['a_id'])
    is_b = make_is_func(parties['b_id'])
    
    print(f"Party A: {parties['a_id']} ({parties['a_count']:,} msgs)")
    print(f"Party B: {parties['b_id']} ({parties['b_count']:,} msgs)")
    print()
    
    # Run all frameworks
    print("Running 24 framework analysis...")
    framework_results, monthly_data, burst_data = run_all_frameworks(msgs, is_a, is_b)
    print("  Frameworks done.")
    
    # Additional metrics
    print("Computing additional metrics...")
    additional = compute_additional_metrics(msgs, is_a, is_b)
    print("  Additional metrics done.")
    
    # Normalization
    normalized = normalize_per_1k(framework_results, parties['a_count'], parties['b_count'])
    
    # Correlations
    print("Computing correlations...")
    correlations = compute_correlations(monthly_data, framework_results,
                                          parties['a_count'], parties['b_count'])
    print("  Correlations done.")
    
    # Determine output path
    output_path = args.output
    if not output_path:
        base = os.path.splitext(args.json_path)[0]
        output_path = base + '_analysis.json'
    
    # Assemble output
    output = {
        'meta': {
            'input_file': args.json_path,
            'output_file': output_path,
            'total_messages': len(msgs),
            'total_days': additional['date_range']['total_days'],
            'date_range': additional['date_range'],
            'party_a': {
                'sender': parties['a_id'],
                'messages': parties['a_count'],
                'pct': parties['a_pct']
            },
            'party_b': {
                'sender': parties['b_id'],
                'messages': parties['b_count'],
                'pct': parties['b_pct']
            }
        },
        'frameworks': framework_results,
        'monthly_trends': {m: dict(monthly_data[m]) for m in sorted(monthly_data.keys())},
        'normalized': normalized,
        'emotional_bursts': burst_data,
        'additional_metrics': additional,
        'correlations': correlations
    }
    
    # Save
    save_json(output, output_path)
    print(f"\nResults saved to: {output_path}")
    
    # Print summary
    if not args.quiet:
        print()
        print_summary(output)

if __name__ == '__main__':
    main()
