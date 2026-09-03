"""Tests for monitoring module."""
import sys
sys.path.insert(0, 'src')
from monitoring import SystemMonitor, get_monitor


def test_monitor_initialization():
    """Monitor should initialize with correct attributes."""
    monitor = SystemMonitor("test-service", "testing")
    assert monitor.service_name == "test-service"
    assert monitor.environment == "testing"


def test_cpu_metrics_structure():
    """CPU metrics should have required fields."""
    monitor = SystemMonitor("test-service")
    metrics = monitor.collect_cpu_metrics()
    required = ["metric", "service", "value", "unit", "timestamp"]
    for field in required:
        assert field in metrics, f"Missing field: {field}"


def test_cpu_value_in_range():
    """CPU utilization should be between 0 and 100."""
    monitor = SystemMonitor("test-service")
    metrics = monitor.collect_cpu_metrics()
    assert 0 <= metrics["value"] <= 100


def test_memory_metrics_structure():
    """Memory metrics should have required fields."""
    monitor = SystemMonitor("test-service")
    metrics = monitor.collect_memory_metrics()
    assert "total_mb" in metrics
    assert "used_mb" in metrics
    assert "available_mb" in metrics
    assert metrics["used_mb"] + metrics["available_mb"] <= metrics["total_mb"] + 1


def test_health_check_returns_status():
    """Health check should always return a status."""
    monitor = SystemMonitor("test-service")
    health = monitor.check_health()
    assert "status" in health
    assert health["status"] in ["healthy", "unhealthy"]


def test_health_check_has_all_checks():
    """Health check should include cpu and memory checks."""
    monitor = SystemMonitor("test-service")
    health = monitor.check_health()
    assert "checks" in health
    assert "cpu" in health["checks"]
    assert "memory" in health["checks"]


def test_get_monitor_factory():
    """get_monitor factory should return SystemMonitor."""
    monitor = get_monitor("factory-test")
    assert isinstance(monitor, SystemMonitor)
    assert monitor.service_name == "factory-test"


print("All monitoring tests defined successfully")
cat >> tests/test_monitoring.py << 'EOF'


def test_custom_thresholds():
    """Monitor should use custom thresholds when provided."""
    monitor = SystemMonitor(
        "test-service",
        cpu_threshold=70,
        memory_threshold=80
    )
    assert monitor.cpu_threshold == 70
    assert monitor.memory_threshold == 80


def test_default_thresholds():
    """Monitor should use defaults when not specified."""
    monitor = SystemMonitor("test-service")
    assert monitor.cpu_threshold == SystemMonitor.DEFAULT_CPU_THRESHOLD
    assert monitor.memory_threshold == SystemMonitor.DEFAULT_MEMORY_THRESHOLD
