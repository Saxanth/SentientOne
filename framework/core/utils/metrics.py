"""Simple performance metrics collection."""
import time
from typing import Dict, Any
from collections import defaultdict
import threading
from .logging import get_logger

logger = get_logger(__name__)

class MetricsCollector:
    """Simple metrics collector for performance monitoring."""
    
    def __init__(self):
        """Initialize metrics collector."""
        self._metrics = defaultdict(lambda: defaultdict(float))
        self._counters = defaultdict(int)
        self._lock = threading.Lock()
        
    def record_time(self, category: str, operation: str, duration: float) -> None:
        """Record operation duration.
        
        Args:
            category: Metric category
            operation: Operation name
            duration: Duration in seconds
        """
        with self._lock:
            self._metrics[category][operation] = duration
            self._counters[f"{category}.{operation}"] += 1
            
    def increment_counter(self, name: str) -> None:
        """Increment a counter.
        
        Args:
            name: Counter name
        """
        with self._lock:
            self._counters[name] += 1
            
    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics.
        
        Returns:
            Dictionary of metrics
        """
        with self._lock:
            return {
                "metrics": dict(self._metrics),
                "counters": dict(self._counters)
            }
            
class Timer:
    """Context manager for timing operations."""
    
    def __init__(self, collector: MetricsCollector, category: str, operation: str):
        """Initialize timer.
        
        Args:
            collector: Metrics collector
            category: Metric category
            operation: Operation name
        """
        self.collector = collector
        self.category = category
        self.operation = operation
        
    def __enter__(self):
        """Start timer."""
        self.start = time.time()
        return self
        
    def __exit__(self, *args):
        """Stop timer and record duration."""
        duration = time.time() - self.start
        self.collector.record_time(self.category, self.operation, duration)
        
# Global metrics collector instance
metrics = MetricsCollector()
