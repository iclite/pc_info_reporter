import wx
import wx.adv
import client

config = {
    "name": "PC Info Reporter Client",
    "version": '0.0.1'
}


class PcInfoClientGUIMainFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.Center(wx.BOTH)

        self.pnl = wx.Panel(self)

        self.st = wx.StaticText(self.pnl, label='', pos=(150, 25), style=wx.ALIGN_RIGHT)

        self.status_bar = self.CreateStatusBar()
        self.status_bar.SetFieldsCount(2)
        self.status_bar.SetStatusWidths([-3, -1])
        self.status_bar.SetStatusText("", 0)
        self.status_bar.SetStatusText("Waiting", 1)

        self.btn_upload = wx.Button(self.pnl, label='Upload', pos=(150, 120))
        self.Bind(wx.EVT_BUTTON, self.upload_button_action, self.btn_upload)

    def upload_button_action(self, event):
        self.start = True

        self.status_bar.SetStatusText("Upload...", 1)

        if client.report_info():
            self.status_bar.SetStatusText("Upload Success!", 0)
            self.status_bar.SetStatusText("Uploaded", 1)
        else:
            self.status_bar.SetStatusText("Something error!", 0)
            self.status_bar.SetStatusText("Failure", 1)

class PcInfoClientGUI(wx.App):
    def OnInit(self):
        self.frame = PcInfoClientGUIMainFrame(None, title=f'{config["name"]} {config["version"]}', size=(400, 250))
        self.frame.Show()

        return True

if __name__ == '__main__':
    pc_info_Client_gui = PcInfoClientGUI()
    pc_info_Client_gui.MainLoop()