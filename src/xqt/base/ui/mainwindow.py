from PyQt5 import QtCore, QtGui, QtWidgets
from functools import partial
from importlib import import_module
from ..utility import TRADER_PATH, get_icon_path
from typing import Callable
import webbrowser

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, main_engine, event_engine):
        super(MainWindow, self).__init__()
        self.main_engine = main_engine
        self.event_engine = event_engine
        self.window_title = f'VN Trader [{TRADER_PATH}]'
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(self.window_title)
        self.init_dock()
        self.init_menu()
        # self.load_window_setting("custom")
    def init_dock(self):
        pass
    def init_menu(self):
        """"""
        bar = self.menuBar()

        sys_menu = bar.addMenu("系统")
        app_menu = bar.addMenu("功能")
        help_menu = bar.addMenu("帮助")

        # System menu
        gateway_names = self.main_engine.get_all_gateway_names()
        for name in gateway_names:
            func = partial(self.connect, name)
            self.add_menu_action(sys_menu, f"连接{name}", "connect.ico", func)

        sys_menu.addSeparator()

        self.add_menu_action(sys_menu, "退出", "exit.ico", self.close)

        # App menu
        all_apps = self.main_engine.get_all_apps()
        for app in all_apps:
            ui_module = import_module(app.app_module + ".ui")
            widget_class = getattr(ui_module, app.widget_name)

            func = partial(self.open_widget, widget_class, app.app_name)
            icon_path = str(app.app_path.joinpath("ui", app.icon_name))
            self.add_menu_action(
                app_menu, f"打开{app.display_name}", icon_path, func
            )

        # Help menu
        # self.add_menu_action(
        #     help_menu,
        #     "查询合约",
        #     "contract.ico",
        #     partial(self.open_widget, ContractManager, "contract"),
        # )

        self.add_menu_action(
            help_menu, "还原窗口", "restore.ico", self.restore_window_setting
        )

        self.add_menu_action(
            help_menu, "测试邮件", "email.ico", self.send_test_email
        )

        self.add_menu_action(
            help_menu, "社区论坛", "forum.ico", self.open_forum
        )

        # self.add_menu_action(
        #     help_menu,
        #     "关于",
        #     "about.ico",
        #     partial(self.open_widget, AboutDialog, "about"),
        # )
    def add_menu_action(
        self,
        menu: QtWidgets.QMenu,
        action_name: str,
        icon_name: str,
        func: Callable,
    ):
        """"""
        icon = QtGui.QIcon(get_icon_path(__file__, icon_name))

        action = QtWidgets.QAction(action_name, self)
        action.triggered.connect(func)
        action.setIcon(icon)

        menu.addAction(action)

    def restore_window_setting(self):
        """
        Restore window to default setting.
        """
        self.load_window_setting("default")
        self.showMaximized()

    def send_test_email(self):
        """
        Sending a test email.
        """
        self.main_engine.send_email("VN Trader", "testing")

    def open_forum(self):
        """
        """
        webbrowser.open("https://www.vnpy.com/forum/")

    def load_window_setting(self, name: str):
        """
        Load previous window size and state by trader path and setting name.
        """
        settings = QtCore.QSettings(self.window_title, name)
        state = settings.value("state")
        geometry = settings.value("geometry")

        if isinstance(state, QtCore.QByteArray):
            self.restoreState(state)
            self.restoreGeometry(geometry)
