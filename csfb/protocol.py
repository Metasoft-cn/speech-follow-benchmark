from __future__ import annotations

import json
import subprocess
import time


class SubprocessAdapter:
    """JSONL stdin/stdout adapter. Commands execute arbitrary local code."""
    def __init__(self, command):
        self.proc=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,encoding="utf-8",bufsize=1)

    def send(self,message):
        self.proc.stdin.write(json.dumps(message,ensure_ascii=False)+"\n");self.proc.stdin.flush()
        line=self.proc.stdout.readline()
        if not line:raise RuntimeError("engine closed stdout before returning a prediction")
        return json.loads(line)

    def load_script(self,script_id,text,segments,initial_segment_index=0):return self.send({"type":"load_script","script_id":script_id,"text":text,"segments":[{"index":i,"text":s} for i,s in enumerate(segments)],"initial_segment_index":initial_segment_index})
    def process_event(self,event):return self.send(event)
    def close(self):
        if self.proc.stdin:self.proc.stdin.close()
        try:self.proc.wait(timeout=2)
        except subprocess.TimeoutExpired:self.proc.terminate()
