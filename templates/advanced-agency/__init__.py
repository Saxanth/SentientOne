"""SentientOne Agency Framework.

This framework provides a comprehensive structure for managing AI agents in an
organizational context, with specialized roles, departments, and task management.
"""

from .core import (
    Department, Role, AgentProfile, Agency,
    AgentFactory, TaskOrchestrator, MetricsCollector
)
from .specialized import (
    ResearchAgent, DeveloperAgent, TesterAgent,
    ExecutiveTeam, Project, ProjectPriority,
    SRDepartment, JobRequirement
)
from .base import BaseAgent
from .config import AgencyConfig, config, ValidationError

__version__ = '0.1.0'

__all__ = [
    # Core Structure
    'Department',
    'Role',
    'AgentProfile',
    'Agency',
    
    # Specialized Agents & Departments
    'ResearchAgent',
    'DeveloperAgent',
    'TesterAgent',
    'ExecutiveTeam',
    'SRDepartment',
    
    # Project Management
    'Project',
    'ProjectPriority',
    'JobRequirement',
    
    # Base Components
    'BaseAgent',
    
    # Utilities
    'AgentFactory',
    'TaskOrchestrator',
    'MetricsCollector',
    
    # Configuration
    'AgencyConfig',
    'config',
    'ValidationError',
]
