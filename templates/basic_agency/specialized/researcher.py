"""Research agent implementation."""
from typing import Dict, Any, Optional
from ..base.agent import BaseAgent
from ..core.structure import AgentProfile, Role

class ResearchAgent(BaseAgent):
    """Agent specialized in research tasks."""
    
    async def _process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process research task.
        
        Args:
            task: Task specification with:
                - query: Research query
                - context: Additional context
                - requirements: Specific requirements
            
        Returns:
            Research results
        """
        if not self.provider:
            return {
                "success": False,
                "error": "No language model provider configured"
            }
            
        # Construct research prompt
        prompt = self._construct_research_prompt(task)
        
        # Generate research using provider
        response = await self.provider.generate(
            prompt=prompt,
            task_type="research",
            system="You are a research specialist focused on thorough analysis and accurate information gathering."
        )
        
        if not response.success:
            return {
                "success": False,
                "error": response.error or "Research generation failed"
            }
            
        return {
            "success": True,
            "findings": response.content,
            "metadata": response.metadata
        }
    
    def _construct_research_prompt(self, task: Dict[str, Any]) -> str:
        """Construct research prompt from task.
        
        Args:
            task: Task specification
            
        Returns:
            Formatted prompt
        """
        query = task.get("query", "")
        context = task.get("context", "")
        requirements = task.get("requirements", [])
        
        prompt_parts = [
            f"Research Query: {query}",
            f"Context: {context}" if context else "",
            "Requirements:",
            *[f"- {req}" for req in requirements],
            "\nPlease provide:",
            "1. Key findings",
            "2. Supporting evidence",
            "3. Potential implications",
            "4. Areas for further investigation"
        ]
        
        return "\n".join(filter(None, prompt_parts))
    
    def get_performance_metrics(self) -> Dict[str, float]:
        """Get research-specific performance metrics.
        
        Returns:
            Performance metrics
        """
        base_metrics = super().get_performance_metrics()
        
        # Add research-specific metrics
        if self.task_history:
            accurate_findings = sum(
                1 for task in self.task_history
                if task["result"].get("success", False) and
                len(task["result"].get("findings", "").split()) > 100  # Basic length check
            )
            base_metrics["accuracy"] = accurate_findings / len(self.task_history)
            
        return base_metrics
