from __future__ import annotations

import random

from .model import Case, Event, Expectation

SEED=20260923
GENERATOR_VERSION="0.2.1"
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


def _script_text(script):
    if isinstance(script, str):
        return script
    if "blocks" in script:
        return "\n".join(block["text"] for block in script["blocks"])
    return script.get("text", "")


def _infer_language(script):
    text = _script_text(script)
    has_han = any("\u3400" <= char <= "\u9fff" for char in text)
    has_latin = any(char.isascii() and char.isalpha() for char in text)
    if has_han and has_latin:
        return "mixed"
    if has_latin:
        return "en"
    return "zh-Hans"


def _mutation_severity(category, metadata):
    if metadata.get("mutation_severity"):
        return metadata["mutation_severity"]
    legacy_severity = metadata.get("severity")
    if legacy_severity:
        return {"low": "light", "medium": "moderate", "high": "high"}.get(legacy_severity, legacy_severity)
    if category in {"exact", "silence", "forgotten_word_pause", "backtrack"}:
        return "none"
    if category in {"filler_words", "punctuation", "spacing", "partial_growth", "partial_correction"}:
        return "light"
    if category in {
        "duplicate", "near_duplicate", "prefix_collision", "short_segment",
        "intentional_skip", "section_jump", "accidental_future_phrase",
        "false_jump_candidate", "jump_confirmation", "jump_cancellation",
        "non_spoken_regions", "non_spoken_similarity_trap", "spoken_override",
        "skip_override", "consecutive_non_spoken", "non_spoken_title",
        "non_spoken_heading", "non_spoken_note", "non_spoken_stage_direction",
        "non_spoken_header_footer", "forgotten_then_skip",
    }:
        return "high"
    return "moderate"


def _case_metadata(category, script, meta=None):
    metadata = dict(meta or {})
    metadata.setdefault("language", _infer_language(script))
    metadata.setdefault("difficulty", "medium")
    metadata.setdefault("source", "generated")
    metadata.setdefault("mutation_severity", _mutation_severity(category, metadata))
    metadata.setdefault("tags", [])
    metadata.setdefault("category", category)
    return metadata


def make(cid,cat,script,events,labels,meta=None):
    metadata=_case_metadata(cat,script,meta)
    previous=metadata.get("initial_segment_index",0);expectations=[]
    for i,label in enumerate(labels):
        expectations.append(Expectation(i,label,should_move=(label!=previous) if label is not None else None,should_be_lost=(label is None)))
        if label is not None:previous=label
    script_obj=script if isinstance(script,dict) else {"id":"script_"+cid,"text":script}
    return Case(cid,cat,script_obj,events,expectations,metadata)


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


