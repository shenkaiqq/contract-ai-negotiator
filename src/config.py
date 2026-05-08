import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    MODEL_NAME = "gpt-4"  # 或 gpt-3.5-turbo
    MAX_DEBATE_ROUNDS = 3  # 熔断轮数
    CONFIDENCE_THRESHOLD = 0.7  # 需要人工介入的阈值
    
    # Agent角色定义
    AGENT_ROLES = {
        "parser": "合同解析专家，负责提取关键条款和变更点",
        "defender": "本方法务代表，站在企业立场审查风险",
        "opponent_sim": "对方律师模拟器，预测对方可能的反驳策略",
        "arbitrator": "仲裁Agent，综合各方意见给出最终建议"
    }
