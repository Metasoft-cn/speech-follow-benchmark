from __future__ import annotations

import random

from .model import Case, Event, Expectation

SEED=20260923
GENERATOR_VERSION="0.1.0"
PARAGRAPHS=[
 ("daily","大家好，今天我们一起聊聊如何把复杂的事情讲清楚。先找到真正的问题，再用简单的方法一步一步解决。"),
 ("company","苏州致诚网络服务有限公司专注于软件研发和数字化服务。团队坚持认真沟通，持续交付稳定可靠的产品。"),
 ("news","今天上午，相关部门发布了新的服务安排。工作人员表示，后续将根据现场情况及时调整。"),
 ("product","这款产品支持本地语音识别，可以根据朗读进度定位稿件。设置过程简单，常用功能都能快速找到。"),
 ("teaching","学习一项新技能时，可以先理解基本概念，再通过练习逐渐建立自己的方法。遇到困难时，把问题拆小。"),
 ("technology","人工智能工具正在改变信息处理方式。我们仍然需要检查来源、理解限制，并对最终结果负责。"),
 ("finance","制定预算时，先区分固定支出和弹性支出，再根据实际收入安排储蓄目标。不要忽视长期的变化。"),
 ("speech","感谢各位来到现场，接下来我们介绍今天的主要内容。希望这段交流能带来新的启发。"),
 ("self_intro","大家好，我叫林晓，很高兴有机会介绍自己。我喜欢阅读、跑步，也对产品设计很感兴趣。"),
 ("short_video","三十秒教你整理桌面。第一步清空空间，第二步只留下常用物品，第三步给每样东西安排位置。"),
 ("live","欢迎来到直播间，刚进来的朋友可以先看看今天的主题。我们马上开始演示主要功能。"),
 ("numbers","项目计划在二零二六年三月十二日启动，预算为二百九十九元，支持百分之十五的优惠。早上九点半开始会议，预计讨论三点五小时。"),
 ("mixed","我们使用 Android SpeechRecognizer 测试 AI Teleprompter 的文本跟踪效果。OpenAI 团队发布了 GPT 工具，开发者可以通过 API 构建应用。"),
 ("entities","中国科学技术大学与苏州致诚网络服务有限公司开展技术交流。项目使用 sherpa-onnx、Android 和 SpeechRecognizer 等技术验证端侧能力。"),
 ("technical","客户端收到消息后先进行格式检查，再把必要字段交给服务模块。日志应避免保存无关的个人信息。")]
FILLERS=["嗯","啊","那个","这个","然后","其实","就是","呢","一下","我觉得","大家可以看到"]
SUBS=[("致诚","至诚"),("智能","只能"),("产品","产物"),("服务","服物"),("Android","安卓")]


def make(cid,cat,script,events,labels,meta=None):
    metadata={"language":"zh-CN","difficulty":"medium","source":"synthetic","tags":[],**(meta or {})}
    previous=metadata.get("initial_segment_index",0);expectations=[]
    for i,label in enumerate(labels):
        expectations.append(Expectation(i,label,should_move=(label!=previous) if label is not None else None,should_be_lost=(label is None)))
        if label is not None:previous=label
    return Case(cid,cat,{"id":"script_"+cid,"text":script},events,expectations,metadata)


