"""Tester agent implementation."""
from typing import Dict, Any, Optional
from ..base.agent import BaseAgent
from ..core.structure import AgentProfile, Role

class TesterAgent(BaseAgent):
    """Agent specialized in testing and quality assurance."""
    
    async def _process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process testing task.
        
        Args:
            task: Task specification with:
                - code: Code to test
                - requirements: Test requirements
                - test_type: Type of testing
                - context: Additional context
            
        Returns:
            Testing results
        """
        if not self.provider:
            return {
                "success": False,
                "error": "No language model provider configured"
            }
            
        # Construct testing prompt
        prompt = self._construct_testing_prompt(task)
        
        # Generate tests using provider
        response = await self.provider.generate(
            prompt=prompt,
            task_type="test",
            system="You are a testing specialist focused on comprehensive test coverage and edge case detection."
        )
        
        if not response.success:
            return {
                "success": False,
                "error": response.error or "Test generation failed"
            }
            
        return {
            "success": True,
            "tests": response.content,
            "metadata": response.metadata
        }
    
    def _construct_testing_prompt(self, task: Dict[str, Any]) -> str:
        """Construct testing prompt from task.
        
        Args:
            task: Task specification
            
        Returns:
            Formatted prompt
        """
        code = task.get("code", "")
        requirements = task.get("requirements", [])
        test_type = task.get("test_type", "unit")
        context = task.get("context", "")
        
        prompt_parts = [
            f"Code to Test:\n{code}",
            f"Test Type: {test_type}",
            f"Context: {context}" if context else "",
            "Requirements:",
            *[f"- {req}" for req in requirements],
            "\nPlease provide:",
            "1. Comprehensive test cases",
            "2. Edge cases and error scenarios",
            "3. Test coverage analysis",
            "4. Potential improvements"
        ]
        
        return "\n".join(filter(None, prompt_parts))
    
    def get_performance_metrics(self) -> Dict[str, float]:
        """Get testing-specific performance metrics.
        
        Returns:
            Performance metrics
        """
        base_metrics = super().get_performance_metrics()
        
        # Add testing-specific metrics
        if self.task_history:
            comprehensive_tests = sum(
                1 for task in self.task_history
                if task["result"].get("success", False) and
                task["result"].get("tests")  # Has generated tests
            )
            base_metrics["test_coverage"] = comprehensive_tests / len(self.task_history)
            
        return base_metrics
