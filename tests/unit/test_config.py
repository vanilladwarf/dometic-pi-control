"""Tests for the Config loader."""
import textwrap
import pytest
from pathlib import Path
from dometic.config import (
    Config, ThermostatCfg, ProtectionsCfg, SensorsCfg,
    PinsCfg, ApiCfg, LoopCfg, MqttCfg, load_config,
)


def test_default_config_has_all_sections():
    cfg = Config()
    assert isinstance(cfg.thermostat, ThermostatCfg)
    assert isinstance(cfg.protections, ProtectionsCfg)
    assert isinstance(cfg.sensors, SensorsCfg)
    assert isinstance(cfg.pins, PinsCfg)
    assert isinstance(cfg.api, ApiCfg)
    assert isinstance(cfg.loop, LoopCfg)
    assert isinstance(cfg.mqtt, MqttCfg)


def test_default_setpoints():
    cfg = Config()
    assert cfg.thermostat.setpoint_cool_f == 74.0
    assert cfg.thermostat.setpoint_heat_f == 68.0


def test_default_protection_timers():
    cfg = Config()
    assert cfg.protections.min_compressor_off_secs == 120
    assert cfg.protections.heat_pump_lockout_f == 24.0
    assert cfg.protections.hard_lockout_f == 10.0


def test_load_config_from_yaml(tmp_path, monkeypatch):
    yaml = textwrap.dedent("""
        thermostat:
          setpoint_cool_f: 70
          setpoint_heat_f: 65
        protections:
          min_compressor_off_secs: 60
    """).strip()
    cfg_file = tmp_path / "config.yaml"
    cfg_file.write_text(yaml)
    monkeypatch.setenv("DOMETIC_CONFIG", str(cfg_file))
    cfg = load_config(force=True)
    assert cfg.thermostat.setpoint_cool_f == 70.0
    assert cfg.thermostat.setpoint_heat_f == 65.0
    assert cfg.protections.min_compressor_off_secs == 60
    assert cfg.thermostat.cool_deadband_f == 1.5


def test_pin_map_keys_present():
    from dometic.pins import get_pin_map
    cfg = Config()
    pins = get_pin_map(cfg)
    assert "FAN_LOW" in pins
    assert "COOL" in pins
    assert "HEAT_PUMP" in pins
    assert "COMP1" in pins
    assert "RV1" in pins
