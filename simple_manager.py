class AbstractTabManager:

    def __init__(self, parent):
        from window import Window
        self.parent: Window = parent

        self.parent.tabs.currentChanged.connect(self.tab_changed)

    def tab_changed(self, index: int):
        pass
