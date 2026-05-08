from typing import List, Dict, Any
import chromadb
from chromadb.config import Settings

class MemorySystem:
    def __init__(self):
        # 使用ChromaDB作为向量记忆库
        self.client = chromadb.Client(Settings(anonymized_telemetry=False))
        
        # 创建collection存储历史谈判案例
        self.case_library = self.client.create_collection("contract_cases")
        
        # 共享白板 - 当前任务的公共记忆
        self.shared_whiteboard: List[Dict[str, Any]] = []
        
        # 各Agent的私有记忆
        self.private_memories: Dict[str, List] = {}
    
    def add_to_whiteboard(self, entry: Dict[str, Any]):
        """添加到共享白板"""
        self.shared_whiteboard.append(entry)
    
    def get_whiteboard(self) -> List[Dict]:
        return self.shared_whiteboard
    
    def add_private_memory(self, agent_name: str, memory: Any):
        if agent_name not in self.private_memories:
            self.private_memories[agent_name] = []
        self.private_memories[agent_name].append(memory)
    
    def clear_task_memory(self):
        """新任务开始时清理白板"""
        self.shared_whiteboard = []
    
    def store_case(self, case_id: str, summary: str, metadata: Dict):
        """存储历史案例到向量数据库"""
        self.case_library.add(
            documents=[summary],
            metadatas=[metadata],
            ids=[case_id]
        )
    
    def query_similar_cases(self, query: str, n_results: int = 3) -> List:
        """查询相似历史案例"""
        results = self.case_library.query(
            query_texts=[query],
            n_results=n_results
        )
        return results
