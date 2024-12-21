"""Agency configuration management."""
from typing import Dict, Any, Optional
import os
import yaml
from dataclasses import dataclass, field
from pathlib import Path
from .validation import (
    ValidationError,
    validate_department_config,
    validate_agent_config,
    validate_orchestration_config,
    validate_metrics_config,
    validate_logging_config
)

@dataclass
class DepartmentConfig:
    """Department-specific configuration."""
    evaluation_threshold: float = 0.8
    performance_window: int = 10
    max_concurrent_tasks: int = 5
    code_review_required: bool = True
    task_priority_levels: list = field(default_factory=lambda: ["low", "medium", "high", "critical"])
    resource_utilization_threshold: float = 0.8
    metrics_update_interval: int = 300
    alert_threshold: float = 0.7

    def __post_init__(self):
        """Validate configuration after initialization."""
        validate_department_config(self)

@dataclass
class AgentConfig:
    """Agent-specific configuration."""
    task_timeout: int = 300
    max_retries: int = 3
    memory_limit: int = 512
    min_research_depth: int = 3
    citation_required: bool = True
    code_style: str = "pep8"
    test_coverage_min: float = 0.8
    coverage_threshold: float = 0.9
    edge_cases_required: int = 5

    def __post_init__(self):
        """Validate configuration after initialization."""
        validate_agent_config(self)

@dataclass
class OrchestrationConfig:
    """Task orchestration configuration."""
    max_workers: int = 5
    pipeline_timeout: int = 600
    retry_delay: int = 5
    queue_size: int = 100

    def __post_init__(self):
        """Validate configuration after initialization."""
        validate_orchestration_config(self)

@dataclass
class MetricsConfig:
    """Metrics collection configuration."""
    collection_interval: int = 60
    retention_period: int = 604800
    aggregation_window: int = 3600
    storage_path: str = "metrics/"

    def __post_init__(self):
        """Validate configuration after initialization."""
        validate_metrics_config(self)

@dataclass
class LoggingConfig:
    """Logging configuration."""
    level: str = "INFO"
    file_path: str = "logs/agency.log"
    rotation: str = "1 day"
    retention: str = "30 days"

    def __post_init__(self):
        """Validate configuration after initialization."""
        validate_logging_config(self)

@dataclass
class SecurityConfig:
    """Security configuration."""
    task_validation: bool = True
    agent_isolation: bool = True
    permission_checks: bool = True

class AgencyConfig:
    """Agency configuration manager."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration manager.
        
        Args:
            config_path: Optional path to config file
        """
        self.config_path = config_path or self._get_default_config_path()
        self._load_config()
        
    def _get_default_config_path(self) -> str:
        """Get default configuration path.
        
        Returns:
            Path to default config file
        """
        return str(Path(__file__).parent.parent / "config.yaml")
        
    def _load_config(self) -> None:
        """Load and validate configuration from file."""
        try:
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f)
            
            agency_config = config.get('agency', {})
            
            # Initialize and validate configurations
            try:
                self.departments = {
                    dept: DepartmentConfig(**cfg)
                    for dept, cfg in agency_config.get('departments', {}).items()
                }
                
                agent_cfg = agency_config.get('agents', {})
                self.base_agent = AgentConfig(**agent_cfg.get('base', {}))
                self.specialized_agents = {
                    role: AgentConfig(**cfg)
                    for role, cfg in agent_cfg.get('specialized', {}).items()
                }
                
                self.orchestration = OrchestrationConfig(
                    **agency_config.get('orchestration', {})
                )
                self.metrics = MetricsConfig(**agency_config.get('metrics', {}))
                self.logging = LoggingConfig(**agency_config.get('logging', {}))
                self.security = SecurityConfig(**agency_config.get('security', {}))
                
            except ValidationError as e:
                print(f"Configuration validation failed: {e}")
                self._use_defaults()
                
        except Exception as e:
            print(f"Error loading config: {e}")
            self._use_defaults()
    
    def _use_defaults(self) -> None:
        """Use default configurations."""
        self.departments = {
            'sr': DepartmentConfig(),
            'engineering': DepartmentConfig(),
            'operations': DepartmentConfig(),
            'analytics': DepartmentConfig()
        }
        self.base_agent = AgentConfig()
        self.specialized_agents = {
            'researcher': AgentConfig(),
            'developer': AgentConfig(),
            'tester': AgentConfig()
        }
        self.orchestration = OrchestrationConfig()
        self.metrics = MetricsConfig()
        self.logging = LoggingConfig()
        self.security = SecurityConfig()
    
    def get_department_config(self, department: str) -> DepartmentConfig:
        """Get configuration for department.
        
        Args:
            department: Department name
            
        Returns:
            Department configuration
        """
        return self.departments.get(department, DepartmentConfig())
    
    def get_agent_config(self, role: str) -> AgentConfig:
        """Get configuration for agent role.
        
        Args:
            role: Agent role
            
        Returns:
            Agent configuration
        """
        return self.specialized_agents.get(role, self.base_agent)
    
    def update_config(self, section: str, key: str, value: Any) -> None:
        """Update and validate configuration value.
        
        Args:
            section: Configuration section
            key: Configuration key
            value: New value
            
        Raises:
            ValidationError: If new value is invalid
        """
        if hasattr(self, section):
            section_config = getattr(self, section)
            if isinstance(section_config, dict):
                if key in section_config:
                    # Create new instance with updated value for validation
                    config_class = type(section_config[key])
                    current_values = vars(section_config[key])
                    current_values[key] = value
                    # Validation happens in __post_init__
                    section_config[key] = config_class(**current_values)
            else:
                current_values = vars(section_config)
                current_values[key] = value
                # Create new instance with updated value for validation
                config_class = type(section_config)
                setattr(self, section, config_class(**current_values))
    
    def save_config(self) -> None:
        """Save current configuration to file."""
        config = {
            'agency': {
                'departments': {
                    name: vars(cfg)
                    for name, cfg in self.departments.items()
                },
                'agents': {
                    'base': vars(self.base_agent),
                    'specialized': {
                        role: vars(cfg)
                        for role, cfg in self.specialized_agents.items()
                    }
                },
                'orchestration': vars(self.orchestration),
                'metrics': vars(self.metrics),
                'logging': vars(self.logging),
                'security': vars(self.security)
            }
        }
        
        try:
            with open(self.config_path, 'r') as f:
                existing_config = yaml.safe_load(f)
            
            # Preserve non-agency configurations
            existing_config['agency'] = config['agency']
            
            with open(self.config_path, 'w') as f:
                yaml.safe_dump(existing_config, f, default_flow_style=False)
                
        except Exception as e:
            print(f"Error saving config: {e}")

# Global configuration instance
config = AgencyConfig()
