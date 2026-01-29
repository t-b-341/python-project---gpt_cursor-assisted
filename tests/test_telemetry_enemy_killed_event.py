"""Tests for telemetry EventBus integration: enemy_killed -> ScoreEvent."""
from __future__ import annotations

from dataclasses import dataclass

import pytest

from event_bus import EventBus, GameEvent
from telemetry.event_bus_handlers import register_telemetry_event_handlers
from telemetry.events import ScoreEvent


@dataclass
class FakeConfig:
    enable_telemetry: bool = True


class FakeTelemetryClient:
    def __init__(self):
        self.logged: list[ScoreEvent] = []

    def log_score(self, e: ScoreEvent) -> None:
        self.logged.append(e)


class FakeCtx:
    def __init__(self, enable_telemetry: bool, client):
        self.config = FakeConfig(enable_telemetry=enable_telemetry)
        self.telemetry_client = client


class FakeGameState:
    def __init__(self, score: int, run_time: float):
        self.score = score
        self.run_time = run_time


def test_enemy_killed_event_logs_score_event_when_telemetry_enabled():
    bus = EventBus()
    client = FakeTelemetryClient()
    ctx = FakeCtx(enable_telemetry=True, client=client)
    gs = FakeGameState(score=1234, run_time=12.5)

    register_telemetry_event_handlers(bus, ctx, gs)

    ev = GameEvent(
        type="enemy_killed",
        payload={"enemy_type": "grunt", "wave_number": 3, "score_delta": 50},
    )
    bus.publish(ev)

    assert len(client.logged) == 1
    se = client.logged[0]
    assert isinstance(se, ScoreEvent)
    assert se.score == 1234
    assert se.score_change == 50
    assert se.source == "grunt"
    assert se.t == pytest.approx(12.5)


def test_enemy_killed_event_noop_when_telemetry_disabled():
    bus = EventBus()
    client = FakeTelemetryClient()
    ctx = FakeCtx(enable_telemetry=False, client=client)
    gs = FakeGameState(score=500, run_time=3.0)

    register_telemetry_event_handlers(bus, ctx, gs)

    ev = GameEvent(type="enemy_killed", payload={"enemy_type": "grunt", "score_delta": 50})
    bus.publish(ev)

    assert client.logged == []


def test_enemy_killed_event_noop_when_client_is_none():
    bus = EventBus()
    ctx = FakeCtx(enable_telemetry=True, client=None)
    gs = FakeGameState(score=500, run_time=3.0)

    register_telemetry_event_handlers(bus, ctx, gs)

    ev = GameEvent(type="enemy_killed", payload={"enemy_type": "grunt", "score_delta": 50})

    # Should not raise even if client is None
    bus.publish(ev)


def test_enemy_killed_event_ignored_when_score_delta_zero():
    bus = EventBus()
    client = FakeTelemetryClient()
    ctx = FakeCtx(enable_telemetry=True, client=client)
    gs = FakeGameState(score=999, run_time=1.0)

    register_telemetry_event_handlers(bus, ctx, gs)

    ev = GameEvent(type="enemy_killed", payload={"enemy_type": "grunt", "score_delta": 0})
    bus.publish(ev)

    assert client.logged == []
