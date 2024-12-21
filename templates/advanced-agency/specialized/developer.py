"""Developer agent implementation."""
from typing import Dict, Any, Optional
from ..base.agent import BaseAgent
from ..core.structure import AgentProfile, Role

class DeveloperAgent(BaseAgent):
    """Agent specialized in code implementation."""
    
    async def _process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process development task.
        
        Args:
            task: Task specification with:
                - description: Task description
                - requirements: Code requirements
                - language: Programming language
                - context: Additional context
            
        Returns:
            Implementation results
        """
        if not self.provider:
            return {
                "success": False,
                "error": "No language model provider configured"
            }
            
        # Construct implementation prompt
        prompt = self._construct_implementation_prompt(task)
        
        # Generate implementation using provider
        response = await self.provider.generate(
            prompt=prompt,
            task_type="implementation",
            system="You are a software developer focused on writing clean, efficient, and well-documented code."
        )
        
        if not response.success:
            return {
                "success": False,
                "error": response.error or "Code generation failed"
            }
            
        return {
            "success": True,
            "code": response.content,
            "metadata": response.metadata
        }
    
    def _construct_implementation_prompt(self, task: Dict[str, Any]) -> str:
        """Construct implementation prompt from task.
        
        Args:
            task: Task specification
            
        Returns:
            Formatted prompt
        """
        description = task.get("description", "")
        requirements = task.get("requirements", [])
        language = task.get("language", "python")
        context = task.get("context", "")
        
        prompt_parts = [
            f"Task Description: {description}",
            f"Programming Language: {language}",
            f"Context: {context}" if context else "",
            "Requirements:",
            *[f"- {req}" for req in requirements],
            "\nPlease provide:",
            "1. Complete implementation",
            "2. Brief explanation of the approach",
            "3. Any important considerations or limitations"
        ]
        
        return "\n".join(filter(None, prompt_parts))
    
    def get_performance_metrics(self) -> Dict[str, float]:
        """Get development-specific performance metrics.
        
        Returns:
            Performance metrics
        """
        base_metrics = super().get_performance_metrics()
        
        # Add development-specific metrics
        if self.task_history:
            successful_implementations = sum(
                1 for task in self.task_history
                if task["result"].get("success", False) and
                task["result"].get("code")  # Has generated code
            )
            base_metrics["code_quality"] = successful_implementations / len(self.task_history)
            
        return base_metrics
