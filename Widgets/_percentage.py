__author__ = 'schaef'

from _widget import Widget


class PercentageWidget(Widget):

    def __init__(self, click_callback, label, default_value=50, max_w=15):
        Widget.__init__(self, max_w)
        self.line1 = label
        if default_value < 0:
            default_value = 0
        if default_value > 100:
            default_value = 100
        self.percentage = default_value
        self.click_callback = click_callback

    def refresh(self):
        Widget.refresh(self)


    def click(self):
        self.click_callback(self.percentage)
        pass

    def dial(self, value):
        old_percentage = self.percentage
        # value is between 0 and 300
        self.percentage = int(value / 3)
        self.line2 = '#' * int((self.percentage*self.max_w-1)/100.0 + 1)
        self.dirty = (old_percentage != self.percentage)
        pass