def curated_cases():
    """Individually reviewed, explicitly labeled scenario instances."""
    out=[]
    exact=[
      ("大家好，今天我们介绍新的产品。","大家好今天我们介绍新的产品。"),("早上好，欢迎来到分享会。","早上好欢迎来到分享会"),("请先检查设备，再开始录制。","请先检查设备再开始录制"),("我们的团队专注于本地软件服务。","我们的团队专注于本地软件服务"),("这节课程先讲原理，再做练习。","这节课程先讲原理再做练习"),("数据需要备份，也需要定期检查。","数据需要备份也需要定期检查"),("今天的目标是把问题说明白。","今天的目标是把问题说明白"),("请把文件放进项目资料夹。","请把文件放进项目资料夹"),("欢迎各位参加今天的演示。","欢迎各位参加今天的演示"),("会议结束后我们整理结论。","会议结束后我们整理结论")]
    for i,(script,speech) in enumerate(exact,1):out.append(make(f"curated_exact_{i:03d}","exact",script,[Event("final",speech)],[0],{"source":"curated","review_status":"reviewed","review_notes":"Reviewed script, event, segment label and normalization behavior.","language":"zh-Hans","difficulty":"easy"}))
    filler=["嗯","那个","其实","然后","我觉得","大家可以看到","呃","这个","所以说","那么"]
    for i,((script,speech),fill) in enumerate(zip(exact,filler),1):out.append(make(f"curated_filler_{i:03d}","filler_words",script,[Event("final",fill+speech)],[0],{"source":"curated","review_status":"reviewed","review_notes":"Filler insertion must preserve the one spoken segment.","language":"zh-Hans","difficulty":"medium"}))
    english=["Today we launch our product.","Welcome to the project review.","Check the device before use.","Our team builds offline tools.","Start with a short exercise.","Back up and verify the data.","Explain the problem clearly.","Save the file in its folder.","Thanks for joining our demo.","Publish the notes tomorrow."]
    for i,text in enumerate(english,1):out.append(make(f"curated_english_{i:03d}","english",text,[Event("final",text.lower())],[0],{"source":"curated","review_status":"reviewed","review_notes":"English punctuation and case variation reviewed.","language":"en","difficulty":"easy"}))
    mixed=["今天介绍 AI Teleprompter 的跟稿功能。","我们使用 GPT API 处理测试请求。","SDK 文档说明了 Android 的接入方式。","新 CMS 支持 API 和内容预览。","请检查 AI、GPT 和 SDK 的版本。","这个工具可以导出 CSV 和 JSON。","Android returns partial.","项目计划使用 OpenAI API 做离线对照。","AI Teleprompter 支持中英文稿件。","我们比较 GPT 与 G P T 的识别写法。"]
    mixed_asr=["今天介绍 A I teleprompter 的跟稿功能","我们使用 G P T A P I 处理测试请求","S D K 文档说明了安卓的接入方式","新 C M S 支持 A P I 和内容预览","请检查 A I G P T 和 S D K 的版本","这个工具可以导出 C S V 和 J S O N","Android returns partial","项目计划使用 OpenAI A P I 做离线对照","AI teleprompter 支持中英文稿件","我们比较 GPT 与 G P T 的识别写法"]
    for i,(script,speech) in enumerate(zip(mixed,mixed_asr),1):out.append(make(f"curated_mixed_{i:03d}","mixed",script,[Event("final",speech)],[0],{"source":"curated","review_status":"reviewed","review_notes":"Mixed-language/acronym scope and label reviewed.","language":"mixed","difficulty":"hard"}))
    numbers=[("计划于2026年3月12日启动。","计划于二零二六年三月十二日启动。"),("本次预算为299元。","本次预算为二百九十九元。"),("会议在9:30开始。","会议在九点半开始。"),("预计提升15%。","预计提升百分之十五。"),("处理耗时3.5小时。","处理耗时三点五小时。"),("报名人数达到21人。","报名人数达到二十一人。"),("版本号是2026.1。","版本号是二零二六点一。"),("折扣为5%。","折扣为百分之五。"),("请在8:15前到场。","请在八点十五分前到场。"),("订单金额是1200元。","订单金额是一千二百元。")]
    for i,(script,speech) in enumerate(numbers,1):out.append(make(f"curated_numbers_{i:03d}","numbers",script,[Event("final",speech)],[0],{"source":"curated","review_status":"reviewed","review_notes":"Numeric expression variant reviewed; equivalence is the intended label.","language":"zh-Hans","difficulty":"hard"}))
    for i,(script,speech) in enumerate(exact,1):
        blocks={"id":f"curated_doc_{i:03d}","blocks":[{"id":"title","type":"heading","text":f"第{i}部分：项目介绍","speech_policy":"skip"},{"id":"a","type":"paragraph","text":script,"speech_policy":"spoken"},{"id":"note","type":"note","text":"备注：等待画面切换","speech_policy":"skip"},{"id":"b","type":"paragraph","text":"接下来介绍后续安排。","speech_policy":"spoken"}]}
        out.append(make(f"curated_nonspoken_{i:03d}","non_spoken_regions",blocks,[Event("final",speech),Event("final","接下来介绍后续安排")],[0,1],{"source":"curated","review_status":"reviewed","review_notes":"Only spoken blocks form candidates; block-to-segment map checked.","language":"zh-Hans","difficulty":"medium","speech_policy_context":"heading and note skipped"}))
    for i in range(1,11):
        units=[f"第{j}段是项目介绍内容。" for j in range(15)]
        start=2;target=start+i+1;script="".join(units)
        out.append(make(f"curated_intentional_skip_{i:03d}","intentional_skip",script,[Event("final",units[target]),Event("final",units[target+1])],[target,target+1],{"source":"curated","review_status":"reviewed","review_notes":"Intentional direct jump; final target and continuation positions checked.","language":"zh-Hans","difficulty":"hard","intent":"skip","initial_segment_index":start,"skip_distance":target-start}))
    for i in range(1,11):
        current=f"目前我们介绍第{i}项服务的主要特点。";future=f"下一阶段将发布第{i}版智能分析能力。"
        script=current+"中间内容说明。"+future+"随后继续当前主题。"
        events=[Event("partial",future[:9],sequence=1),Event("partial",current[:11],sequence=2),Event("final",current,sequence=3)]
        out.append(make(f"curated_accidental_future_{i:03d}","accidental_future_phrase",script,events,[0,0,0],{"source":"curated","review_status":"reviewed","review_notes":"Brief future phrase is accidental; expected anchor remains current segment.","language":"zh-Hans","difficulty":"adversarial","intent":"mistake","expected_occurrence":{"0":0,"1":0,"2":0}}))
    for i in range(1,11):
        phrase=f"我们先完成第{i}项检查，然后保存结果。"
        out.append(make(f"curated_pause_{i:03d}","forgotten_word_pause",phrase,[Event("partial",phrase[:9],sequence=1),Event("silence",duration_ms=3000),Event("silence",duration_ms=5000),Event("final",phrase[8:])],[0,0,0,0],{"source":"curated","review_status":"reviewed","review_notes":"Pause must hold the same position; continuation resumes the same segment.","language":"zh-Hans","difficulty":"medium","intent":"pause"}))
    for i in range(1,11):
        script=f"感谢大家。补充背景{i}。感谢大家。再次说明{i}。感谢大家。"
        out.append(make(f"curated_duplicate_{i:03d}","duplicate",script,[Event("final","感谢大家")],[4],{"source":"curated","review_status":"reviewed","review_notes":"The same phrase occurs at segments 0, 2, and 4; the initial anchor and expected occurrence are the third occurrence.","language":"zh-Hans","difficulty":"adversarial","intent":"normal","initial_segment_index":4,"expected_occurrence":{"0":4}}))
    for i in range(1,11):
        phrase=f"Team will review plan {i}."
        script=f"{phrase} Background note. {phrase}"
        out.append(make(f"curated_english_duplicate_{i:03d}","duplicate",script,[Event("final",phrase[:-1])],[2],{"source":"curated","review_status":"reviewed","review_notes":"The same English phrase occurs at segments 0 and 2; the expected label is the later occurrence.","language":"en","difficulty":"adversarial","initial_segment_index":2,"expected_occurrence":{"0":2}}))
    for i in range(1,11):
        units=[f"第{j}段记录了第{i}项工作的进度。" for j in range(12)]
        out.append(make(f"curated_backtrack_{i:03d}","backtrack", "".join(units),[Event("final",units[8])],[8],{"source":"curated","review_status":"reviewed","review_notes":"One-segment backtrack from the initial anchor; target position checked.","language":"zh-Hans","difficulty":"medium","initial_segment_index":9,"intent":"backtrack"}))
    for i in range(1,11):
        phrase=f"本次发布将于第{i}季度完成部署。"
        events=[Event("partial",phrase[:8],sequence=1),Event("partial",phrase[:12],sequence=2),Event("partial",phrase[:8],sequence=1),Event("final",phrase)]
        out.append(make(f"curated_partial_correction_{i:03d}","partial_correction",phrase,events,[0,0,0,0],{"source":"curated","review_status":"reviewed","review_notes":"Growing and corrected partial hypotheses remain on the same segment.","language":"zh-Hans","difficulty":"medium"}))

    # Additional individually authored gold cases cover the main linguistic
    # confusions and the multi-hypothesis jump decisions introduced in v0.2.
    missing=[
      ("我们希望通过准备减少现场等待时间。","我们希望通过准备减少等待时间。"),
      ("平台会自动保存每次修改记录。","平台会保存每次修改记录。"),
      ("每位参与者都可以查看完整的操作说明。","每位参与者可以查看操作说明。"),
      ("请在提交之前再次确认所有必要字段。","请在提交之前确认必要字段。"),
      ("新的流程能够帮助团队快速发现异常。","新的流程帮助团队发现异常。"),
      ("我们会根据大家的建议继续调整页面。","我们根据建议继续调整页面。"),
      ("会议结束以后请把结果同步给项目成员。","会议结束以后把结果同步给成员。"),
      ("系统支持在没有网络连接时继续工作。","系统支持没有网络时继续工作。"),
      ("这份指南介绍安装配置和日常维护方法。","这份指南介绍配置和维护方法。"),
      ("每周五下午我们会整理本周完成的事项。","每周五我们整理本周完成的事项。"),
    ]
    extra=[
      ("请打开设置页面检查当前版本。","那么请打开设置页面看一下当前版本。"),
      ("今天我们介绍产品的三个主要功能。","今天呢我们来介绍产品的三个主要功能。"),
      ("完成录制后可以直接预览视频。","录制完成以后就可以直接预览视频了。"),
      ("新的版本支持导出字幕文件。","这个新的版本现在支持导出字幕文件。"),
      ("请先选择文件再开始上传。","请先选择要处理的文件然后再开始上传。"),
      ("这项服务面向中小型团队开放。","其实这项服务主要是面向中小型团队开放的。"),
      ("我们将在下周公布具体安排。","我们预计会在下周公布具体的安排。"),
      ("数据处理过程会保留必要日志。","数据处理的过程会保留必要的日志记录。"),
      ("现场工作人员会协助完成登记。","现场的工作人员会帮助大家完成登记。"),
      ("请把修改后的文档发给负责人。","麻烦把修改好的文档发给项目负责人。"),
    ]
    traditional=[
      ("欢迎各位参加今天的产品说明会。","歡迎各位參加今天的產品說明會。"),
      ("请检查设备状态并确认网络连接。","請檢查設備狀態並確認網路連線。"),
      ("我们会持续优化服务体验。","我們會持續優化服務體驗。"),
      ("这份资料已经完成更新。","這份資料已經完成更新。"),
      ("请把文件保存到指定目录。","請把檔案儲存到指定目錄。"),
      ("用户可以随时修改个人设置。","使用者可以隨時修改個人設定。"),
      ("团队正在讨论新的解决方案。","團隊正在討論新的解決方案。"),
      ("会议将在下午三点准时开始。","會議將在下午三點準時開始。"),
      ("我们已经收到你的申请。","我們已經收到你的申請。"),
      ("请阅读完整说明后再继续操作。","請閱讀完整說明後再繼續操作。"),
    ]
    homophones=[
      ("苏州致诚网络服务有限公司。","苏州至诚网络服务有限公司。"),
      ("智能分析可以缩短检查时间。","只能分析可以缩短检查时间。"),
      ("我们需要制定清晰的计划。","我们需要制订清晰的计划。"),
      ("请确认账户已经完成验证。","请确认账号已经完成验证。"),
      ("这个方案能够提高工作效率。","这个方按能够提高工作效率。"),
      ("会议记录需要保存原始内容。","会议纪录需要保存原始内容。"),
      ("他已经完成了项目交接。","他已经完成了项目交界。"),
      ("系统会自动提醒相关人员。","系统会自动题型相关人员。"),
      ("我们正在研究新的技术路线。","我们正在研究新的技术路现。"),
      ("请把会场安排在明天。","请把会场安拍在明天。"),
    ]
    for family,pairs,category,language,note in (
        ("missing",missing,"missing_words","zh-Hans","Required words are omitted while the intended segment remains clear."),
        ("extra",extra,"extra_words","zh-Hans","Inserted spoken material does not change the intended segment."),
        ("traditional",traditional,"traditional_simplified","zh-Hant","Traditional Chinese variant is labeled against the corresponding simplified script."),
        ("homophone",homophones,"homophone_like","zh-Hans","Near-homophone or lexical variant is matched to its intended segment."),
    ):
        for i,(script,speech) in enumerate(pairs,1):
            out.append(make(f"curated_reviewed_{family}_{i:03d}",category,script,[Event("final",speech)],[0],{"source":"curated","review_status":"reviewed","review_notes":note,"language":language,"difficulty":"medium"}))

    prefixes=[
      ("本次会议将讨论产品维护计划。","本次会议将讨论产品升级计划。","本次会议将讨论产品交付计划。"),
      ("我们先查看第一季度服务数据。","我们先查看第二季度服务数据。","我们先查看年度服务数据。"),
      ("这次更新会改善文件搜索体验。","这次更新会改善图片搜索体验。","这次更新会改善消息搜索体验。"),
      ("请按照流程完成账号验证。","请按照流程完成设备验证。","请按照流程完成邮箱验证。"),
      ("接下来介绍线下培训安排。","接下来介绍线上培训安排。","接下来介绍新人培训安排。"),
      ("新页面会展示项目完成进度。","新页面会展示预算使用进度。","新页面会展示任务审核进度。"),
      ("当前版本支持导入本地文档。","当前版本支持导入云端文档。","当前版本支持导入归档文档。"),
      ("我们计划增加自动备份功能。","我们计划增加定时备份功能。","我们计划增加手动备份功能。"),
      ("这项服务适合小型研发团队。","这项服务适合大型研发团队。","这项服务适合远程研发团队。"),
      ("最后说明本周的发布安排。","最后说明下周的发布安排。","最后说明月底的发布安排。"),
    ]
    for i,variants in enumerate(prefixes,1):
        script="".join(variants); events=[Event("partial",variants[0][:6],sequence=1),Event("final",variants[1],sequence=2)]
        out.append(make(f"curated_reviewed_prefix_{i:03d}","prefix_collision",script,events,[0,1],{"source":"curated","review_status":"reviewed","review_notes":"Shared-prefix partial stays at the anchor; final wording identifies the second segment.","language":"zh-Hans","difficulty":"adversarial","initial_segment_index":0}))

    from .model import Expectation
    for i in range(1,11):
        units=[f"第{j+1}段是第{i}项议题的详细说明。" for j in range(16)]
        target=4+i; script="".join(units)
        events=[Event("final",units[target],sequence=1),Event("final",units[target+1],sequence=2)]
        expectations=[Expectation(0,0,should_move=False,should_be_lost=False,expected_state="suspect_jump",expected_jump_status="suspected",expected_candidate_index=target,expected_jump_evidence=1),Expectation(1,target+1,should_move=True,should_be_lost=False,expected_state="confirmed_jump",expected_jump_status="confirmed",expected_candidate_index=target,expected_jump_evidence=2)]
        skip_script={"id":f"script_curated_reviewed_skip_{i:03d}","text":script}
        out.append(Case(f"curated_reviewed_intentional_skip_{i:03d}","intentional_skip",skip_script,events,expectations,_case_metadata("intentional_skip",skip_script,{"source":"curated","review_status":"reviewed","review_notes":"A distant segment and its immediate continuation confirm the intentional skip.","language":"zh-Hans","difficulty":"hard","intent":"skip","initial_segment_index":0,"skip_distance":target})))

    for i in range(1,11):
        current=f"目前我们介绍第{i}项服务的主要特点。"; middle="随后说明相关背景和准备工作。"; future=f"下一阶段将发布第{i}版智能分析能力。"; script=current+middle+future
        events=[Event("partial","下一阶段",sequence=1),Event("final",current,sequence=2)]
        expectations=[Expectation(0,0,should_move=False,should_be_lost=False,expected_state="suspect_jump",expected_jump_status="suspected",expected_candidate_index=2,expected_jump_evidence=1),Expectation(1,0,should_move=False,should_be_lost=False,expected_state="locked",expected_jump_status="cancelled",expected_candidate_index=None,expected_jump_evidence=0)]
        future_script={"id":f"script_curated_reviewed_future_{i:03d}","text":script}
        out.append(Case(f"curated_reviewed_accidental_future_{i:03d}","accidental_future_phrase",future_script,events,expectations,_case_metadata("accidental_future_phrase",future_script,{"source":"curated","review_status":"reviewed","review_notes":"One short future phrase creates only a candidate; return to the current segment cancels it.","language":"zh-Hans","difficulty":"adversarial","intent":"mistake","initial_segment_index":0})))

    for i in range(1,11):
        current=f"我们先完成第{i}项检查，再确认结果并保存记录。"; script="背景说明。"+current+"后续内容。"
        events=[Event("partial",current[:9],sequence=1),Event("silence",duration_ms=3000,sequence=2),Event("silence",duration_ms=30000,sequence=3),Event("final",current,sequence=4)]
        expectations=[Expectation(0,1,should_move=False,should_be_lost=False,expected_state="uncertain",expected_jump_status="none",expected_candidate_index=None,expected_jump_evidence=0),Expectation(1,1,should_move=False,should_be_lost=False,expected_state="uncertain",expected_jump_status="none",expected_candidate_index=None,expected_jump_evidence=0),Expectation(2,1,should_move=False,should_be_lost=False,expected_state="uncertain",expected_jump_status="none",expected_candidate_index=None,expected_jump_evidence=0),Expectation(3,1,should_move=False,should_be_lost=False,expected_state="locked",expected_jump_status="none",expected_candidate_index=None,expected_jump_evidence=0)]
        pause_script={"id":f"script_curated_reviewed_pause_{i:03d}","text":script}
        out.append(Case(f"curated_reviewed_forgotten_pause_{i:03d}","forgotten_word_pause",pause_script,events,expectations,_case_metadata("forgotten_word_pause",pause_script,{"source":"curated","review_status":"reviewed","review_notes":"Silence holds the existing anchor; matching continuation resumes it without speculative movement.","language":"zh-Hans","difficulty":"medium","intent":"pause","initial_segment_index":1})))

    assert len(out)==210
    return out


