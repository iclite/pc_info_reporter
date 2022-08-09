import wx
import wx.adv
import server

config = {
    "name": "PC Info Reporter Server",
    "version": '0.0.1'
}

class PcInfoServerGUIMainFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.Center(wx.BOTH)

        self.pnl = wx.Panel(self)

        self.st = wx.StaticText(self.pnl, label='', pos=(150, 25), style=wx.ALIGN_RIGHT)

        self.status_bar = self.CreateStatusBar()
        self.status_bar.SetFieldsCount(2)
        self.status_bar.SetStatusWidths([-3, -1])
        self.status_bar.SetStatusText("", 0)
        self.status_bar.SetStatusText("Stop", 1)

        self.start = False
        self.btn_convert = wx.Button(self.pnl, label='Start', pos=(150, 120))
        self.Bind(wx.EVT_BUTTON, self.start_button_action, self.btn_convert)

    def start_button_action(self, event):
        if self.start == False:
            self.start = True

            self.status_bar.SetStatusText("Starting...", 1)
            self.discover_server = server.DiscoverThread()
            self.report_server = server.ReportThread()

            self.discover_server.start()
            self.report_server.start()

            server_string = "IP: "

            for host in server.get_host_ip():
                server_string += f"[{host}] "

            self.status_bar.SetStatusText(server_string, 0)
            self.status_bar.SetStatusText("Started", 1)
            self.btn_convert.SetLabel('Stop')
        else:
            self.start = False

            self.status_bar.SetStatusText("Stopping...", 1)
            
            self.discover_server.stop()
            self.report_server.stop()

            self.discover_server.join()
            self.report_server.join()
            
            self.discover_server = None
            self.report_server = None

            self.status_bar.SetStatusText("", 0)
            self.status_bar.SetStatusText("Stopped", 1)
            self.btn_convert.SetLabel('Start')


class PcInfoServerGUI(wx.App):
    def OnInit(self):
        self.frame = PcInfoServerGUIMainFrame(None, title=f'{config["name"]} {config["version"]}', size=(400, 250))
        self.frame.Show()

        return True

if __name__ == '__main__':
    pc_info_server_gui = PcInfoServerGUI()
    pc_info_server_gui.MainLoop()