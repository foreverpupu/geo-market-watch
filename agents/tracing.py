"""
Tracing - Agent 执行日志记录

用于记录 agent 执行日志和输入输出信息。
"""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any


class AgentTracer:
    """Agent 执行追踪器。"""
    
    def __init__(self, log_dir: str = "/tmp/geo_market_traces"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.current_trace = None
    
    def start_trace(self, input_text: str, metadata: dict = None) -> str:
        """开始新的追踪会话。"""
        trace_id = f"trace_{uuid.uuid4().hex[:12]}"
        
        self.current_trace = {
            "trace_id": trace_id,
            "started_at": datetime.now().isoformat(),
            "input_text": input_text,
            "input_metadata": metadata or {},
            "steps": [],
        }
        
        return trace_id
    
    def log_agent_execution(
        self,
        agent_name: str,
        input_view: dict,
        output_update: dict,
        execution_time_ms: float,
        metadata: dict = None,
    ) -> None:
        """记录 Agent 执行。"""
        if self.current_trace is None:
            return
        
        step = {
            "step_number": len(self.current_trace["steps"]) + 1,
            "agent_name": agent_name,
            "timestamp": datetime.now().isoformat(),
            "execution_time_ms": execution_time_ms,
            "input_view": input_view,
            "output_update": output_update,
            "metadata": metadata or {},
        }
        
        self.current_trace["steps"].append(step)
    
    def log_short_circuit(
        self,
        agent_name: str,
        reason: str,
        metadata: dict = None,
    ) -> None:
        """记录短路终止。"""
        if self.current_trace is None:
            return
        
        step = {
            "step_number": len(self.current_trace["steps"]) + 1,
            "agent_name": agent_name,
            "timestamp": datetime.now().isoformat(),
            "short_circuit": True,
            "reason": reason,
            "metadata": metadata or {},
        }
        
        self.current_trace["steps"].append(step)
    
    def end_trace(self, final_state: dict, success: bool = True) -> str:
        """结束追踪会话并保存。"""
        if self.current_trace is None:
            return ""
        
        self.current_trace["ended_at"] = datetime.now().isoformat()
        self.current_trace["final_state"] = final_state
        self.current_trace["success"] = success
        
        # 保存到文件
        trace_file = self.log_dir / f"{self.current_trace['trace_id']}.json"
        with open(trace_file, "w", encoding="utf-8") as f:
            json.dump(self.current_trace, f, indent=2, ensure_ascii=False)
        
        trace_id = self.current_trace["trace_id"]
        self.current_trace = None
        
        return str(trace_file)
    
    def get_trace_summary(self) -> dict:
        """获取当前追踪摘要。"""
        if self.current_trace is None:
            return {}
        
        return {
            "trace_id": self.current_trace["trace_id"],
            "step_count": len(self.current_trace["steps"]),
            "agents_executed": list(set(
                step["agent_name"] for step in self.current_trace["steps"]
            )),
        }


class ConsoleTracer:
    """控制台追踪器（简单输出）。"""
    
    @staticmethod
    def log_agent_start(agent_name: str):
        """记录 Agent 开始。"""
        print(f"\n{'='*60}")
        print(f"Agent: {agent_name}")
        print(f"{'='*60}")
    
    @staticmethod
    def log_agent_output(agent_name: str, output: dict):
        """记录 Agent 输出。"""
        print("\nOutput:")
        for key, value in output.items():
            print(f"  {key}: {value}")
    
    @staticmethod
    def log_short_circuit(agent_name: str, reason: str):
        """记录短路。"""
        print(f"\n⚠️  Short Circuit: {reason}")
    
    @staticmethod
    def log_state_update(field: str, value: Any):
        """记录状态更新。"""
        print(f"  → State update: {field} = {value}")
