"""Base agent implementation."""
from typing import Dict, Any, Optional, List
from uuid import UUID
import asyncio
from ..structure import AgentProfile, Role
from framework.core.providers.ollama import OllamaProvider

class BaseAgent:
    """Base agent class with core functionality."""
    
    def __init__(
        self,
        profile: AgentProfile,
        provider: Optional[OllamaProvider] = None
    ):
        """Initialize base agent.
        
        Args:
            profile: Agent profile
            provider: Optional language model provider
        """
        self.profile = profile
        self.provider = provider
        self.task_history: List[Dict[str, Any]] = []
        self._lock = asyncio.Lock()
        
    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a task.
        
        Args:
            task: Task specification
            
        Returns:
            Task result
        """
        async with self._lock:
            try:
                result = await self._process_task(task)
                self._update_task_history(task, result)
                return result
            except Exception as e:
                error_result = {
                    "success": False,
                    "error": str(e)
                }
                self._update_task_history(task, error_result)
                return error_result
    
    async def _process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process task implementation.
        
        Args:
            task: Task specification
            
        Returns:
            Task result
            
        Raises:
            NotImplementedError: Must be implemented by subclasses
        """
        raise NotImplementedError("Subclasses must implement _process_task")
    
    def _update_task_history(
        self,
        task: Dict[str, Any],
        result: Dict[str, Any]
    ) -> None:
        """Update task history.
        
        Args:
            task: Original task
            result: Task result
        """
        self.task_history.append({
            "task": task,
            "result": result,
            "agent_id": self.profile.agent_id,
            "role": self.profile.role.name
        })
    
    def get_performance_metrics(self) -> Dict[str, float]:
        """Calculate current performance metrics.
        
        Returns:
            Performance metrics dictionary
        """
        total_tasks = len(self.task_history)
        if total_tasks == 0:
            return {}
            
        successful_tasks = sum(
            1 for task in self.task_history
            if task["result"].get("success", False)
        )
        
        return {
            "task_completion": successful_tasks / total_tasks,
            "total_tasks": total_tasks
        }
        
    async def collaborate(
        self,
        other_agent: 'BaseAgent',
        task: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Collaborate with another agent on a task.
        
        Args:
            other_agent: Agent to collaborate with
            task: Task specification
            
        Returns:
            Collaboration result
        """
        # Execute task with both agents
        my_result = await self.execute_task(task)
        other_result = await other_agent.execute_task(task)
        
        # Combine results
        return {
            "success": my_result.get("success", False) and other_result.get("success", False),
            "my_result": my_result,
            "other_result": other_result
        }
