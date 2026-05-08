import json
from typing import Dict, Any, List
from rich.console import Console
from rich.panel import Panel
from agents import (
    ContractParserAgent, DefenderAgent, 
    OpponentSimulatorAgent, ArbitratorAgent,
    AgentMessage
)
from memory import MemorySystem
from config import Config

console = Console()

class MultiAgentOrchestrator:
    def __init__(self):
        self.parser = ContractParserAgent()
        self.defender = DefenderAgent()
        self.opponent = OpponentSimulatorAgent()
        self.arbitrator = ArbitratorAgent()
        self.memory = MemorySystem()
        self.debate_round = 0
        
    def analyze_contract(self, contract_text: str) -> Dict[str, Any]:
        """多Agent合同分析主流程"""
        
        console.print(Panel.fit("🚀 启动多Agent合同分析", style="bold blue"))
        
        # 1. 解析阶段
        console.print("\n[bold yellow]阶段1: 合同解析[/bold yellow]")
        parse_result = self.parser.think(
            task=f"请分析这份合同，提取关键条款和修改点:\n{contract_text}",
            context={"task": "contract_parsing"}
        )
        self._log_agent_output(parse_result)
        
        # 2. 防守方分析
        console.print("\n[bold yellow]阶段2: 本方法务审查[/bold yellow]")
        defender_result = self.defender.think(
            task=f"基于解析结果，从公司立场审查风险:\n{parse_result.conclusion}",
            context={"parsed_contract": parse_result.conclusion}
        )
        self._log_agent_output(defender_result)
        
        # 3. 对手模拟
        console.print("\n[bold yellow]阶段3: 对手策略模拟[/bold yellow]")
        opponent_result = self.opponent.think(
            task=f"作为对方律师，请反驳本方法务的风险判断:\n{defender_result.conclusion}",
            context={
                "our_position": defender_result.conclusion,
                "our_evidence": defender_result.evidence
            }
        )
        self._log_agent_output(opponent_result)
        
        # 4. 谈判模拟循环(带熔断)
        console.print("\n[bold yellow]阶段4: 谈判博弈模拟[/bold yellow]")
        debate_result = self._debate_loop(defender_result, opponent_result)
        
        # 5. 仲裁与建议
        console.print("\n[bold yellow]阶段5: 仲裁与策略建议[/bold yellow]")
        final_result = self.arbitrator.think(
            task=f"综合双方立场，给出最终建议:\n{json.dumps(debate_result, ensure_ascii=False)}",
            context={
                "defender_position": defender_result.conclusion,
                "opponent_position": opponent_result.conclusion,
                "debate_history": debate_result
            }
        )
        self._log_agent_output(final_result)
        
        # 6. 生成最终报告
        report = self._generate_report(parse_result, final_result, debate_result)
        
        return report
    
    def _debate_loop(self, defender_msg: AgentMessage, opponent_msg: AgentMessage) -> Dict:
        """Agent辩论循环，带熔断机制"""
        debate_history = []
        
        while self.debate_round < Config.MAX_DEBATE_ROUNDS:
            self.debate_round += 1
            
            console.print(f"\n[cyan]辩论回合 {self.debate_round}/{Config.MAX_DEBATE_ROUNDS}[/cyan]")
            
            # 检查是否需要熔断
            if self._should_break(defender_msg, opponent_msg):
                console.print("[red]⚠️ 触发熔断：双方陷入僵局[/red]")
                break
            
            # 防守方回应
            defender_msg = self.defender.think(
                task=f"回应对方论点：{opponent_msg.conclusion}",
                context={"opponent_argument": opponent_msg.conclusion},
                shared_memory=debate_history
            )
            
            # 对方回击
            opponent_msg = self.opponent.think(
                task=f"回应防守方论点：{defender_msg.conclusion}",
                context={"defender_argument": defender_msg.conclusion},
                shared_memory=debate_history
            )
            
            debate_history.append({
                "round": self.debate_round,
                "defender": defender_msg.dict(),
                "opponent": opponent_msg.dict()
            })
        
        return {
            "total_rounds": self.debate_round,
            "history": debate_history,
            "stalemate": self.debate_round >= Config.MAX_DEBATE_ROUNDS
        }
    
    def _should_break(self, msg1: AgentMessage, msg2: AgentMessage) -> bool:
        """判断是否触发熔断"""
        # 如果双方置信度都很高但结论相反，可能陷入僵局
        if msg1.confidence > 0.8 and msg2.confidence > 0.8:
            # 简单判断：如果上一轮也这样，就该熔断
            if self.debate_round > 1:
                return True
        return False
    
    def _log_agent_output(self, message: AgentMessage):
        """格式化输出Agent消息"""
        panel = Panel(
            f"[bold]结论:[/bold] {message.conclusion}\n"
            f"[bold]置信度:[/bold] {message.confidence}\n"
            f"[bold]依据:[/bold] {', '.join(message.evidence)}\n"
            f"[bold]建议行动:[/bold] {message.next_action or '无'}",
            title=f"🤖 {message.agent_name}",
            border_style="green"
        )
        console.print(panel)
    
    def _generate_report(self, parse_result, final_result, debate_result) -> Dict:
        """生成最终报告"""
        report = {
            "合同摘要": parse_result.conclusion,
            "风险等级": self._calculate_risk_level(final_result),
            "谈判策略": final_result.conclusion,
            "建议话术": final_result.next_action,
            "博弈分析": f"经过{debate_result['total_rounds']}轮模拟谈判",
            "是否需要法务介入": final_result.confidence < Config.CONFIDENCE_THRESHOLD
        }
        
        console.print("\n" + "="*50)
        console.print(Panel.fit("📊 最终分析报告", style="bold green"))
        console.print_json(json.dumps(report, ensure_ascii=False, indent=2))
        
        return report
    
    def _calculate_risk_level(self, final_result) -> str:
        if final_result.confidence > 0.8:
            return "高风险"
        elif final_result.confidence > 0.5:
            return "中风险"
        else:
            return "低风险"
