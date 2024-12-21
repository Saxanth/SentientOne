"""Utility functions for the agency framework."""
from typing import Dict, Any, List, Type, Optional
from uuid import UUID
import asyncio
from concurrent.futures import ThreadPoolExecutor

from .structure import AgentProfile, Role, Department
from .internal import BaseAgent
from .specialized import ResearchAgent, DeveloperAgent, TesterAgent

class AgentFactory:
    """Factory for creating specialized agents."""
    
    _agent_types: Dict[Role, Type[BaseAgent]] = {
        Role.RESEARCHER: ResearchAgent,
        Role.DEVELOPER: DeveloperAgent,
        Role.TESTER: TesterAgent,
    }
    
    @classmethod
    def create_agent(cls, profile: AgentProfile) -> Optional[BaseAgent]:
        """Create an agent instance based on role.
        
        Args:
            profile: Agent profile with role
            
        Returns:
            Specialized agent instance or None if role not supported
        """
        agent_class = cls._agent_types.get(profile.role)
        if agent_class:
            return agent_class(profile=profile)
        return None

class TaskOrchestrator:
    """Orchestrates tasks between multiple agents."""
    
    def __init__(self, max_workers: int = 5):
        """Initialize orchestrator.
        
        Args:
            max_workers: Maximum number of concurrent tasks
        """
        self._executor = ThreadPoolExecutor(max_workers=max_workers)
        self._tasks: Dict[UUID, asyncio.Task] = {}
    
    async def execute_parallel(
        self,
        agents: List[BaseAgent],
        task: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Execute task across multiple agents in parallel.
        
        Args:
            agents: List of agents
            task: Task specification
            
        Returns:
            List of results from each agent
        """
        tasks = [
            asyncio.create_task(agent.execute_task(task))
            for agent in agents
        ]
        self._tasks.update({agent.profile.agent_id: task for agent, task in zip(agents, tasks)})
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return [
            result if not isinstance(result, Exception) else {"error": str(result)}
            for result in results
        ]
    
    async def execute_pipeline(
        self,
        agents: List[BaseAgent],
        task: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute task through a pipeline of agents.
        
        Args:
            agents: Ordered list of agents
            task: Initial task
            
        Returns:
            Final result after pipeline execution
        """
        current_task = task
        for agent in agents:
            result = await agent.execute_task(current_task)
            if not result.get("success", False):
                return result
            current_task = self._prepare_next_task(current_task, result)
        return current_task
    
    def _prepare_next_task(
        self,
        original_task: Dict[str, Any],
        previous_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Prepare task for next agent in pipeline.
        
        Args:
            original_task: Original task
            previous_result: Result from previous agent
            
        Returns:
            Modified task for next agent
        """
        return {
            **original_task,
            "previous_result": previous_result,
            "timestamp": asyncio.get_event_loop().time()
        }
    
    def get_task_status(self, agent_id: UUID) -> Optional[str]:
        """Get status of task for specific agent.
        
        Args:
            agent_id: Agent ID
            
        Returns:
            Task status if found
        """
        task = self._tasks.get(agent_id)
        if not task:
            return None
        if task.done():
            return "completed"
        if task.cancelled():
            return "cancelled"
        return "running"

class MetricsCollector:
    """Collects and analyzes agent performance metrics."""
    
    def __init__(self):
        """Initialize metrics collector."""
        self._metrics: Dict[UUID, List[Dict[str, float]]] = {}
    
    def record_metrics(
        self,
        agent: BaseAgent,
        metrics: Dict[str, float]
    ) -> None:
        """Record new metrics for agent.
        
        Args:
            agent: Agent instance
            metrics: New metrics
        """
        agent_id = agent.profile.agent_id
        if agent_id not in self._metrics:
            self._metrics[agent_id] = []
        self._metrics[agent_id].append(metrics)
    
    def get_agent_metrics(
        self,
        agent: BaseAgent,
        window: Optional[int] = None
    ) -> Dict[str, float]:
        """Get aggregated metrics for agent.
        
        Args:
            agent: Agent instance
            window: Optional window size for recent metrics
            
        Returns:
            Aggregated metrics
        """
        agent_id = agent.profile.agent_id
        metrics_list = self._metrics.get(agent_id, [])
        if not metrics_list:
            return {}
            
        if window:
            metrics_list = metrics_list[-window:]
            
        # Aggregate metrics
        aggregated = {}
        for metric in metrics_list[0].keys():
            values = [m[metric] for m in metrics_list if metric in m]
            if values:
                aggregated[metric] = sum(values) / len(values)
                
        return aggregated
    
    def get_department_metrics(
        self,
        department: Department
    ) -> Dict[str, Dict[str, float]]:
        """Get metrics for all agents in department.
        
        Args:
            department: Department instance
            
        Returns:
            Dictionary of agent metrics
        """
        metrics = {}
        for agent in [department.lead_agent, *department.agents]:
            agent_metrics = self.get_agent_metrics(agent)
            if agent_metrics:
                metrics[agent.profile.agent_id] = agent_metrics
        return metrics
