"""Command-line interface for SentientOne framework."""
import click
import asyncio
import json
from typing import Optional
from framework.core.agents.specialized import (
    ResearchAgent,
    ImplementationAgent,
    TestAgent
)
from framework.core.agents._internal.tasks import TaskType, TaskPriority
from framework.core.utils.logging import setup_logging
from framework.core.utils.metrics import metrics

def get_agent_class(agent_type: str):
    """Get agent class by type."""
    return {
        "research": ResearchAgent,
        "implementation": ImplementationAgent,
        "test": TestAgent
    }[agent_type.lower()]

def get_task_type(type_str: str) -> TaskType:
    """Get task type from string."""
    return {
        "research": TaskType.RESEARCH,
        "implement": TaskType.IMPLEMENT,
        "test": TaskType.TEST
    }[type_str.lower()]

def get_priority(priority_str: str) -> TaskPriority:
    """Get priority from string."""
    return {
        "low": TaskPriority.LOW,
        "medium": TaskPriority.MEDIUM,
        "high": TaskPriority.HIGH,
        "critical": TaskPriority.CRITICAL
    }[priority_str.lower()]

@click.group()
def cli():
    """SentientOne CLI tool."""
    pass

@cli.command()
@click.option("--agent-type", type=str, required=True, 
              help="Type of agent (research/implementation/test)")
@click.option("--task-type", type=str, required=True,
              help="Type of task (research/implement/test)")
@click.option("--title", type=str, required=True,
              help="Task title")
@click.option("--description", type=str, default="",
              help="Task description")
@click.option("--priority", type=str, default="medium",
              help="Task priority (low/medium/high/critical)")
@click.option("--log-level", type=str, default="INFO",
              help="Logging level")
@click.option("--log-file", type=str,
              help="Log file path")
async def run_task(
    agent_type: str,
    task_type: str,
    title: str,
    description: str,
    priority: str,
    log_level: str,
    log_file: Optional[str]
):
    """Run a single task with specified agent."""
    # Setup logging
    setup_logging(log_level=log_level, log_file=log_file)
    
    # Create and start agent
    agent_class = get_agent_class(agent_type)
    agent = agent_class()
    await agent.start()
    
    try:
        # Submit and process task
        task_id = await agent.submit_task(
            task_type=get_task_type(task_type),
            title=title,
            description=description,
            priority=get_priority(priority)
        )
        
        result = await agent.process_task(task_id)
        
        # Print result
        if result.success:
            click.echo(f"Task completed successfully: {json.dumps(result.output, indent=2)}")
        else:
            click.echo(f"Task failed: {result.error}", err=True)
            
        # Print metrics
        click.echo("\nMetrics:")
        click.echo(json.dumps(metrics.get_metrics(), indent=2))
        
    finally:
        await agent.stop()

@cli.command()
@click.option("--log-level", type=str, default="INFO",
              help="Logging level")
@click.option("--log-file", type=str,
              help="Log file path")
async def run_workflow(log_level: str, log_file: Optional[str]):
    """Run a complete workflow with multiple agents."""
    # Setup logging
    setup_logging(log_level=log_level, log_file=log_file)
    
    # Create agents
    research_agent = ResearchAgent()
    impl_agent = ImplementationAgent()
    test_agent = TestAgent()
    
    # Start all agents
    await asyncio.gather(
        research_agent.start(),
        impl_agent.start(),
        test_agent.start()
    )
    
    try:
        # Run workflow
        # 1. Research
        research_task = await research_agent.submit_task(
            task_type=TaskType.RESEARCH,
            title="Research Task",
            priority=TaskPriority.HIGH
        )
        research_result = await research_agent.process_task(research_task)
        
        if not research_result.success:
            raise click.ClickException(f"Research failed: {research_result.error}")
            
        # 2. Implementation
        impl_task = await impl_agent.submit_task(
            task_type=TaskType.IMPLEMENT,
            title="Implementation Task",
            priority=TaskPriority.HIGH
        )
        impl_result = await impl_agent.process_task(impl_task)
        
        if not impl_result.success:
            raise click.ClickException(f"Implementation failed: {impl_result.error}")
            
        # 3. Testing
        test_task = await test_agent.submit_task(
            task_type=TaskType.TEST,
            title="Test Task",
            priority=TaskPriority.HIGH
        )
        test_result = await test_agent.process_task(test_task)
        
        if not test_result.success:
            raise click.ClickException(f"Testing failed: {test_result.error}")
            
        # Print results
        click.echo("Workflow completed successfully!")
        click.echo("\nMetrics:")
        click.echo(json.dumps(metrics.get_metrics(), indent=2))
        
    finally:
        # Stop all agents
        await asyncio.gather(
            research_agent.stop(),
            impl_agent.stop(),
            test_agent.stop()
        )

def main():
    """CLI entry point."""
    cli(_anyio_backend="asyncio")
