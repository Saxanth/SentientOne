"""Tests for specialized agents."""
import pytest
from framework.core.agents.specialized import (
    ResearchAgent,
    ImplementationAgent,
    TestAgent
)
from framework.core.agents._internal.tasks import (
    TaskType,
    TaskPriority,
    TaskStatus
)

@pytest.mark.asyncio
async def test_research_agent():
    """Test research agent functionality."""
    agent = ResearchAgent()
    await agent.start()
    
    # Submit task
    task_id = await agent.submit_task(
        task_type=TaskType.RESEARCH,
        title="Test Research",
        priority=TaskPriority.MEDIUM
    )
    
    # Check task status
    status = await agent.get_task_status(task_id)
    assert status == TaskStatus.PENDING
    
    # Process task
    result = await agent.process_task(task_id)
    assert result.success
    
    # Check final status
    status = await agent.get_task_status(task_id)
    assert status == TaskStatus.COMPLETED
    
    await agent.stop()

@pytest.mark.asyncio
async def test_implementation_agent():
    """Test implementation agent functionality."""
    agent = ImplementationAgent()
    await agent.start()
    
    # Submit task
    task_id = await agent.submit_task(
        task_type=TaskType.IMPLEMENT,
        title="Test Implementation",
        priority=TaskPriority.HIGH
    )
    
    # Check task status
    status = await agent.get_task_status(task_id)
    assert status == TaskStatus.PENDING
    
    # Process task
    result = await agent.process_task(task_id)
    assert result.success
    
    # Check final status
    status = await agent.get_task_status(task_id)
    assert status == TaskStatus.COMPLETED
    
    await agent.stop()

@pytest.mark.asyncio
async def test_test_agent():
    """Test test agent functionality."""
    agent = TestAgent()
    await agent.start()
    
    # Submit task
    task_id = await agent.submit_task(
        task_type=TaskType.TEST,
        title="Run Tests",
        priority=TaskPriority.HIGH
    )
    
    # Check task status
    status = await agent.get_task_status(task_id)
    assert status == TaskStatus.PENDING
    
    # Process task
    result = await agent.process_task(task_id)
    assert result.success
    
    # Check final status
    status = await agent.get_task_status(task_id)
    assert status == TaskStatus.COMPLETED
    
    await agent.stop()

@pytest.mark.asyncio
async def test_agent_capabilities():
    """Test agent capabilities."""
    research_agent = ResearchAgent()
    impl_agent = ImplementationAgent()
    test_agent = TestAgent()
    
    # Check research agent capabilities
    caps = research_agent.get_capabilities()
    assert TaskType.RESEARCH in caps["supported_tasks"]
    assert caps["specialization"] == "research"
    
    # Check implementation agent capabilities
    caps = impl_agent.get_capabilities()
    assert TaskType.IMPLEMENT in caps["supported_tasks"]
    assert caps["specialization"] == "implementation"
    
    # Check test agent capabilities
    caps = test_agent.get_capabilities()
    assert TaskType.TEST in caps["supported_tasks"]
    assert caps["specialization"] == "testing"
