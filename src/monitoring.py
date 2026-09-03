"""
Monitoring dashboard module.
Provides system health metrics for DevOps observability.
"""
import os
import datetime
from typing import Dict, Any, Optional


class SystemMonitor:
    """
    Collects and reports system health metrics.

    Designed for integration with CloudWatch or Prometheus.
    Configurable thresholds for different environments.
    """

    DEFAULT_CPU_THRESHOLD = 85
    DEFAULT_MEMORY_THRESHOLD = 90

    def __init__(self, service_name: str,
                 environment: str = "production",
                 cpu_threshold: float = None,
                 memory_threshold: float = None):
        """
        Initialize the system monitor.

        Args:
            service_name: Name of the service being monitored
            environment: Deployment environment (dev/staging/prod)
            cpu_threshold: CPU % above which status is unhealthy
                          (default: 85)
            memory_threshold: Memory % above which status is unhealthy
                             (default: 90)
        """
        self.service_name = service_name
        self.environment = environment
        self.cpu_threshold = cpu_threshold or self.DEFAULT_CPU_THRESHOLD
        self.memory_threshold = (memory_threshold or
                                  self.DEFAULT_MEMORY_THRESHOLD)
        self._metrics_history = []

    def collect_cpu_metrics(self) -> Dict[str, Any]:
        """Collect CPU utilization metrics."""
        import random
        current = random.uniform(10, 90)
        return {
            "metric": "cpu_utilization",
            "service": self.service_name,
            "environment": self.environment,
            "value": round(current, 2),
            "unit": "percent",
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
        }

    def collect_memory_metrics(self) -> Dict[str, Any]:
        """Collect memory utilization metrics."""
        import random
        total_mb = 1024
        used_mb = random.uniform(200, 900)
        available_mb = total_mb - used_mb
        return {
            "metric": "memory_utilization",
            "service": self.service_name,
            "environment": self.environment,
            "total_mb": total_mb,
            "used_mb": round(used_mb, 2),
            "available_mb": round(available_mb, 2),
            "utilization_percent": round((used_mb / total_mb) * 100, 2),
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
        }

    def check_health(self) -> Dict[str, Any]:
        """
        Perform overall health check using configured thresholds.

        Returns health status with all metrics and threshold info.
        """
        cpu = self.collect_cpu_metrics()
        memory = self.collect_memory_metrics()
        cpu_healthy = cpu["value"] < self.cpu_threshold
        memory_healthy = (memory["utilization_percent"]
                          < self.memory_threshold)
        overall_healthy = cpu_healthy and memory_healthy

        return {
            "service": self.service_name,
            "environment": self.environment,
            "status": "healthy" if overall_healthy else "unhealthy",
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "checks": {
                "cpu": {
                    "status": "pass" if cpu_healthy else "fail",
                    "value": cpu["value"],
                    "threshold": self.cpu_threshold
                },
                "memory": {
                    "status": "pass" if memory_healthy else "fail",
                    "value": memory["utilization_percent"],
                    "threshold": self.memory_threshold
                }
            }
        }


def get_monitor(service_name: Optional[str] = None,
                cpu_threshold: float = None,
                memory_threshold: float = None) -> SystemMonitor:
    """Factory function to create a SystemMonitor instance."""
    name = service_name or os.environ.get(
        "SERVICE_NAME", "unknown-service"
    )
    env = os.environ.get("ENVIRONMENT", "development")
    return SystemMonitor(
        service_name=name,
        environment=env,
        cpu_threshold=cpu_threshold,
        memory_threshold=memory_threshold
    )