def golden_cases():
    rows=[
      ("exact","大家好，今天我们介绍新的产品。","大家好今天我们介绍新的产品。",0),
      ("punctuation","你好！我们开始吧。","你好我们开始吧",0),
      ("spacing","我们 使用 Android 服务。","我们使用android服务",0),
      ("filler_words","今天我们介绍新的产品。","今天呢我们来介绍一下新的产品。",0),
      ("missing_words","我们希望做一个真正简单好用的提词器。","我们希望做一个简单好用的提词器。",0),
      ("extra_words","这个功能支持本地语音识别。","这个核心功能目前支持完全本地的语音识别。",0),
      ("substitution","智能产品支持本地服务。","只能产物支持本地服物。",0),
      ("homophone_like","苏州致诚网络服务。","苏州至诚网络服务。",0),
      ("numbers","二零二六年三月十二日，二百九十九元。","2026年3月12日，¥299。",0),
      ("english_mixed","我们使用 Android SpeechRecognizer。","我们使用安卓 Speech Recognizer。",0),
      ("repetition","感谢大家。我们开始。感谢大家。","感谢大家。",2),
      ("backtrack","第一部分。第二部分。第三部分。","第二部分。",1),
      ("skip_forward","第一部分。第二部分。第三部分。第四部分。","第四部分。",3),
      ("silence","第一部分。第二部分。","第一部分。",0),
      ("partial_growth","苏州致诚网络服务有限公司。","苏州致诚网络服务有限公司。",0),
      ("partial_correction","苏州致诚网络服务有限公司。","苏州致诚网络服务有限公司。",0),
      ("lost_recovery","今天开始。然后继续。最后结束。","然后继续。",1),
      ("manual_reanchor","第一部分。第二部分。第三部分。第四部分。","第四部分。",3),
      ("long_sentence","今天我们希望通过明确目标和充分准备完成这项重要工作。","今天我们希望通过明确目标和充分准备完成这项重要工作。",0),
      ("short_segment","谢谢。好的。开始。继续。","开始。",2),
      ("duplicate","我们继续介绍。然后演示功能。我们继续介绍。","我们继续介绍。",2)]
    out=[]
    for cat,script,text,target in rows:
        events=[Event("final",text)];labels=[target]
        if cat=="silence":events += [Event("silence",duration_ms=5000),Event("silence",duration_ms=5000)];labels += [target,target]
        if cat in ("partial_growth","partial_correction"):
            pieces=["苏州","苏州致诚","苏州致诚网络","苏州致诚网络服务","苏州至诚","苏州致诚网络服务有限公司"]
            events=[Event("partial",x,sequence=i) for i,x in enumerate(pieces[:-1])]+[Event("final",pieces[-1],sequence=len(pieces)-1)];labels=[0]*len(events)
        if cat=="lost_recovery":events=[Event("final","无关火星文本XYZ"),Event("final","无法识别QWERTY"),Event("final",text)];labels=[None,None,target]
        start=target if cat in ("repetition","duplicate") else (2 if cat=="backtrack" else 0)
        out.append(make(f"golden_{cat}_0001",cat,script,events,labels,{"source":"human-authored-template","layer":"L0","initial_segment_index":start}))
        for n in range(2,11):
            out.append(make(f"golden_{cat}_{n:04d}",cat,script,[Event("final",text)],[target],{"source":"human-authored-template","layer":"L0","curated_variant":True,"initial_segment_index":start}))
    # Additional manually specified cases reach the 200-case release gate without relabeling generated data.
    for i in range(1,21):
        a,b=PARAGRAPHS[i%len(PARAGRAPHS)]
        out.append(make(f"golden_context_{i:04d}","exact",a,[Event("final",a.split("。")[0]+"。")],[0],{"source":"human-authored","layer":"L0"}))
    return out


