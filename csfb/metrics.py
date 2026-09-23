import math
import statistics


def percentile(xs,p):
    if not xs:return 0
    ys=sorted(xs);return ys[min(len(ys)-1,math.ceil(p*len(ys))-1)]


def score(rows):
    judged=[r for r in rows if r["expected"] is not None]
    finals=[r for r in judged if r["event_type"]=="final"]
    def expected_set(r):return [r["expected"]]+(r.get("acceptable_segments") or [])
    def error(r):return min(abs(r["predicted"]-x) for x in expected_set(r))
    def acc(rs,n=0):return sum(error(r)<=n for r in rs)/len(rs) if rs else None
    err=[error(r) for r in judged]
    cf=[r for r in judged if r["confidence"] is not None]
    high=[r for r in cf if r["confidence"]>=.8]
    wrong_f=[r for r in judged if r.get("moved_forward_wrong")]
    wrong_b=[r for r in judged if r.get("moved_backward_wrong")]
    cat_abs=[r for r in judged if error(r)>=5]
    cat_back=[r for r in judged if r["predicted"]<min(expected_set(r))-2]
    lost=[r for r in rows if r["state"]=="lost"]
    lost_annotated=[r for r in rows if r.get("should_be_lost") is not None]
    false_lost=[r for r in lost_annotated if r["state"]=="lost" and r["should_be_lost"] is False]
    false_lost_denominator=sum(r["should_be_lost"] is False for r in lost_annotated)
    no_move=[r for r in rows if r.get("should_move") is False]
    wrong_movement=[r for r in no_move if r["moved"]]
    lat=[r["latency_us"] for r in rows]
    bycase={}
    for r in rows:bycase.setdefault(r["case_id"],[]).append(r)
    recoveries=[];lost_cases=0;recovered_cases=0
    for seq in bycase.values():
        lost_at=next((i for i,r in enumerate(seq) if r["state"]=="lost"),None)
        if lost_at is not None:
            lost_cases+=1
            recovered_at=next((i for i,r in enumerate(seq[lost_at+1:],lost_at+1) if r["state"]=="recovered"),None)
            if recovered_at is not None:recovered_cases+=1;recoveries.append(recovered_at-lost_at)
    reversals=0
    for seq in bycase.values():
        anchors=[r["predicted"] for r in seq if r["event_type"]=="partial"]
        reversals+=sum((b-a)*(c-b)<0 for a,b,c in zip(anchors,anchors[1:],anchors[2:]))
    n=max(1,len(judged))
    return {"event_accuracy":acc(judged),"final_accuracy":acc(finals),"within_1_accuracy":acc(judged,1),"within_2_accuracy":acc(judged,2),"mae_segments":statistics.mean(err) if err else None,"median_ae_segments":statistics.median(err) if err else None,"p95_segment_error":percentile(err,.95),"wrong_forward_jump_rate":len(wrong_f)/n,"wrong_backward_jump_rate":len(wrong_b)/n,"wrong_movement_rate":len(wrong_movement)/len(no_move) if no_move else None,"catastrophic_absolute_rate":len(cat_abs)/n,"catastrophic_backward_rate":len(cat_back)/n,"lost_rate":len(lost)/max(1,len(rows)),"false_lost_rate":len(false_lost)/false_lost_denominator if false_lost_denominator else None,"recovery_success_rate":recovered_cases/lost_cases if lost_cases else None,"median_recovery_events":statistics.median(recoveries) if recoveries else None,"p95_recovery_events":percentile(recoveries,.95) if recoveries else None,"anchor_reversal_count":reversals,"high_confidence_accuracy":sum(error(r)==0 for r in high)/len(high) if high else None,"high_confidence_wrong_rate":sum(error(r)>0 for r in high)/len(high) if high else None,"latency_mean_us":statistics.mean(lat) if lat else 0,"latency_median_us":statistics.median(lat) if lat else 0,"latency_p95_us":percentile(lat,.95),"latency_p99_us":percentile(lat,.99),"judged_events":len(judged),"final_events":len(finals),"total_events":len(rows)}
