"""Agency organizational structure."""
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum, auto
from uuid import UUID, uuid4

class Department(Enum):
    """Agency departments."""
    EXECUTIVE = auto()
    SR = auto()  # Sentient Resources
    ENGINEERING = auto()
    OPERATIONS = auto()
    ANALYTICS = auto()

class Role(Enum):
    """Agent roles."""
    # Executive
    CEO = auto()
    CTO = auto()
    CFO = auto()
    
    # Sentient Resources
    SR_MANAGER = auto()
    SR_RECRUITER = auto()
    SR_PERFORMANCE_ANALYST = auto()
    
    # Engineering
    RESEARCH_LEAD = auto()
    IMPLEMENTATION_LEAD = auto()
    QA_LEAD = auto()
    RESEARCHER = auto()
    DEVELOPER = auto()
    TESTER = auto()
    
    # Operations
    PROJECT_MANAGER = auto()
    RESOURCE_MANAGER = auto()
    
    # Analytics
    PERFORMANCE_MONITOR = auto()
    RISK_ANALYST = auto()

@dataclass
class AgentProfile:
    """Agent profile containing capabilities and performance metrics."""
    agent_id: UUID = field(default_factory=uuid4)
    name: str
    role: Role
    capabilities: List[str]
    performance_metrics: Dict[str, float] = field(default_factory=dict)
    supervisor_id: Optional[UUID] = None
    
    def update_metrics(self, metrics: Dict[str, float]) -> None:
        """Update agent's performance metrics."""
        self.performance_metrics.update(metrics)

@dataclass
class Department:
    """Department containing groups of agents."""
    name: str
    department_type: Department
    lead_agent: AgentProfile
    agents: List[AgentProfile] = field(default_factory=list)
    
    def add_agent(self, agent: AgentProfile) -> None:
        """Add agent to department."""
        agent.supervisor_id = self.lead_agent.agent_id
        self.agents.append(agent)
        
    def remove_agent(self, agent_id: UUID) -> Optional[AgentProfile]:
        """Remove agent from department."""
        for i, agent in enumerate(self.agents):
            if agent.agent_id == agent_id:
                return self.agents.pop(i)
        return None

@dataclass
class Agency:
    """Main agency structure."""
    departments: Dict[Department, Department] = field(default_factory=dict)
    executive_team: List[AgentProfile] = field(default_factory=list)
    
    def add_department(self, department: Department) -> None:
        """Add department to agency."""
        self.departments[department.department_type] = department
    
    def add_executive(self, agent: AgentProfile) -> None:
        """Add executive to agency."""
        if agent.role in [Role.CEO, Role.CTO, Role.CFO]:
            self.executive_team.append(agent)
    
    def get_department(self, dept_type: Department) -> Optional[Department]:
        """Get department by type."""
        return self.departments.get(dept_type)
    
    def get_agent_chain_of_command(self, agent_id: UUID) -> List[AgentProfile]:
        """Get agent's chain of command up to executive level."""
        chain = []
        current_agent = self._find_agent(agent_id)
        
        while current_agent:
            chain.append(current_agent)
            if not current_agent.supervisor_id:
                break
            current_agent = self._find_agent(current_agent.supervisor_id)
            
        return chain
    
    def _find_agent(self, agent_id: UUID) -> Optional[AgentProfile]:
        """Find agent by ID."""
        # Check executive team
        for exec_agent in self.executive_team:
            if exec_agent.agent_id == agent_id:
                return exec_agent
        
        # Check departments
        for department in self.departments.values():
            if department.lead_agent.agent_id == agent_id:
                return department.lead_agent
            for agent in department.agents:
                if agent.agent_id == agent_id:
                    return agent
        
        return None