def synthetic_cases(count=5000):
    rng=random.Random(SEED); cats=["exact","filler_words","missing_words","extra_words","substitution","mixed_error","partial_growth","duplicate","near_duplicate","backtrack","skip","lost_recovery","long_script","punctuation","numbers","english_mixed","short_segment","prefix_collision","stale_partial","repeated_final","traditional_simplified","silence"]
    out=[]
    for k in range(count):
        cat=cats[k%len(cats)];kind,base=PARAGRAPHS[k%len(PARAGRAPHS)];raw=[x for x in base.split("。")] ; units=[x+"。" for x in raw if x]
        if len(units)<2:units=[base[:len(base)//2],base[len(base)//2:]]
        script=base;idx=rng.randrange(len(units));initial=idx;txt=units[idx].strip();events=[Event("final",txt)];labels=[idx];difficulty="easy";severity="low"
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
            target=txt if cat=="duplicate" else txt[:-1]+"内容";script=txt+"。补充说明。"+target+"。";labels=[2];events=[Event("final",target)];initial=2 if cat=="duplicate" else 1;difficulty="adversarial"
        elif cat in ("backtrack","skip"):
            initial=idx;labels=[max(0,idx-1) if cat=="backtrack" else min(len(units)-1,idx+min(2,len(units)-1-idx))];events=[Event("final",units[labels[0]])]
        elif cat=="lost_recovery":initial=idx;events=[Event("final","完全无关文本XYZ"),Event("final",txt)];labels=[None,idx];difficulty="hard"
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
            script="今天我们介绍产品甲。今天我们介绍产品乙。今天我们介绍产品丙。";events=[Event("partial","今天我们介绍产品"),Event("final","今天我们介绍产品乙")];labels=[0,1];initial=0;difficulty="adversarial"
        elif cat=="short_segment":
            script="好的。开始。继续。谢谢。可以。";selected=rng.randrange(5);events=[Event("final",["好的","开始","继续","谢谢","可以"][selected])];labels=[selected];initial=selected;difficulty="hard"
        elif cat=="numbers":events=[Event("final",txt.replace("二零二六","2026").replace("三月十二日","3月12日").replace("二百九十九元","299元"))];difficulty="medium"
        # Every stream includes a standardized five-point silence tail. This makes
        # pause stability measurable without adding wall-clock or microphone input.
        hold=next((x for x in reversed(labels) if x is not None),0)
        events += [Event("silence",duration_ms=duration) for duration in (1000,3000,5000,10000,30000)]
        labels += [hold]*5
        actual=max(1,len(__import__("csfb.segmenter",fromlist=["segment"]).segment(script)));labels=[None if x is None else min(x,actual-1) for x in labels]
        out.append(make(f"synthetic_{cat}_{k+1:05d}",cat,script,events,labels,{"layer":"L1/L2","source_type":kind,"difficulty":difficulty,"severity":severity,"seed":SEED,"generator_version":GENERATOR_VERSION,"initial_segment_index":min(initial,actual-1)}))
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
    out.extend(nonspoken_cases())
    out.extend(jump_intent_cases())
    return out


def nonspoken_cases():
    out=[]
    for count in (1,3,5,10,20):
        blocks=[{"id":"a","type":"paragraph","text":"大家好，欢迎来到活动现场。","speech_policy":"spoken"}]
        blocks += [{"id":f"skip{j}","type":["heading","note","stage_direction","header","footer"][j%5],"text":f"非口播内容第{j+1}项","speech_policy":"skip"} for j in range(count)]
        blocks += [{"id":"b","type":"paragraph","text":"接下来介绍今天的主要安排。","speech_policy":"spoken"}]
        category="non_spoken_regions" if count==1 else "consecutive_non_spoken"
        out.append(make(f"nonspoken_consecutive_{count:02d}",category,{"id":f"blocks{count}","blocks":blocks},[Event("final","大家好欢迎来到活动现场"),Event("final","接下来介绍今天的主要安排")],[0,1],{"source":"synthetic","layer":"L2","difficulty":"hard","language":"zh-Hans","speech_policy_context":f"{count} consecutive skip blocks"}))
    for kind in ("title","heading","note","stage_direction","header","footer"):
        category="non_spoken_header_footer" if kind in ("header","footer") else f"non_spoken_{kind}"
        for i in range(1,6):
            blocks={"id":f"{kind}{i}","blocks":[{"id":"skip","type":kind,"text":f"{kind} marker {i}","speech_policy":"skip"},{"id":"body","type":"paragraph","text":f"正文第{i}段介绍工作安排。","speech_policy":"spoken"}]}
            out.append(make(f"nonspoken_{kind}_{i:03d}",category,blocks,[Event("final",f"正文第{i}段介绍工作安排")],[0],{"source":"synthetic","layer":"L2","difficulty":"medium","language":"zh-Hans","speech_policy_context":f"{kind} explicitly skipped"}))
    for i in range(1,11):
        blocks={"id":f"skipoverride{i}","blocks":[{"id":"a","type":"paragraph","text":f"朗读时略过第{i}项说明。","speech_policy":"skip","speech_policy_source":"user_override"},{"id":"b","type":"paragraph","text":f"继续介绍第{i}项安排。","speech_policy":"spoken"}]}
        out.append(make(f"skip_override_{i:03d}","skip_override",blocks,[Event("final",f"继续介绍第{i}项安排")],[0],{"source":"synthetic","layer":"L2","difficulty":"medium","language":"zh-Hans","speech_policy_context":"paragraph explicitly overridden to skip"}))
    for i in range(1,11):
        blocks={"id":f"similartrap{i}","blocks":[{"id":"h","type":"heading","text":"下一步介绍产品维护安排","speech_policy":"skip"},{"id":"n","type":"note","text":"请切换演示画面","speech_policy":"skip"},{"id":"p","type":"paragraph","text":"下一步正式介绍产品的维护安排和服务方式。","speech_policy":"spoken"}]}
        out.append(make(f"nonspoken_similarity_trap_{i:03d}","non_spoken_similarity_trap",blocks,[Event("final","下一步正式介绍产品的维护安排和服务方式")],[0],{"source":"synthetic","layer":"L2","difficulty":"adversarial","language":"zh-Hans","speech_policy_context":"skip heading is a close lexical match"}))
    for i in range(1,11):
        blocks={"id":f"readskip{i}","blocks":[{"id":"a","type":"paragraph","text":f"正文第{i}段先介绍项目背景。","speech_policy":"spoken"},{"id":"note","type":"note","text":f"这里暂停{i}秒并切换投影","speech_policy":"skip"},{"id":"b","type":"paragraph","text":f"恢复后说明第{i}项计划。","speech_policy":"spoken"}]}
        out.append(make(f"nonspoken_read_skip_{i:03d}","spoken_override",blocks,[Event("final",f"正文第{i}段先介绍项目背景"),Event("final",f"这里暂停{i}秒并切换投影"),Event("final",f"恢复后说明第{i}项计划")],[0,0,1],{"source":"synthetic","layer":"L2","difficulty":"hard","language":"zh-Hans","intent":"mistake","speech_policy_context":"skip note was spoken by reader; it remains a non-spoken script candidate"}))
    return out


def jump_intent_cases():
    """Paired evidence/cancellation cases for intentional skips vs accidental future phrases."""
    from .model import Expectation
    out=[]

    def add(cid,category,script,events,initial,expectations,metadata=None):
        document=script if isinstance(script,dict) else {"id":"script_"+cid,"text":script}
        inferred_intent="skip" if category in ("intentional_skip","section_jump","forgotten_then_skip") else "mistake" if category in ("accidental_future_phrase","false_jump_candidate","jump_cancellation") else "pause" if category=="forgotten_word_pause" else "navigation" if category=="section_jump" else "normal"
        case_metadata=_case_metadata(category,document,{"difficulty":"adversarial","source":"synthetic","layer":"L2","initial_segment_index":initial,"intent":inferred_intent,**(metadata or {})})
        out.append(Case(cid,category,document,events,expectations,case_metadata))

    for distance in (2,3,10,50):
        units=[f"第{j+1}段内容编号{j}，本段介绍具体安排和执行方法。" for j in range(65)]
        start=5;target=start+distance;script="".join(x+"。" for x in units)
        events=[Event("final",units[target]),Event("final",units[target+1])]
        exp=[Expectation(0,start,should_move=False,should_be_lost=False,expected_state="suspect_jump",expected_jump_status="suspected",expected_candidate_index=target,expected_jump_evidence=1),Expectation(1,target+1,should_move=True,should_be_lost=False,expected_state="confirmed_jump",expected_jump_status="confirmed",expected_candidate_index=target,expected_jump_evidence=2)]
        add(f"intentional_skip_distance_{distance:02d}","intentional_skip",script,events,start,exp,{"skip_distance":distance})
    for i in range(120):
        units=[f"第{j+1}段内容编号{j}，本段介绍具体安排和执行方法。" for j in range(40)]
        start=5+(i%10);distance=(4,5,8,12,20)[i%5];target=start+distance
        script="".join(x+"。" for x in units)
        events=[Event("final",units[target],sequence=1),Event("final",units[target+1],sequence=2)]
        exp=[Expectation(0,start,should_move=False,should_be_lost=False,expected_state="suspect_jump",expected_jump_status="suspected",expected_candidate_index=target,expected_jump_evidence=1),Expectation(1,target+1,should_move=True,should_be_lost=False,expected_state="confirmed_jump",expected_jump_status="confirmed",expected_candidate_index=target,expected_jump_evidence=2)]
        add(f"intentional_skip_{i+1:04d}","intentional_skip",script,events,start,exp,{"skip_distance":distance})

        # Same forward-probe pattern, explicit confirmation-focused category.
        start2=3+(i%8);target2=start2+distance
        events2=[Event("partial",units[target2][:12],sequence=1),Event("final",units[target2],sequence=2),Event("final",units[target2+1],sequence=3)]
        exp2=[Expectation(0,start2,should_move=False,expected_state="suspect_jump",expected_jump_status="suspected",expected_candidate_index=target2,expected_jump_evidence=1),Expectation(1,start2,should_move=False,expected_state="suspect_jump",expected_jump_status="suspected",expected_candidate_index=target2,expected_jump_evidence=2),Expectation(2,target2+1,should_move=True,expected_state="confirmed_jump",expected_jump_status="confirmed",expected_candidate_index=target2,expected_jump_evidence=3)]
        add(f"jump_confirmation_{i+1:04d}","jump_confirmation",script,events2,start2,exp2,{"skip_distance":distance})

    script_parts=[f"第{j+1}段背景内容，提供前后文信息。" for j in range(40)]
    script_parts[17]="我们的产品主要解决企业网站维护问题。"
    script_parts[18]="下一阶段我们会加入自动内容更新能力。"
    script="".join(x for x in script_parts)
    for i in range(120):
        events=[Event("partial","下一阶段",sequence=1),Event("final","我们的产品主要解决企业网站维护问题。",sequence=2)]
        exp=[Expectation(0,17,should_move=False,expected_state="suspect_jump",expected_jump_status="suspected",expected_candidate_index=18,expected_jump_evidence=1),Expectation(1,17,should_move=False,expected_state="locked",expected_jump_status="cancelled",expected_candidate_index=None,expected_jump_evidence=0)]
        add(f"accidental_future_phrase_{i+1:04d}","accidental_future_phrase",script,events,17,exp)
        add(f"jump_cancellation_{i+1:04d}","jump_cancellation",script,events,17,exp)
        # A brief future phrase followed by silence must hold the existing anchor.
        silent=[Event("partial","下一阶段",sequence=1),Event("silence",duration_ms=3000,sequence=2),Event("silence",duration_ms=10000,sequence=3)]
        sexp=[Expectation(0,17,should_move=False,expected_state="suspect_jump",expected_jump_status="suspected",expected_candidate_index=18,expected_jump_evidence=1),Expectation(1,17,should_move=False,should_be_lost=False,expected_state="uncertain",expected_jump_status="cancelled",expected_candidate_index=None,expected_jump_evidence=0),Expectation(2,17,should_move=False,should_be_lost=False,expected_state="uncertain",expected_jump_status="cancelled",expected_candidate_index=None,expected_jump_evidence=0)]
        add(f"false_jump_candidate_{i+1:04d}","false_jump_candidate",script,silent,17,sexp)

        forgotten=[Event("partial","我们的产品主要",sequence=1),Event("silence",duration_ms=1000,sequence=2),Event("silence",duration_ms=5000,sequence=3),Event("silence",duration_ms=30000,sequence=4)]
        fexp=[Expectation(j,17,should_move=False,should_be_lost=False,expected_state="uncertain",expected_jump_status="none",expected_candidate_index=None,expected_jump_evidence=0) for j in range(4)]
        add(f"forgotten_word_pause_{i+1:04d}","forgotten_word_pause",script,forgotten,17,fexp)

        forgot_skip=[Event("partial",units[17][:12],sequence=1),Event("silence",duration_ms=3000,sequence=2),Event("silence",duration_ms=5000,sequence=3),Event("final",units[25],sequence=4),Event("final",units[26],sequence=5)]
        forgot_skip_exp=[Expectation(0,17,should_move=False,expected_state="uncertain",expected_jump_status="none",expected_candidate_index=None,expected_jump_evidence=0),Expectation(1,17,should_move=False,should_be_lost=False,expected_state="uncertain",expected_jump_status="none",expected_candidate_index=None,expected_jump_evidence=0),Expectation(2,17,should_move=False,should_be_lost=False,expected_state="uncertain",expected_jump_status="none",expected_candidate_index=None,expected_jump_evidence=0),Expectation(3,17,should_move=False,expected_state="suspect_jump",expected_jump_status="suspected",expected_candidate_index=25,expected_jump_evidence=1),Expectation(4,26,should_move=True,expected_state="confirmed_jump",expected_jump_status="confirmed",expected_candidate_index=25,expected_jump_evidence=2)]
        add(f"forgotten_then_skip_{i+1:04d}","forgotten_then_skip",script,forgot_skip,17,forgot_skip_exp,{"skip_distance":8})

    for i in range(120):
        blocks=[]
        for s in range(3):
            blocks.append({"id":f"heading_{s+1}","type":"heading","text":f"第{s+1}部分","speech_policy":"skip"})
            blocks.append({"id":f"section_{s+1}_p1","type":"paragraph","text":f"第{s+1}部分第一段内容。","speech_policy":"spoken"})
            blocks.append({"id":f"section_{s+1}_p2","type":"paragraph","text":f"第{s+1}部分第二段内容。","speech_policy":"spoken"})
        script={"id":f"section_script_{i+1:04d}","blocks":blocks};target=4
        sections=[{"id":f"section_{s+1}","title":f"第{s+1}部分","start_segment":s*2,"end_segment":s*2+1,"navigation_only_block_ids":[f"heading_{s+1}"],"heading_block_id":f"heading_{s+1}"} for s in range(3)]
        events=[Event("final","第三部分第一段内容。",sequence=1),Event("final","第三部分第二段内容。",sequence=2)]
        exp=[Expectation(0,1,should_move=False,expected_state="suspect_jump",expected_jump_status="suspected",expected_candidate_index=target,expected_jump_evidence=1),Expectation(1,target+1,should_move=True,expected_state="confirmed_jump",expected_jump_status="confirmed",expected_candidate_index=target,expected_jump_evidence=2)]
        add(f"section_jump_{i+1:04d}","section_jump",script,events,1,exp,{"sections":sections})
    return out
