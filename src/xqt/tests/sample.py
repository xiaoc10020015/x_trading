
from src.xqt.base.engine import MainEngine
from src.xqt.event import EventEngine
from src.xqt.base.ui.mainwindow import MainWindow
from src.xqt.base.ui import create_qapp


qapp = create_qapp()

event_manger = EventEngine()
main_manager = MainEngine()
main_window = MainWindow(main_engine=main_manager, event_engine=event_manger)
main_window.showMaximized()
qapp.exec()

