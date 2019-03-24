from abc import ABC
from src.xqt.event.engine import EventEngine

class MainEngine:
    def __init__(self):
        self.gateways = {}
        self.engines = {}
        self.apps = {}

    def get_all_gateway_names(self):
        """
        Get all names of gatewasy added in main engine.
        """
        return list(self.gateways.keys())

    def get_all_apps(self):
        """
        Get all app objects.
        """
        return list(self.apps.values())

    def connect(self, setting: dict, gateway_name: str):
        """
        Start connection of a specific gateway.
        """
        gateway = self.get_gateway(gateway_name)
        if gateway:
            gateway.connect(setting)

class BaseEngine(ABC):
    """
    Abstract class for implementing an function engine.
    """

    def __init__(
        self,
        main_engine: MainEngine,
        event_engine: EventEngine,
        engine_name: str,
    ):
        """"""
        self.main_engine = main_engine
        self.event_engine = event_engine
        self.engine_name = engine_name

    def close(self):
        """"""
        pass
