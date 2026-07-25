"""
Real-Time Telemetry Stream Gateway for Eco-Loop Building Agents.

Architected as a hardware-agnostic pub/sub streaming interface layer between
building sensors (BACnet / IoT Gateway digital twin) and the LLM Decision Agent.
"""
import time
import queue
import logging
from typing import Dict, Any, Optional, Callable
from schemas import SensorTelemetryPayload, ActionDecisionPayload

logger = logging.getLogger(__name__)

class TelemetryStreamGateway:
    """
    Decoupled Pub/Sub Stream Manager for Sensor Telemetry and Actuator Commands.
    """
    def __init__(self, maxsize: int = 100):
        self.sensor_channel: queue.Queue = queue.Queue(maxsize=maxsize)
        self.action_channel: queue.Queue = queue.Queue(maxsize=maxsize)
        self.latency_log: list = []
        self.is_connected: bool = True
        logger.info("TelemetryStreamGateway initialized (BACnet/IoT Gateway Mock Interface Active).")

    def publish_telemetry(self, payload: SensorTelemetryPayload) -> bool:
        """
        Sensor Publisher: Pushes telemetry payload onto sensor channel.
        """
        try:
            t0 = time.perf_counter()
            self.sensor_channel.put_nowait(payload.to_dict())
            latency_ms = (time.perf_counter() - t0) * 1000.0
            self.latency_log.append(latency_ms)
            return True
        except queue.Full:
            logger.warning("Sensor channel queue full! Telemetry message dropped.")
            return False

    def subscribe_telemetry(self, timeout: float = 0.5) -> Optional[Dict[str, Any]]:
        """
        Agent Subscriber: Consumes next telemetry payload from sensor channel.
        """
        try:
            return self.sensor_channel.get(block=True, timeout=timeout)
        except queue.Empty:
            return None

    def publish_action(self, payload: ActionDecisionPayload) -> bool:
        """
        Agent Publisher: Pushes decision payload onto action channel.
        """
        try:
            self.action_channel.put_nowait(payload.to_dict())
            return True
        except queue.Full:
            logger.warning("Action channel queue full!")
            return False

    def subscribe_action(self, timeout: float = 0.5) -> Optional[Dict[str, Any]]:
        """
        Actuator Consumer: Consumes next action decision from action channel.
        """
        try:
            return self.action_channel.get(block=True, timeout=timeout)
        except queue.Empty:
            return None

    def get_avg_latency_ms(self) -> float:
        if not self.latency_log:
            return 0.05
        return sum(self.latency_log) / len(self.latency_log)

# Global Singleton Instance
gateway = TelemetryStreamGateway()
