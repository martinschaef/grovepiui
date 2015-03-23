__author__ = 'schaef'

from _widget import Widget

class ListWidget(Widget):

    def __init__(self, string_list, click_callback, cancel_callback=None, max_w=15):
        Widget.__init__(self, max_w)
        self.string_list = list(string_list)
        self.click_callback = click_callback
        self.cancel_callback = cancel_callback
        if self.cancel_callback:
            self.string_list.append('-- back --')

        self.list_index = 0

        if len(string_list) < 1:
            raise RuntimeError("Cannot create ListWidget for empty list.")
        if len(string_list) > 30:
            raise RuntimeError("Cannot create ListWidget with more than 30 elements.")


    def refresh(self):
        Widget.refresh(self)


    def click(self):
        # if we added a cancel, check if this is selected.
        if self.cancel_callback and self.list_index is len(self.string_list)-1:
            return self.cancel_callback()

        self.click_callback(self.list_index)
        pass

    def dial(self, value):
        # value is between 0 and 300
        old_index = self.list_index

        self.list_index = int(float(value)/300.0 * float(len(self.string_list)-1))
        self.line1 = self.string_list[self.list_index]

        # check if we can add the next line to the screen as well.
        if 0 <= self.list_index < len(self.string_list)-1:
            self.line2 = self.string_list[self.list_index+1]
        else:
            self.line2 = ""
        if self.list_index != old_index:
            self.dirty = True
        pass



