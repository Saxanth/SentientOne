"""Executive team functionality."""
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from uuid import UUID
from enum import Enum, auto
from ..core.structure import AgentProfile, Department, Role, Agency

class ProjectPriority(Enum):
    """Project priority levels."""
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()
    CRITICAL = auto()

@dataclass
class Project:
    """Project specification."""
    name: str
    priority: ProjectPriority
    required_roles: Dict[Role, int]  # Role -> Count needed
    assigned_agents: List[UUID] = field(default_factory=list)
    completion_percentage: float = 0.0

class ExecutiveTeam:
    """Handles high-level decision making."""
    
    def __init__(self, agency: Agency):
        """Initialize executive team.
        
        Args:
            agency: Agency instance
        """
        self.agency = agency
        self.active_projects: List[Project] = []
        self.resource_utilization: Dict[UUID, float] = {}  # Agent ID -> Utilization
    
    def allocate_resources(self, project: Project) -> bool:
        """Allocate agents to project based on requirements.
        
        Args:
            project: Project specification
            
        Returns:
            True if allocation successful
        """
        # Check each required role
        for role, count in project.required_roles.items():
            allocated = 0
            department = self._get_department_for_role(role)
            if not department:
                continue
                
            # Find available agents
            for agent in department.agents:
                if (
                    agent.role == role and
                    self.resource_utilization.get(agent.agent_id, 0) < 0.8 and  # 80% max utilization
                    allocated < count
                ):
                    project.assigned_agents.append(agent.agent_id)
                    self.resource_utilization[agent.agent_id] = self.resource_utilization.get(agent.agent_id, 0) + 0.2
                    allocated += 1
                    
            if allocated < count:
                # Couldn't allocate enough agents
                return False
                
        return True
    
    def start_project(self, project: Project) -> bool:
        """Start new project if resources available.
        
        Args:
            project: Project specification
            
        Returns:
            True if project started
        """
        if self.allocate_resources(project):
            self.active_projects.append(project)
            return True
        return False
    
    def update_project_status(self, project: Project, completion: float) -> None:
        """Update project completion status.
        
        Args:
            project: Project
            completion: New completion percentage
        """
        project.completion_percentage = completion
        if completion >= 100:
            self._complete_project(project)
    
    def _complete_project(self, project: Project) -> None:
        """Handle project completion.
        
        Args:
            project: Completed project
        """
        # Free up resources
        for agent_id in project.assigned_agents:
            if agent_id in self.resource_utilization:
                self.resource_utilization[agent_id] = max(
                    0,
                    self.resource_utilization[agent_id] - 0.2
                )
        
        # Remove from active projects
        if project in self.active_projects:
            self.active_projects.remove(project)
    
    def _get_department_for_role(self, role: Role) -> Optional[Department]:
        """Get appropriate department for role.
        
        Args:
            role: Agent role
            
        Returns:
            Matching department if found
        """
        role_department_map = {
            # SR Department
            Role.SR_MANAGER: Department.SR,
            Role.SR_RECRUITER: Department.SR,
            Role.SR_PERFORMANCE_ANALYST: Department.SR,
            # Engineering Department
            Role.RESEARCHER: Department.ENGINEERING,
            Role.DEVELOPER: Department.ENGINEERING,
            Role.TESTER: Department.ENGINEERING,
            # Operations Department
            Role.PROJECT_MANAGER: Department.OPERATIONS,
            Role.RESOURCE_MANAGER: Department.OPERATIONS,
            # Analytics Department
            Role.PERFORMANCE_MONITOR: Department.ANALYTICS,
            Role.RISK_ANALYST: Department.ANALYTICS
        }
        
        dept_type = role_department_map.get(role)
        if dept_type:
            return self.agency.get_department(dept_type)
        return None
    
    def generate_resource_report(self) -> Dict[str, any]:
        """Generate resource utilization report.
        
        Returns:
            Report dictionary
        """
        return {
            "active_projects": len(self.active_projects),
            "resource_utilization": self.resource_utilization,
            "department_stats": self._get_department_stats()
        }
    
    def _get_department_stats(self) -> Dict[str, Dict[str, int]]:
        """Get department statistics.
        
        Returns:
            Department statistics
        """
        stats = {}
        for dept_type, department in self.agency.departments.items():
            stats[dept_type.name] = {
                "total_agents": len(department.agents),
                "active_agents": sum(
                    1 for agent in department.agents
                    if self.resource_utilization.get(agent.agent_id, 0) > 0
                )
            }
        return stats
