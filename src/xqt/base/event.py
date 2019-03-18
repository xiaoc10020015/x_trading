from collections import defaultdict
from queue import Empty, Queue
from threading import Thread
from time import sleep
from typing import Any, Callable

EVENT_TICK = "eTick."
EVENT_TRADE = "eTrade."
EVENT_ORDER = "eOrder."
EVENT_POSITION = "ePosition."
EVENT_ACCOUNT = "eAccount."
EVENT_CONTRACT = "eContract."
EVENT_LOG = "eLog"

EVENT_TIMER_TYPE = "evt_timer_type"


class Event:
    def __init__(self, evt_type: str, data: Any = None):
        """"""
        self.type = evt_type
        self.data = data


HandlerType = Callable[[Event], None]


class EventManager:
    def __init__(self, interval: int = 1):
        self._interval = interval
        self._queue = Queue()
        self._active = False
        self._thread = Thread(target=self._run)
        self._timer = Thread(target=self._run_timer)
        self._handlers = defaultdict(list)
        self._general_handlers = []

    # 事件监听线程
    def _run(self):
        while self._active:
            try:
                event = self._queue.get(block=True, timeout=1)
                self._process(evt=event)
            except Empty:
                pass

    # 事件处理
    def _process(self, evt: Event):
        if evt.type in self._handlers:
            [handler(evt) for handler in self._handlers[evt.type]]

        if self._general_handlers:
            [handler(evt) for handler in self._general_handlers]

    # 心跳线程
    def _run_timer(self):
        while self._active:
            sleep(self._interval)
            evt = Event(evt_type=EVENT_TIMER_TYPE)
            self.put(evt)

    # 启动事件
    def start(self):
        self._active = True
        self._thread.start()
        self._timer.start()

    # 停止事件
    def stop(self):
        self._active = False
        self._thread.join()
        self._timer.join()

    # 入栈
    def put(self, evt: Event):
        self._queue.put(evt)

    # 注册事件
    def register(self, evt_type: str, handler: HandlerType):
        handler_list = self._handlers[evt_type]
        if handler not in handler_list:
            self._handlersder.append(handler)

    # 注销事件
    def unregister(self, evt_type: str, handler: HandlerType):
        handler_list = self._handlers[evt_type]
        if handler not in handler_list:
            self._handlersder.pop(handler)

    # 注册公共事件
    def register_general(self, handler: HandlerType):
        if handler not in self._general_handlers:
            self._general_handlers.append(handler)

    # 注销公共事件
    def unregister_general(self, handler: HandlerType):
        if handler in self._general_handlers:
            self._general_handlers.remove(handler)
