import json
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from openai import OpenAI
from config import Config

client = OpenAI(api_key=Config.OPENAI_API_KEY)

class AgentMessage(BaseModel):
    """Agent间标准通信格式"""
    agent_name: str
    conclusion: str
    evidence: List[str]
    confidence: float
    next_action: Optional[str] = None

class BaseAgent:
    def __init__(self, name: str, role: str, system_prompt: str):
        self.name = name
        self.role = role
        self.system_prompt = system_prompt
        self.private_memory = []  # 私有记忆
        
    def think(self, task: str, context: Dict[str, Any], shared_memory: List = None) -> AgentMessage:
        """Agent思考并返回结构化结果"""
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "system", "content": f"当前上下文: {json.dumps(context, ensure_ascii=False)}"}
        ]
        
        if shared_memory:
            messages.append({
                "role": "system", 
                "content": f"共享记忆: {json.dumps(shared_memory, ensure_ascii=False)}"
            })
            
        messages.append({"role": "user", "content": task})
        
        # 要求JSON输出
        messages.append({
            "role": "system", 
            "content": "请以JSON格式回复: {\"conclusion\":\"结论\",\"evidence\":[\"依据1\"],\"confidence\":0.9,\"next_action\":\"建议下一步\"}"
        })
        
        response = client.chat.completions.create(
            model=Config.MODEL_NAME,
            messages=messages,
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        
        message = AgentMessage(
            agent_name=self.name,
            conclusion=result.get("conclusion", ""),
            evidence=result.get("evidence", []),
            confidence=result.get("confidence", 0.5),
            next_action=result.get("next_action")
        )
        
        # 添加到私有记忆
        self.private_memory.append(message)
        
        return message


class ContractParserAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="合同解析Agent",
            role="parser",
            system_prompt="""你是一个专业的合同解析专家。你的职责是：
1. 识别合同中的所有关键条款
2. 标注哪些条款被修改过
3. 提取风险点
4. 保持客观中立，不做策略判断"""
        )

class DefenderAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="本方法务Agent",
            role="defender",
            system_prompt="""你代表本企业的法务立场。在审查合同时：
1. 优先保护公司知识产权和数据安全
2. 关注责任上限、赔偿条款
3. 维护有利的付款条款
4. 对不利修改必须明确指出来"""
        )

class OpponentSimulatorAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="对方模拟Agent",
            role="opponent_sim",
            system_prompt="""你模拟对方律师的思考方式：
1. 总是寻找对我方(对方企业)最有利的解释
2. 坚持对对方有利的条款修改
3. 引用行业惯例作为支撑
4. 预测对方会用什么策略反驳"""
        )

class ArbitratorAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="仲裁Agent",
            role="arbitrator",
            system_prompt="""你是中立仲裁人，综合各方意见后：
1. 评估每个争议点的实际风险
2. 给出具体的修改建议文本
3. 提供谈判策略（坚持/让步/交换）
4. 引用历史数据和行业标准"""
        )
