"""Configuration validation."""
from typing import Dict, Any, List, Optional
from dataclasses import fields

class ValidationError(Exception):
    """Configuration validation error."""
    pass

def validate_range(value: float, min_val: float, max_val: float, name: str) -> None:
    """Validate numeric range.
    
    Args:
        value: Value to validate
        min_val: Minimum allowed value
        max_val: Maximum allowed value
        name: Field name for error message
        
    Raises:
        ValidationError: If validation fails
    """
    if not min_val <= value <= max_val:
        raise ValidationError(
            f"{name} must be between {min_val} and {max_val}, got {value}"
        )

def validate_positive(value: int, name: str) -> None:
    """Validate positive integer.
    
    Args:
        value: Value to validate
        name: Field name for error message
        
    Raises:
        ValidationError: If validation fails
    """
    if value <= 0:
        raise ValidationError(f"{name} must be positive, got {value}")

def validate_department_config(config: Any) -> None:
    """Validate department configuration.
    
    Args:
        config: Department configuration
        
    Raises:
        ValidationError: If validation fails
    """
    validate_range(
        config.evaluation_threshold,
        0.0,
        1.0,
        "evaluation_threshold"
    )
    validate_positive(config.performance_window, "performance_window")
    validate_positive(config.max_concurrent_tasks, "max_concurrent_tasks")
    validate_range(
        config.resource_utilization_threshold,
        0.0,
        1.0,
        "resource_utilization_threshold"
    )
    validate_positive(
        config.metrics_update_interval,
        "metrics_update_interval"
    )
    validate_range(
        config.alert_threshold,
        0.0,
        1.0,
        "alert_threshold"
    )

def validate_agent_config(config: Any) -> None:
    """Validate agent configuration.
    
    Args:
        config: Agent configuration
        
    Raises:
        ValidationError: If validation fails
    """
    validate_positive(config.task_timeout, "task_timeout")
    validate_positive(config.max_retries, "max_retries")
    validate_positive(config.memory_limit, "memory_limit")
    validate_positive(config.min_research_depth, "min_research_depth")
    validate_range(
        config.test_coverage_min,
        0.0,
        1.0,
        "test_coverage_min"
    )
    validate_range(
        config.coverage_threshold,
        0.0,
        1.0,
        "coverage_threshold"
    )
    validate_positive(config.edge_cases_required, "edge_cases_required")

def validate_orchestration_config(config: Any) -> None:
    """Validate orchestration configuration.
    
    Args:
        config: Orchestration configuration
        
    Raises:
        ValidationError: If validation fails
    """
    validate_positive(config.max_workers, "max_workers")
    validate_positive(config.pipeline_timeout, "pipeline_timeout")
    validate_positive(config.retry_delay, "retry_delay")
    validate_positive(config.queue_size, "queue_size")

def validate_metrics_config(config: Any) -> None:
    """Validate metrics configuration.
    
    Args:
        config: Metrics configuration
        
    Raises:
        ValidationError: If validation fails
    """
    validate_positive(config.collection_interval, "collection_interval")
    validate_positive(config.retention_period, "retention_period")
    validate_positive(config.aggregation_window, "aggregation_window")
    
    if not config.storage_path:
        raise ValidationError("storage_path cannot be empty")

def validate_logging_config(config: Any) -> None:
    """Validate logging configuration.
    
    Args:
        config: Logging configuration
        
    Raises:
        ValidationError: If validation fails
    """
    valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
    if config.level not in valid_levels:
        raise ValidationError(
            f"log level must be one of {valid_levels}, got {config.level}"
        )
    
    if not config.file_path:
        raise ValidationError("file_path cannot be empty")
    
    if not config.rotation:
        raise ValidationError("rotation cannot be empty")
    
    if not config.retention:
        raise ValidationError("retention cannot be empty")