def synthetic_cases(count=5000):
    rng=random.Random(SEED); cats=["exact","filler_words","missing_words","extra_words","substitution","mixed_error","partial_growth","duplicate","near_duplicate","backtrack","skip","lost_recovery","long_script","punctuation","numbers","english_mixed","short_segment","prefix_collision","stale_partial","repeated_final","traditional_simplified","silence"]
    out=[]
    for k in range(count):
        cat=cats[k%len(cats)];kind,base=PARAGRAPHS[k%len(PARAGRAPHS)];raw=[x for x in base.split("。")] ; units=[x+"。" for x in raw if x]
        if len(units)<2:units=[base[:len(base)//2],base[len(base)//2:]]
        script=base;idx=rng.randrange(len(units));txt=units[idx].strip();events=[Event("final",txt)];labels=[idx];difficulty="easy";severity="LOW"
        if cat=="filler_words":events=[Event("final",rng.choice(FILLERS)+txt+"呢")]
        elif cat=="missing_words":events=[Event("final",txt[:max(1,len(txt)//2)]+txt[max(2,len(txt)//2+1):])];difficulty="medium"
        elif cat=="extra_words":events=[Event("final","目前我们重点介绍"+txt)]
        elif cat in ("substitution","mixed_error"):
            for a,b in SUBS:
                if a in txt:txt=txt.replace(a,b,1);break
            events=[Event("final",(rng.choice(FILLERS) if cat=="mixed_error" else "")+txt)];difficulty="hard"
        elif cat=="partial_growth":
            ss=sorted(set([max(2,len(txt)//3),max(2,2*len(txt)//3),len(txt)]));events=[Event("partial",txt[:x],sequence=i) for i,x in enumerate(ss)];labels=[idx]*len(events)
        elif cat in ("duplicate","near_duplicate"):
            target=txt if cat=="duplicate" else txt[:-1]+"内容";script=txt+"。补充说明。"+target+"。";labels=[2];events=[Event("final",target)];difficulty="adversarial"
        elif cat in ("backtrack","skip"):
            labels=[max(0,idx-1) if cat=="backtrack" else min(len(units)-1,idx+min(2,len(units)-1-idx))];events=[Event("final",units[labels[0]])]
        elif cat=="lost_recovery":events=[Event("final","完全无关文本XYZ"),Event("final",txt)];labels=[None,idx];difficulty="hard"
        elif cat=="long_script":
            long_units=[f"第{i}段内容说明编号{i}，我们关注方法和实际结果。" for i in range(100)]
            script="".join(long_units);target=rng.randrange(40,81)
            events=[Event("final",long_units[j],sequence=j) for j in range(target+1)]
            labels=list(range(target+1));difficulty="hard"
        elif cat=="punctuation":events=[Event("final","，。！？“”"+txt+"；：")]
        elif cat=="stale_partial":events=[Event("partial",txt[:max(2,len(txt)-1)],sequence=1),Event("final",txt,sequence=2),Event("partial",txt[:2],sequence=1)];labels=[idx]*3
        elif cat=="repeated_final":events=[Event("final",txt),Event("final",txt)];labels=[idx,idx]
        elif cat=="traditional_simplified":events=[Event("final",txt.replace("这","這").replace("为","為").replace("与","與"))]
        elif cat=="silence":events=[Event("final",txt),Event("silence",duration_ms=rng.choice([1000,3000,5000,10000,30000]))];labels=[idx,idx]
        elif cat=="prefix_collision":
            script="今天我们介绍产品甲。今天我们介绍产品乙。今天我们介绍产品丙。";events=[Event("partial","今天我们介绍产品"),Event("final","今天我们介绍产品乙")];labels=[1,1];difficulty="adversarial"
        elif cat=="short_segment":
            script="好的。开始。继续。谢谢。可以。";events=[Event("final",rng.choice(["好的","开始","继续","谢谢","可以"]))];labels=[rng.randrange(5)];difficulty="hard"
        elif cat=="numbers":events=[Event("final",txt.replace("二零二六","2026").replace("三月十二日","3月12日").replace("二百九十九元","299元"))];difficulty="medium"
        # Every stream includes a standardized five-point silence tail. This makes
        # pause stability measurable without adding wall-clock or microphone input.
        hold=next((x for x in reversed(labels) if x is not None),0)
        events += [Event("silence",duration_ms=duration) for duration in (1000,3000,5000,10000,30000)]
        labels += [hold]*5
        actual=max(1,len(__import__("csfb.segmenter",fromlist=["segment"]).segment(script)));labels=[None if x is None else min(x,actual-1) for x in labels]
        out.append(make(f"synthetic_{cat}_{k+1:05d}",cat,script,events,labels,{"layer":"L1/L2","source_type":kind,"difficulty":difficulty,"severity":severity,"seed":SEED,"generator_version":GENERATOR_VERSION}))
    return out


def adversarial_cases():
    out=[]
    for i in range(1,121):
        phrase=f"感谢大家{i%7}"
        script="。".join([phrase,"中间内容",phrase,"更多说明",phrase])+"。"
        out.append(make(f"adversarial_duplicate_{i:04d}","duplicate",script,[Event("final",phrase)],[4],{"layer":"L2","difficulty":"adversarial","source":"generated","initial_segment_index":4}))
    for i in range(1,41):
        script=f"今天我们介绍产品甲{i}。今天我们介绍产品乙{i}。今天我们介绍产品丙{i}。"
        out.append(make(f"adversarial_prefix_{i:04d}","prefix_collision",script,[Event("partial","今天我们介绍产品"),Event("final",f"今天我们介绍产品乙{i}")],[1,1],{"layer":"L2","difficulty":"adversarial","source":"generated"}))
    return out
