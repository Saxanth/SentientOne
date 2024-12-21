"""Sentient Resources (SR) department functionality."""
from dataclasses import dataclass
from typing import List, Dict, Optional
from uuid import UUID
from ..core.structure import AgentProfile, Department, Role, Agency

@dataclass
class JobRequirement:
    """Job requirement specification."""
    role: Role
    required_capabilities: List[str]
    minimum_performance_metrics: Dict[str, float]

class SRDepartment:
    """Handles agent recruitment and management."""
    
    def __init__(self, agency: Agency):
        """Initialize SR department.
        
        Args:
            agency: Agency instance
        """
        self.agency = agency
        self.job_requirements: Dict[Role, JobRequirement] = {}
        self._setup_default_requirements()
    
    def _setup_default_requirements(self) -> None:
        """Setup default job requirements."""
        self.job_requirements[Role.RESEARCHER] = JobRequirement(
            role=Role.RESEARCHER,
            required_capabilities=["research", "analysis", "documentation"],
            minimum_performance_metrics={
                "accuracy": 0.8,
                "efficiency": 0.7,
                "cognitive_complexity": 0.75
            }
        )
        
        self.job_requirements[Role.DEVELOPER] = JobRequirement(
            role=Role.DEVELOPER,
            required_capabilities=["coding", "problem_solving", "optimization"],
            minimum_performance_metrics={
                "code_quality": 0.8,
                "task_completion": 0.9,
                "adaptation_rate": 0.85
            }
        )
        
        self.job_requirements[Role.TESTER] = JobRequirement(
            role=Role.TESTER,
            required_capabilities=["testing", "quality_assurance", "documentation"],
            minimum_performance_metrics={
                "test_coverage": 0.9,
                "bug_detection": 0.8,
                "edge_case_identification": 0.85
            }
        )
    
    def evaluate_candidate(self, candidate: AgentProfile, role: Role) -> bool:
        """Evaluate if candidate meets job requirements.
        
        Args:
            candidate: Agent profile
            role: Target role
            
        Returns:
            True if candidate meets requirements
        """
        requirements = self.job_requirements.get(role)
        if not requirements:
            return False
            
        # Check capabilities
        has_capabilities = all(
            cap in candidate.capabilities 
            for cap in requirements.required_capabilities
        )
        if not has_capabilities:
            return False
            
        # Check performance metrics
        for metric, min_value in requirements.minimum_performance_metrics.items():
            if candidate.performance_metrics.get(metric, 0) < min_value:
                return False
                
        return True
    
    def initialize_agent(
        self,
        candidate: AgentProfile,
        department: Department
    ) -> bool:
        """Initialize new agent into department.
        
        Args:
            candidate: Agent profile
            department: Target department
            
        Returns:
            True if initialization successful
        """
        if not self.evaluate_candidate(candidate, candidate.role):
            return False
            
        department.add_agent(candidate)
        return True
    
    def decommission_agent(
        self,
        agent_id: UUID,
        department: Department,
        reason: str
    ) -> Optional[AgentProfile]:
        """Remove agent from department.
        
        Args:
            agent_id: Agent ID
            department: Agent's department
            reason: Reason for decommission
            
        Returns:
            Removed agent profile if found
        """
        return department.remove_agent(agent_id)
    
    def evaluate_performance(
        self,
        agent: AgentProfile,
        new_metrics: Dict[str, float]
    ) -> bool:
        """Evaluate agent's performance against role requirements.
        
        Args:
            agent: Agent profile
            new_metrics: New performance metrics
            
        Returns:
            True if performance meets requirements
        """
        agent.update_metrics(new_metrics)
        return self.evaluate_candidate(agent, agent.role)
    
    def reassign_role(
        self,
        agent: AgentProfile,
        new_role: Role,
        new_department: Department
    ) -> bool:
        """Reassign agent to new role and department.
        
        Args:
            agent: Agent profile
            new_role: New role
            new_department: New department
            
        Returns:
            True if reassignment successful
        """
        if not self.evaluate_candidate(agent, new_role):
            return False
            
        old_department = None
        for dept in self.agency.departments.values():
            if agent in dept.agents:
                old_department = dept
                break
                
        if old_department:
            old_department.remove_agent(agent.agent_id)
            
        agent.role = new_role
        new_department.add_agent(agent)
        return True
