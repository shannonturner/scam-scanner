from bs4 import BeautifulSoup, SoupStrainer
import os.path
import re
import time
import urllib2
import webbrowser
import whoisclient
import wx
import xlrd

class Panel_Criteria(wx.Panel):

    """ Panel_Criteria() is the wx.Panel where the criteria and innocuous criteria that will be checked for are set.
    """

    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)

        criteria_icon = [0,1,2,3]
        criteria_button = [0,1,2,3]
        criteria_label = [0,1,2,3]
        clear_button = [0,1]

        static_box = [0,1]
        sbox = [0,1]
        hbox = [0,1,2,3,4,5]
        vbox = wx.BoxSizer(wx.VERTICAL)

        criteria_icon[0] = wx.Bitmap("icons/criteria.png", wx.BITMAP_TYPE_PNG)
        criteria_button[0] = wx.BitmapButton(self, bitmap=criteria_icon[0], size=(criteria_icon[0].GetWidth()+16, criteria_icon[0].GetHeight()+16))
        criteria_button[0].SetBitmapHover(wx.Bitmap("icons/criteria-hover.png", wx.BITMAP_TYPE_PNG))
        criteria_button[0].SetBitmapSelected(wx.Bitmap("icons/criteria-selected.png", wx.BITMAP_TYPE_PNG))
        criteria_button[0].Bind(wx.EVT_BUTTON, lambda load_type: self.load("load")) 

        criteria_icon[1] = wx.Bitmap("icons/criteria-qe.png", wx.BITMAP_TYPE_PNG)
        criteria_button[1] = wx.BitmapButton(self, bitmap=criteria_icon[1], size=(criteria_icon[1].GetWidth()+16, criteria_icon[1].GetHeight()+16))
        criteria_button[1].SetBitmapHover(wx.Bitmap("icons/criteria-hover-qe.png", wx.BITMAP_TYPE_PNG))
        criteria_button[1].SetBitmapSelected(wx.Bitmap("icons/criteria-selected-qe.png", wx.BITMAP_TYPE_PNG))
        criteria_button[1].Bind(wx.EVT_BUTTON, lambda load_type: self.load("quick"))

        criteria_icon[2] = wx.Bitmap("icons/criteria-innoc.png", wx.BITMAP_TYPE_PNG)  
        criteria_button[2] = wx.BitmapButton(self, bitmap=criteria_icon[2], size=(criteria_icon[2].GetWidth()+16, criteria_icon[2].GetHeight()+16))
        criteria_button[2].SetBitmapHover(wx.Bitmap("icons/criteria-innoc-hover.png", wx.BITMAP_TYPE_PNG)) 
        criteria_button[2].SetBitmapSelected(wx.Bitmap("icons/criteria-innoc-selected.png", wx.BITMAP_TYPE_PNG)) 
        criteria_button[2].Bind(wx.EVT_BUTTON, lambda load_type: self.load("load-innoc"))

        criteria_icon[3] = wx.Bitmap("icons/criteria-qe-innoc.png", wx.BITMAP_TYPE_PNG) 
        criteria_button[3] = wx.BitmapButton(self, bitmap=criteria_icon[3], size=(criteria_icon[3].GetWidth()+16, criteria_icon[3].GetHeight()+16))
        criteria_button[3].SetBitmapHover(wx.Bitmap("icons/criteria-hover-qe-innoc.png", wx.BITMAP_TYPE_PNG)) 
        criteria_button[3].SetBitmapSelected(wx.Bitmap("icons/criteria-selected-qe-innoc.png", wx.BITMAP_TYPE_PNG))  
        criteria_button[3].Bind(wx.EVT_BUTTON, lambda load_type: self.load("quick-innoc"))

        criteria_label[0] = wx.StaticText(self, label="Load Criteria: Select a file in comma or tab-delimited format to use as your criteria;\nthe first row of your spreadsheet is reserved as a header row.")
        criteria_label[1] = wx.StaticText(self, label="Quick-Edit Criteria: Opens a file in the system-default spreadsheet editor for making quick edits.\n\nSets this file as the file to use as your criteria. (Just be sure to save and close your file before runtime!)")
        criteria_label[2] = wx.StaticText(self, label="(Optional) Load Innocuous: Select a file in plaintext format to use as a list of innocuous criteria / criteria to ignore.")
        criteria_label[3] = wx.StaticText(self, label="(Optional) Quick-Edit Innocuous: Opens a file in the system-default text editor for making quick edits. \n\nSets this file as the file to use as your innocuous criteria. (Just be sure to save and close your file before runtime!)")

        self.criteria_filename = wx.TextCtrl(self, value="", size=(400,20), style=wx.TE_READONLY)
        self.innocuous_filename = wx.TextCtrl(self, value="", size=(400,20), style=wx.TE_READONLY)

        clear_button[0] = wx.Button(self, label="Clear")
        clear_button[0].Bind(wx.EVT_BUTTON, lambda clear_field: self.clear("criteria"))
        clear_button[1] = wx.Button(self, label="Clear")
        clear_button[1].Bind(wx.EVT_BUTTON, lambda clear_field: self.clear("innocuous"))

        static_box[0] = wx.StaticBox(self, label="Criteria to scan for")
        static_box[1] = wx.StaticBox(self, label="(Optional) Innocuous criteria to ignore")

        hbox[0] = wx.BoxSizer(wx.HORIZONTAL)
        hbox[0].Add(criteria_button[0], proportion=0, border=10, flag=wx.ALL|wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
        hbox[0].Add(criteria_label[0], proportion=1, border=5, flag=wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL)

        hbox[1] = wx.BoxSizer(wx.HORIZONTAL)
        hbox[1].Add(wx.StaticText(self, label="Filename: "), proportion=0, border=10, flag=wx.LEFT|wx.TOP|wx.BOTTOM|wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
        hbox[1].Add(self.criteria_filename, proportion=1, border=5, flag=wx.ALL|wx.EXPAND|wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL)
        hbox[1].Add(clear_button[0], proportion=0, border=5, flag=wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)

        hbox[2] = wx.BoxSizer(wx.HORIZONTAL)
        hbox[2].Add(criteria_button[1], proportion=0, border=10, flag=wx.ALL|wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL) 
        hbox[2].Add(criteria_label[1], proportion=1, border=5, flag=wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL)
        
        hbox[3] = wx.BoxSizer(wx.HORIZONTAL)
        hbox[3].Add(criteria_button[2], proportion=0, border=10, flag=wx.ALL|wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
        hbox[3].Add(criteria_label[2], proportion=1, border=5, flag=wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL)
        
        hbox[4] = wx.BoxSizer(wx.HORIZONTAL)
        hbox[4].Add(wx.StaticText(self, label="Filename: "), proportion=0, border=10, flag=wx.LEFT|wx.TOP|wx.BOTTOM|wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
        hbox[4].Add(self.innocuous_filename, proportion=1, border=5, flag=wx.ALL|wx.EXPAND|wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL)
        hbox[4].Add(clear_button[1], proportion=0, border=5, flag=wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        
        hbox[5] = wx.BoxSizer(wx.HORIZONTAL)
        hbox[5].Add(criteria_button[3], proportion=0, border=10, flag=wx.ALL|wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
        hbox[5].Add(criteria_label[3], proportion=1, border=5, flag=wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL)
        
        sbox[0] = wx.StaticBoxSizer(static_box[0], wx.VERTICAL)
        sbox[0].Add(hbox[0], proportion=1, flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL)
        sbox[0].Add(hbox[1], flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL)
        sbox[0].Add(hbox[2], proportion=1, flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL)

        sbox[1] = wx.StaticBoxSizer(static_box[1], wx.VERTICAL)
        sbox[1].Add(hbox[3], proportion=1, flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL)
        sbox[1].Add(hbox[4], flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL)
        sbox[1].Add(hbox[5], proportion=1, flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL)

        vbox.Add(sbox[0], proportion=1, border=5, flag=wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL)
        vbox.Add(sbox[1], proportion=1, border=5, flag=wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL)

        self.SetSizerAndFit(vbox)

    def load(self, load_type):

        """ load(load_type): Selects the (criteria|innocuous criteria) file to be used, or opens the file for quick editing and then sets the file to be used.
        """

        if (load_type == "load" or load_type == "quick"):
            file_dialog = wx.FileDialog(self, message="Open criteria file ...", defaultFile="", wildcard="Excel Spreadsheet (*.xls, *.xlsx)|*.xls;*.xlsx|Tab Separated Values (*.tsv; *.txt)|*.tsv;*.txt|Comma Separated Values (*.csv)|*.csv", style=wx.OPEN)
            if file_dialog.ShowModal() == wx.ID_OK:
                self.criteria_filename.SetValue("{}\\{}".format(file_dialog.GetDirectory(), file_dialog.GetFilename()))
                if (load_type == "quick"):
                    os.startfile("{}\\{}".format(file_dialog.GetDirectory(), file_dialog.GetFilename()))
        else:
            file_dialog = wx.FileDialog(self, message="Open innocuous criteria file ...", defaultFile="", wildcard="Plaintext file (*.txt)|*.txt", style=wx.OPEN)
            if file_dialog.ShowModal() == wx.ID_OK:
                self.innocuous_filename.SetValue("{}\\{}".format(file_dialog.GetDirectory(), file_dialog.GetFilename()))
                if (load_type == "quick-innoc"):
                    os.startfile("{}\\{}".format(file_dialog.GetDirectory(), file_dialog.GetFilename()))

    def clear(self, clear_field):

        """ clear(clear_field): The wx.TextCtrl fields are readonly (to ensure a valid file path and name), but there needs to be a way to delete the contents.
        """
        
        if clear_field == "criteria":
            self.criteria_filename.SetValue("")
        elif clear_field == "innocuous":
            self.innocuous_filename.SetValue("")

class Panel_Websites(wx.Panel):

    """ Panel_Websites() is the wx.Panel where the websites that will be checked for criteria are set.
    """

    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)

        websites_icon = [0,1]
        websites_button = [0,1]
        websites_label = [0,1]

        static_box = [0]
        sbox = [0]
        hbox = [0,1,2,3]
        vbox = wx.BoxSizer(wx.VERTICAL)

        websites_icon[0] = wx.Bitmap("icons/websites.png", wx.BITMAP_TYPE_PNG) 
        websites_button[0] = wx.BitmapButton(self, bitmap=websites_icon[0], size=(websites_icon[0].GetWidth()+16, websites_icon[0].GetHeight()+16))
        websites_button[0].SetBitmapHover(wx.Bitmap("icons/websites-hover.png", wx.BITMAP_TYPE_PNG))
        websites_button[0].SetBitmapSelected(wx.Bitmap("icons/websites-selected.png", wx.BITMAP_TYPE_PNG))
        websites_button[0].Bind(wx.EVT_BUTTON, lambda load_type: self.load("load"))

        websites_icon[1] = wx.Bitmap("icons/websites-qe.png", wx.BITMAP_TYPE_PNG) 
        websites_button[1] = wx.BitmapButton(self, bitmap=websites_icon[1], size=(websites_icon[1].GetWidth()+16, websites_icon[1].GetHeight()+16))
        websites_button[1].SetBitmapHover(wx.Bitmap("icons/websites-hover-qe.png", wx.BITMAP_TYPE_PNG))
        websites_button[1].SetBitmapSelected(wx.Bitmap("icons/websites-selected-qe.png", wx.BITMAP_TYPE_PNG))
        websites_button[1].Bind(wx.EVT_BUTTON, lambda load_type: self.load("quick"))

        websites_label[0] = wx.StaticText(self, label="Load Website list: Select a file in plaintext format to use as the list of websites to search criteria on.")
        websites_label[1] = wx.StaticText(self, label="Quick-Edit Website list: Opens a file in the system-default text editor for making quick edits.\n\nSets this file as the file to use as your website list. (Just be sure to save and close your file before runtime!)")

        self.websites_filename = wx.TextCtrl(self, value="", size=(400,20), style=wx.TE_READONLY)

        static_box[0] = wx.StaticBox(self, label="Websites to scan")

        hbox[0] = wx.BoxSizer(wx.HORIZONTAL)
        hbox[0].Add(websites_button[0], proportion=0, border=50, flag=wx.ALL|wx.ALIGN_LEFT)
        hbox[0].Add(websites_label[0], proportion=1, border=50, flag=wx.ALIGN_CENTER) 

        hbox[1] = wx.BoxSizer(wx.HORIZONTAL)
        hbox[1].Add(wx.StaticText(self, label="Filename: "), proportion=0, border=20, flag=wx.LEFT|wx.TOP|wx.BOTTOM|wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
        hbox[1].Add(self.websites_filename, proportion=1, border=25, flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)

        hbox[2] = wx.BoxSizer(wx.HORIZONTAL)
        hbox[2].Add(wx.StaticLine(self, size=(500, 5)), proportion=1, border=20, flag=wx.ALL|wx.ALIGN_CENTER)

        hbox[3] = wx.BoxSizer(wx.HORIZONTAL)
        hbox[3].Add(websites_button[1], proportion=0, border=50, flag=wx.ALL|wx.ALIGN_LEFT)
        hbox[3].Add(websites_label[1], proportion=1, border=50, flag=wx.ALIGN_CENTER)

        sbox[0] = wx.StaticBoxSizer(static_box[0], wx.VERTICAL)
        sbox[0].Add(hbox[0], flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL)
        sbox[0].Add(hbox[1], flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL)
        sbox[0].Add(hbox[2], proportion=1, flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL)
        sbox[0].Add(hbox[3], flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL)

        vbox.Add(sbox[0], proportion=1, border=5, flag=wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL)

        self.SetSizerAndFit(vbox)

    def load(self, load_type):

        """ load(load_type): Selects the websites file to be used, or opens the file for quick editing and then sets the file to be used.
        """
        
        file_dialog = wx.FileDialog(self, message="Open websites file ...", defaultFile="", wildcard="Text File (*.txt)|*.txt", style=wx.OPEN)
        if (file_dialog.ShowModal() == wx.ID_OK):
            self.websites_filename.SetValue("{}\\{}".format(file_dialog.GetDirectory(), file_dialog.GetFilename()))
            if (load_type == "quick"):
                os.startfile("{}\\{}".format(file_dialog.GetDirectory(), file_dialog.GetFilename()))

class Panel_Configuration(wx.Panel):

    """ Panel_Configuration() is the wx.Panel where important configuration details like depth and delay are set.
    """

    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)

        self.saveresults_checkbox = [0,1,2]

        self.spin_depth = wx.SpinCtrl(self, min=0, max=6, initial=2)        
        self.spin_delay = wx.SpinCtrl(self, min=0, max=5, initial=2)

        spin_depth_label = wx.StaticText(self, label="""The number of levels of links to visit beyond the home page. \nEach additional level increases the number of pages visited (and the runtime of the program) exponentially. Use: \n
0\t to just look at the home pages of the sites you've provided.\n
1\t to look at the home pages and every page linked on the home page for the sites you've provided.\n
2\t to look at the home pages, every page linked on those home pages, and each link on each page listed in #1.\t\t\t
3\t and above continue in the same fashion. \n\nIn most cases, 2 or 3 depth is enough to visit all of the pages on a website.\n""")

        spin_delay_label = wx.StaticText(self, label="""The number of seconds to wait in between visiting each page. Use: \n
0\t to visit pages with no delay. May alert sysadmins that you're watching if run repeatedly on large sites.\t\t\t
1\t to visit pages quickly but arousing less suspicion.\n
2\t to visit pages at an average pace.  Won't arouse suspicion. \n
3\t and above will increase the runtime significantly, but will also make your web traffic look more human.\n\n""")

        self.saveresults_checkbox[0] = wx.CheckBox(self, label="Save results to a quick-view spreadsheet")
        self.saveresults_checkbox[0].SetValue(True)
        
        self.saveresults_checkbox[1] = wx.CheckBox(self, label="Save results in a fully detailed report")
        self.saveresults_checkbox[1].SetValue(True)
        
        self.saveresults_checkbox[2] = wx.CheckBox(self, label="Open results automatically when runtime is finished")
        self.saveresults_checkbox[2].SetValue(True)

        self.saveresults_path = wx.TextCtrl(self, value="", size=(400,20), style=wx.TE_READONLY)
        saveresults_changepath = wx.Button(self, label="Change Save Path")
        saveresults_changepath.Bind(wx.EVT_BUTTON, self.choosedir)

        static_box = [0,1,2]
        sbox = [0,1,2]
        hbox = [0,1,2,3,4,5]
        vbox = wx.BoxSizer(wx.VERTICAL)

        static_box[0] = wx.StaticBox(self, label="Site Depth")
        static_box[1] = wx.StaticBox(self, label="Page Delay")
        static_box[2] = wx.StaticBox(self, label="Save Results")

        hbox[0] = wx.BoxSizer(wx.HORIZONTAL)
        hbox[0].Add(self.spin_depth, proportion=0, border=10, flag=wx.ALL|wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
        hbox[0].Add(spin_depth_label, proportion=1, border=5, flag=wx.ALL|wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL)
        
        hbox[1] = wx.BoxSizer(wx.HORIZONTAL)
        hbox[1].Add(self.spin_delay, proportion=0, border=10, flag=wx.ALL|wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
        hbox[1].Add(spin_delay_label, proportion=1, border=5, flag=wx.ALL|wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL)
        
        hbox[2] = wx.BoxSizer(wx.HORIZONTAL)
        hbox[2].Add(self.saveresults_checkbox[0], proportion=1, border=10, flag=wx.ALL|wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL)
        
        hbox[3] = wx.BoxSizer(wx.HORIZONTAL)
        hbox[3].Add(self.saveresults_checkbox[1], proportion=1, border=10, flag=wx.ALL|wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL)
        
        hbox[4] = wx.BoxSizer(wx.HORIZONTAL)
        hbox[4].Add(self.saveresults_checkbox[2], proportion=1, border=10, flag=wx.ALL|wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL)
        
        hbox[5] = wx.BoxSizer(wx.HORIZONTAL)
        hbox[5].Add(wx.StaticText(self, label="Your files will be saved to: "), proportion=0, border=15, flag=wx.LEFT|wx.TOP|wx.BOTTOM|wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
        hbox[5].Add(self.saveresults_path, proportion=1, border=5, flag=wx.ALL|wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL)
        hbox[5].Add(saveresults_changepath, proportion=0, border=15, flag=wx.ALIGN_LEFT|wx.TOP|wx.BOTTOM|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL)

        for x in xrange(3):
            sbox[x] = wx.StaticBoxSizer(static_box[x], wx.VERTICAL)
            sbox[x].Add(hbox[x], proportion=1, flag=wx.EXPAND)

        for x in xrange(3,6):
            if x == 5: # I don't want the wx.TextCtrl for saveresults_path to be stretched the wrong way
                sbox[2].Add(hbox[x], flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL) 
            else:
                sbox[2].Add(hbox[x], proportion=1)

        for x in xrange(3):
            vbox.Add(sbox[x], proportion=1, border=5, flag=wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL)
        
        self.SetSizerAndFit(vbox)

    def choosedir(self, event):

        """ choosedir(): Opens a dialog to choose the folder where files will be saved.
        """
        
        dir_dialog = wx.DirDialog(self, message="Choose Save Folder ...", style=wx.OPEN)
        if (dir_dialog.ShowModal() == wx.ID_OK):
            self.saveresults_path.SetValue(dir_dialog.GetPath())

class Panel_Advanced(wx.Panel):

    """ Panel_Advanced() is the wx.Panel where advanced settings are set.
    """

    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)

        advanced_disclaimer = wx.StaticText(self, label="If you're unfamiliar with these settings, you can leave these settings alone and run the scan.")

        self.user_agent = wx.TextCtrl(self, value="Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0", size=(200,20))
        self.referral_string = wx.TextCtrl(self, value="", size=(200,20))

        self.proxy_ip = wx.TextCtrl(self, value="", size=(200,20))
        self.proxy_port = wx.TextCtrl(self, value="", size=(60,20))

        self.tineye_apikey = wx.TextCtrl(self, value="", size=(200,20))

        self.whois_check = wx.CheckBox(self, label="Get WHOIS data for each domain")
        self.whois_check.SetValue(True)
        
        self.domaindispute_rightsholders = wx.TextCtrl(self, value="", style=wx.TE_READONLY, size=(400,20))
        domaindispute_rightsholders_change = wx.Button(self, label="Load rightsholders")
        domaindispute_rightsholders_change.Bind(wx.EVT_BUTTON, lambda load_type: self.load("rightsholders"))
        clear_button = wx.Button(self, label="Clear")
        clear_button.Bind(wx.EVT_BUTTON, lambda clear_field: self.clear("rightsholders"))

        ## TinEye API is EXPENSIVE ## Disabling for now
        self.tineye_apikey.Disable()

        static_box = [0,1,2,3,4]
        sbox = [0,1,2,3,4]
        hbox = [0,1,2,3,4,5,6,7,8]
        vbox = wx.BoxSizer(wx.VERTICAL)

        static_box[0] = wx.StaticBox(self, label="Custom Browsing Variables")
        static_box[1] = wx.StaticBox(self, label="Use Proxy when Browsing (If you have a system-wide proxy currently applied, you can leave these blank)")
        static_box[2] = wx.StaticBox(self, label="TinEye Configuration (not yet implemented)")
        static_box[3] = wx.StaticBox(self, label="WHOIS Checking (Note: Queries to the WHOIS servers will not be made behind the proxy unless your system-wide proxy is currently applied.)")
        static_box[4] = wx.StaticBox(self, label="Rightsholders to Check for WIPO-type Domain Name Violations")
        
        hbox[0] = wx.BoxSizer(wx.HORIZONTAL)
        hbox[0].Add(wx.StaticText(self, label="User-Agent: "), proportion=0, border=10, flag=wx.ALL|wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
        hbox[0].Add(self.user_agent, proportion=1, border=10, flag=wx.EXPAND|wx.ALL|wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL)
        
        hbox[1] = wx.BoxSizer(wx.HORIZONTAL)
        hbox[1].Add(wx.StaticText(self, label="Referral: "), proportion=0, border=10, flag=wx.ALL|wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
        hbox[1].Add(self.referral_string, proportion=1, border=10, flag=wx.ALL|wx.EXPAND|wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL)    

        hbox[2] = wx.BoxSizer(wx.HORIZONTAL)
        hbox[2].Add(wx.StaticText(self, label="Proxy IP: "), proportion=0, border=10, flag=wx.ALL|wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
        hbox[2].Add(self.proxy_ip, proportion=1, border=10, flag=wx.ALL|wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL)
        hbox[2].Add(wx.StaticText(self, label="Port: "), proportion=0, border=10, flag=wx.ALL|wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
        hbox[2].Add(self.proxy_port, proportion=1, border=10, flag=wx.ALL|wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL)
        
        hbox[3] = wx.BoxSizer(wx.HORIZONTAL)
        hbox[3].Add(wx.StaticText(self, label="TinEye API Key: "), proportion=0, border=10, flag=wx.ALL|wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
        hbox[3].Add(self.tineye_apikey, proportion=1, border=10, flag=wx.ALL|wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL)
        
        hbox[4] = wx.BoxSizer(wx.HORIZONTAL)
        hbox[4].Add(self.whois_check, proportion=1, border=10, flag=wx.ALL|wx.EXPAND|wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL)
        
        hbox[5] = wx.BoxSizer(wx.HORIZONTAL)
        hbox[5].Add(wx.StaticText(self, label="File: "), proportion=0, border=10, flag=wx.ALL|wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
        hbox[5].Add(self.domaindispute_rightsholders, proportion=1, border=10, flag=wx.EXPAND|wx.ALL|wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL)
        hbox[5].Add(domaindispute_rightsholders_change, proportion=0, border=10, flag=wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        hbox[5].Add(clear_button, proportion=0, border=10, flag=wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        
        for x in xrange(5):
            sbox[x] = wx.StaticBoxSizer(static_box[x], wx.VERTICAL)

        sbox[0].Add(hbox[0], flag=wx.EXPAND)
        sbox[0].Add(hbox[1], flag=wx.EXPAND)
        sbox[1].Add(hbox[2], proportion=1, flag=wx.EXPAND|wx.ALIGN_CENTER_VERTICAL)
        sbox[2].Add(hbox[3], proportion=1, flag=wx.EXPAND|wx.ALIGN_CENTER_VERTICAL)
        sbox[3].Add(hbox[4], proportion=1, flag=wx.EXPAND|wx.ALIGN_CENTER_VERTICAL)
        sbox[4].Add(hbox[5], flag=wx.EXPAND|wx.ALIGN_CENTER_VERTICAL)
        
        vbox.Add(advanced_disclaimer, border=10, flag=wx.ALIGN_CENTER)

        for x in xrange(4):
            vbox.Add(sbox[x], proportion=1, border=5, flag=wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL)

        vbox.Add(sbox[4], border=5, flag=wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL) # making the final one smaller

        self.SetSizerAndFit(vbox)

    def load(self, load_type):

        """ load(load_type): Selects the rightsholders file to be used.
        """
         
        file_dialog = wx.FileDialog(self, message="Open {} file ...".format(load_type), defaultFile="", wildcard="Text File (*.txt)|*.txt", style=wx.OPEN)
        if (file_dialog.ShowModal() == wx.ID_OK):
            if (load_type == "rightsholders"):
                self.domaindispute_rightsholders.SetValue("{}\\{}".format(file_dialog.GetDirectory(), file_dialog.GetFilename()))

    def clear(self, clear_field):

        """ clear(clear_field): The wx.TextCtrl fields are readonly (to ensure a valid file path and name), but there needs to be a way to delete the contents.
        """
        
        if clear_field == "rightsholders":
            self.domaindispute_rightsholders.SetValue("")
        

class Panel_Runtime(wx.Panel):

    """ Panel_Runtime() is the wx.Panel that displays the runtime log and progress.
    """

    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)

        self.progress_bar = [0,1,2]
        self.progress_label = [0,1,2]

        self.pl_websites_crawled = 0
        self.pl_websites_to_crawl = 0
        self.pl_current_website = ""
        self.pl_current_depth = 0
        self.pl_maximum_depth = 0
        self.pl_pages_this_depth = 0
        self.pl_total_pages_this_depth = 0

        self.progress_label[0] = wx.StaticText(self, label="")
        self.progress_label[1] = wx.StaticText(self, label="")
        self.progress_label[2] = wx.StaticText(self, label="")

        self.progress_bar[0] = wx.Gauge(self, range=0, size=(725,20)) 
        self.progress_bar[1] = wx.Gauge(self, range=0, size=(725,20))
        self.progress_bar[2] = wx.Gauge(self, range=0, size=(725,20))

        self.runtime_log = wx.TextCtrl(self, size=(700,250), style=wx.TE_MULTILINE|wx.TE_READONLY)

        self.open_folder = wx.Button(self, label="Open Folder")
        self.open_folder.Bind(wx.EVT_BUTTON, self.Open_Folder)
        
        self.folder_path = wx.TextCtrl(self, value="", size=(500,20), style=wx.TE_READONLY)

        static_box = [0,1,2,3,4]
        sbox = [0,1,2,3,4]
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox = wx.BoxSizer(wx.VERTICAL)

        static_box[0] = wx.StaticBox(self, label="Websites Crawled")
        static_box[1] = wx.StaticBox(self, label="Current Depth")
        static_box[2] = wx.StaticBox(self, label="Pages Crawled this Depth")
        static_box[3] = wx.StaticBox(self, label="What's going on right now")
        static_box[4] = wx.StaticBox(self, label="When this run completes, you'll be able to view the results in the folder: ")

        for x in xrange(3):
            sbox[x] = wx.StaticBoxSizer(static_box[x], wx.VERTICAL)
            sbox[x].Add(self.progress_label[x], flag=wx.ALIGN_CENTER)
            sbox[x].Add(self.progress_bar[x], flag=wx.EXPAND|wx.ALIGN_CENTER)
        
        sbox[3] = wx.StaticBoxSizer(static_box[3], wx.VERTICAL)
        sbox[4] = wx.StaticBoxSizer(static_box[4], wx.VERTICAL)

        sbox[3].Add(self.runtime_log, proportion=1, flag=wx.EXPAND)
        hbox.Add(self.open_folder, proportion=0, border=10, flag=wx.ALL|wx.ALIGN_LEFT)
        hbox.Add(self.folder_path, proportion=1, border=10, flag=wx.ALL|wx.ALIGN_CENTER)
        sbox[4].Add(hbox, proportion=1, flag=wx.EXPAND)

        for self.add_sbox in xrange(5):
            if self.add_sbox == 3:
                vbox.Add(sbox[self.add_sbox], proportion=1, flag=wx.EXPAND)
            else:
                vbox.Add(sbox[self.add_sbox], proportion=0, flag=wx.EXPAND)

        self.SetSizerAndFit(vbox)

    def Open_Folder(self, event):

        """ Open_Folder(): Event to open the folder path in the OS
        """

        # TODO: try on other platforms too ... later
        webbrowser.open(self.folder_path.GetValue())

    def Append_Log(self, next_line):

        """ Append_Log(next_line): Appends next_line to both the runtime_log in the GUI and in the specified logfile.
        """

        self.runtime_log.SetValue("{}{}\n".format(self.runtime_log.GetValue(), next_line))
        self.runtime_log.ShowPosition(self.runtime_log.GetLastPosition())
        SVT_Window.log_filehandler.write("{}\n".format(next_line))

class SVT_Win(wx.Frame):

    """ SVT_Win() is the wx.Frame that holds all of the wx.Panels.
    """

    def __init__(self, *args, **kwargs):

        super(SVT_Win, self).__init__(*args, **kwargs)

        self.SetMinSize((750,650))

        self.icon = wx.Icon("icons/icon.ico", wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon)

        self.panel_button = [0,1,2,3,4]

        self.panel_button[0] = wx.ToggleButton(self, label="Criteria")
        self.panel_button[1] = wx.ToggleButton(self, label="Websites")
        self.panel_button[2] = wx.ToggleButton(self, label="Configuration")
        self.panel_button[3] = wx.ToggleButton(self, label="Advanced Settings")
        self.panel_button[4] = wx.ToggleButton(self, label="Run")

        hbox = wx.BoxSizer()

        for self.add_pbutton in xrange(5):
            hbox.Add(self.panel_button[self.add_pbutton], proportion=1, flag=wx.LEFT, border=5)

        # For some reason when I bind these in a for loop it assigns all four buttons to the last value
        self.panel_button[0].Bind(wx.EVT_TOGGLEBUTTON, lambda show_only: self.onSwitchPanels(0))
        self.panel_button[1].Bind(wx.EVT_TOGGLEBUTTON, lambda show_only: self.onSwitchPanels(1))
        self.panel_button[2].Bind(wx.EVT_TOGGLEBUTTON, lambda show_only: self.onSwitchPanels(2))
        self.panel_button[3].Bind(wx.EVT_TOGGLEBUTTON, lambda show_only: self.onSwitchPanels(3))
        self.panel_button[4].Bind(wx.EVT_TOGGLEBUTTON, self.CheckMinimumInputRequirements)
        
        static_line = wx.StaticLine(self, size=(300,5))

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(hbox, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        vbox.Add(static_line, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)

        self.panel = [0,1,2,3,4]
        self.show_only = 0

        self.panel[0] = Panel_Criteria(self, 0)
        self.panel[1] = Panel_Websites(self, 1)
        self.panel[2] = Panel_Configuration(self, 2)
        self.panel[3] = Panel_Advanced(self, 3)
        self.panel[4] = Panel_Runtime(self, 4)

        self.onSwitchPanels(0)

        hbox_panels = wx.BoxSizer()

        for self.add_panel in xrange(5):
            hbox_panels.Add(self.panel[self.add_panel], proportion=1, flag=wx.EXPAND)
        
        vbox.Add(hbox_panels, proportion=1, flag=wx.EXPAND)

        self.SetSizer(vbox)
        self.Layout()

        self.Centre()
        self.Show()

        self.LoadFromLastConfig(self)

    def onSwitchPanels(self, show_only):

        """ onSwitchPanels(show_only): When one of the panel buttons are clicked, (or if called from CheckMinimumInputRequirements()) hides all panels other than show_only.
        """

        for self.hide_this in xrange(5):
            self.panel[self.hide_this].Hide()
            self.panel_button[self.hide_this].SetValue(False)            

        self.panel_button[4].SetLabel("Run") # During / after the run, the label was set to Runtime Log / Run Again; this resets it when the user switches back to any other panel.

        self.panel[show_only].Show()
        self.panel_button[show_only].SetValue(True)
        self.Layout()

    def CheckMinimumInputRequirements(self, event):

        """ CheckMinimumInputRequirements(): Because runtime can't proceed or give meaningful results unless criteria, websites, and where to save the information are given.
        """
        
        if (self.panel[2].saveresults_checkbox[0].GetValue() == False and self.panel[2].saveresults_checkbox[1].GetValue() == False):
            wx.MessageBox("You must save results to a quick-view spreadsheet, a fully detailed report, or both.", "Pre-Run Check", wx.OK|wx.ICON_INFORMATION)
            self.onSwitchPanels(2)
            return

        if (self.panel[2].saveresults_path.GetValue() == ""):
            self.result = wx.MessageBox("You haven't chosen where to save your results yet. Choose your folder now?", "Pre-Run Check", wx.YES_NO|wx.YES_DEFAULT|wx.ICON_QUESTION)
            if (self.result == 2):
                self.panel[2].choosedir(self)
                self.CheckMinimumInputRequirements(self)
                return
            else:
                self.onSwitchPanels(2)
                return            

        if (self.panel[1].websites_filename.GetValue() == ""):
            self.result = wx.MessageBox("You haven't selected your list of websites to scan yet. Choose your list now?", "Pre-Run Check", wx.YES_NO|wx.YES_DEFAULT|wx.ICON_QUESTION)
            if (self.result == 2): # Yes is 2; No is 8
                self.panel[1].load("load")
                self.CheckMinimumInputRequirements(self)
                return
            else:
                self.onSwitchPanels(1)
                return

        if (self.panel[0].criteria_filename.GetValue() == ""):
            self.result = wx.MessageBox("You haven't selected your list of criteria to use yet. Choose your list now?", "Pre-Run Check", wx.YES_NO|wx.YES_DEFAULT|wx.ICON_QUESTION)
            if (self.result == 2):
                self.panel[0].load("load")
                self.CheckMinimumInputRequirements(self)
                return
            else:
                self.onSwitchPanels(0)
                return

        self.CheckAdvancedInputRequirements(self)

    def CheckAdvancedInputRequirements(self, event):

        """ CheckAdvancedInputRequirements(): Called by CheckMinimumInputRequirements(). Adds additional input quality control checks to minimize need for error handling.
        """

        # TODO: Add more sophisticated checks here, then:
        self.RunWebsiteScanner(self)

    def RunWebsiteScanner(self, event):

        """ RunWebSiteScanner(): Called by CheckAdvancedInputRequirements(). Handles all of the actual running of the program and runtime logging.
        """

        self.onSwitchPanels(4)
        self.panel_button[4].SetLabel("Run Again / Runtime Log")

        for self.x in xrange(5):
            self.panel_button[self.x].Disable() # If there is a runtime error, the buttons to change panels don't get re-enabled (and I'm okay with that because I need to add more error handling)

        self.SaveAsLastConfig(self)

        self.panel[4].folder_path.SetValue(self.panel[2].saveresults_path.GetValue())

        (self.year, self.month, self.day, self.hour, self.minute, self.second, self.x, self.y, self.z) = time.localtime()
        del self.x, self.y, self.z

        self.output_filename = "Scan{}-{}-{}_{}-{}-{}".format(self.year, self.month, self.day, self.hour, self.minute, self.second)

        self.log_filehandler = open(r"{}\{}.log".format(self.panel[4].folder_path.GetValue(), self.output_filename), "w")
        self.panel[4].Append_Log("--------------------------------------------------------------- Run Start [{}-{:0>2d}-{:0>2d} {:0>2d}:{:0>2d}:{:0>2d}] ----------------------------------------------------------------".format(self.year, self.month, self.day, self.hour, self.minute, self.second))

        self.runtime_start = time.time()

        if ((".xls" in self.panel[0].criteria_filename.GetValue()[-4:]) or (".xlsx" in self.panel[0].criteria_filename.GetValue()[-5:])):
            (self.column_list, self.criteria) = GetColumnsFromSpreadsheet(self.panel[0].criteria_filename.GetValue())
        elif (".csv" in self.panel[0].criteria_filename.GetValue()[-4:]):
            (self.column_list, self.criteria) = GetColumnsFromTSV(self.panel[0].criteria_filename.GetValue(), delimiter = ",") 
        elif (".tsv" in self.panel[0].criteria_filename.GetValue()[-4:]):
            (self.column_list, self.criteria) = GetColumnsFromTSV(self.panel[0].criteria_filename.GetValue())

        if (self.panel[0].innocuous_filename.GetValue() == ""):
            self.innocuous_list = []
        else:
            with open(self.panel[0].innocuous_filename.GetValue()) as self.innocuous_file:
                self.innocuous_list = self.innocuous_file.read()
                self.innocuous_list = self.innocuous_list.split("\n")

        self.column_list.sort()
        self.column_list.append("WHOIS data")
        self.column_list.append("Domain Dispute Check")
        self.criteria_score = {}.fromkeys(self.criteria,0)

        with open(self.panel[1].websites_filename.GetValue()) as self.websites_file:
            self.websites = self.websites_file.read()
            self.websites = self.websites.split("\n")

        (self.website_scoring, self.phones_associated, self.website_images, self.depth_samedomain_links_list, self.depth_external_links_list) = ScanPages(self.websites, self.criteria, self.innocuous_list, self.criteria_score, self.panel[2].spin_depth.GetValue())

        if (self.website_scoring != -1): # As long as the run didn't terminate early due to a failed proxy

            if self.panel[2].saveresults_checkbox[0].GetValue() == True: # Simple output (spreadsheet)
                FormatDict(self.website_scoring, self.phones_associated, self.website_images, self.depth_samedomain_links_list, self.depth_external_links_list, r"{}\{}.csv".format(self.panel[4].folder_path.GetValue(), self.output_filename), self.column_list)

            if self.panel[2].saveresults_checkbox[1].GetValue() == True: # Fully detailed report (HTML)
                FormatDict(self.website_scoring, self.phones_associated, self.website_images, self.depth_samedomain_links_list, self.depth_external_links_list, r"{}\{}.html".format(self.panel[4].folder_path.GetValue(), self.output_filename), self.column_list, output_format="html")

            (self.end_year, self.end_month, self.end_day, self.end_hour, self.end_minute, self.end_second, self.x, self.y, self.z) = time.localtime()

            self.elapsed_runtime = time.time() - self.runtime_start

            self.hh = int(self.elapsed_runtime/3600)
            self.mm = int((self.elapsed_runtime - (3600*self.hh))/60)
            self.ss = int(self.elapsed_runtime - ((3600*self.hh)+(60*self.mm)))
            
            self.panel[4].Append_Log("------------------------------------------- Run Completed [{}-{:0>2d}-{:0>2d} {:0>2d}:{:0>2d}:{:0>2d}] (Elapsed runtime: {:0>2d}:{:0>2d}:{:0>2d}) -------------------------------------------".format(self.end_year, self.end_month, self.end_day, self.end_hour, self.end_minute, self.end_second, self.hh, self.mm, self.ss))
            self.log_filehandler.close()

            if self.panel[2].saveresults_checkbox[2].GetValue() == True: # Open when finished with runtime
                if self.panel[2].saveresults_checkbox[0].GetValue() == True: # Simple output (spreadsheet)
                    os.startfile(r"{}\{}".format(self.panel[2].saveresults_path.GetValue(), "{}.csv".format(self.output_filename)))
                if self.panel[2].saveresults_checkbox[1].GetValue() == True: # Fully detailed report (HTML)
                    os.startfile(r"{}\{}".format(self.panel[2].saveresults_path.GetValue(), "{}.html".format(self.output_filename)))

        for self.x in xrange(5):
            self.panel_button[self.x].Enable()

    def LoadFromLastConfig(self, event):

        """ LoadFromLastConfig(): Loads 'last.cfg' saved from SaveAsLastConfig() so users don't have to re-enter details of the most recent run.
        """

        # TODO: Optionally allow user to load from a user-chosen configuration file

        if os.path.exists("last.cfg"):
            self.result = wx.MessageBox("Load last-used settings?\n(You can always change them before runtime)", "Load last-used settings?", wx.YES_NO|wx.YES_DEFAULT|wx.ICON_QUESTION)
            if (self.result == 2):
                with open("last.cfg") as self.last_config_file:
                    self.last_config = self.last_config_file.read()
                    self.last_config = self.last_config.split("\n")
                del self.last_config[-1]

                # Since a string with a value of "False" is a boolean true, so I need to do a little conversion here
                for self.x in xrange(5,8):
                    if (self.last_config[self.x] == "False"):
                        self.last_config[self.x] = False

                if self.last_config[14] == "False":
                    self.last_config[14] = False
                
                self.panel[0].criteria_filename.SetValue(self.last_config[0])
                self.panel[0].innocuous_filename.SetValue(self.last_config[1])
                self.panel[1].websites_filename.SetValue(self.last_config[2])
                self.panel[2].spin_depth.SetValue(int(self.last_config[3]))
                self.panel[2].spin_delay.SetValue(int(self.last_config[4]))
                
                self.panel[2].saveresults_checkbox[0].SetValue(bool(self.last_config[5]))
                self.panel[2].saveresults_checkbox[1].SetValue(bool(self.last_config[6]))
                self.panel[2].saveresults_checkbox[2].SetValue(bool(self.last_config[7]))
                self.panel[2].saveresults_path.SetValue(self.last_config[8])
                self.panel[3].user_agent.SetValue(self.last_config[9])
                self.panel[3].referral_string.SetValue(self.last_config[10])
                self.panel[3].proxy_ip.SetValue(self.last_config[11])
                self.panel[3].proxy_port.SetValue(self.last_config[12])
                self.panel[3].tineye_apikey.SetValue(self.last_config[13])
                self.panel[3].whois_check.SetValue(bool(self.last_config[14]))
                self.panel[3].domaindispute_rightsholders.SetValue(self.last_config[15])

    def SaveAsLastConfig(self, event):

        """ SaveAsLastConfig(): Saves everything configured for runtime as 'last.cfg' in the active directory for use with LoadFromLastConfig()
        """

        # TODO: Optionally allow user to save a configuration file as something other than 'last.cfg' for use later

        with open("last.cfg", "w") as self.last_config_file: # Keep in mind you would be saving the tineye password as plaintext ... consider using the keyring library
            self.last_config = [self.panel[0].criteria_filename.GetValue(), self.panel[0].innocuous_filename.GetValue(), self.panel[1].websites_filename.GetValue(), self.panel[2].spin_depth.GetValue(), self.panel[2].spin_delay.GetValue(), self.panel[2].saveresults_checkbox[0].GetValue(), self.panel[2].saveresults_checkbox[1].GetValue(), self.panel[2].saveresults_checkbox[2].GetValue(), self.panel[2].saveresults_path.GetValue(), self.panel[3].user_agent.GetValue(), self.panel[3].referral_string.GetValue(), self.panel[3].proxy_ip.GetValue(), self.panel[3].proxy_port.GetValue(), self.panel[3].tineye_apikey.GetValue(),  self.panel[3].whois_check.GetValue(), self.panel[3].domaindispute_rightsholders.GetValue()]
            for self.index, self.config_item in enumerate(self.last_config):
                self.last_config[self.index] = "{}\n".format(self.config_item)
            self.last_config_file.writelines(self.last_config) 

def GetColumnsFromSpreadsheet(spreadsheet_filename, de_duplicate = True):

    """ GetColumnsFromSpreadsheet(spreadsheet_filename, de_duplicate = True): Iterates over columns (instead of rows), saving information as header_row and criteria.

            By default, de-duplicates within each column.

            returns: header_row, criteria
    """

    spreadsheet_file = xlrd.open_workbook(spreadsheet_filename)
    spreadsheet_read = spreadsheet_file.sheet_by_index(0)
    spreadsheet_data = {}

    header_row = []

    for col_index in xrange(0, spreadsheet_read.ncols):
        spreadsheet_data[spreadsheet_read.cell(0, col_index).value] = []
        header_row.append(spreadsheet_read.cell(0, col_index).value)

    for row_index in xrange(1, spreadsheet_read.nrows):
        for col_index in xrange(0, spreadsheet_read.ncols):
            try:
                spreadsheet_data[spreadsheet_read.cell(0, col_index).value].append(int(spreadsheet_read.cell(row_index, col_index).value))
            except ValueError:
                spreadsheet_data[spreadsheet_read.cell(0, col_index).value].append(spreadsheet_read.cell(row_index, col_index).value)

        if (de_duplicate == True):
            spreadsheet_data[spreadsheet_read.cell(0, col_index).value] = list(set(spreadsheet_data[spreadsheet_read.cell(0, col_index).value]))

    return (header_row, spreadsheet_data)

def GetColumnsFromTSV(filename, delimiter = "\t", de_duplicate = True):

    """ GetColumnsFromTSV(filename, delimiter = "\t", de_duplicate = True): Iterates over columns (instead of rows), saving information as header_row and criteria.

            By default, tabs are used as the delimiter.
            By default, de-duplicates within each column.

            returns: header_row, criteria
    """

    with open(filename) as spreadsheet_file:

        criteria = {}

        header_row = spreadsheet_file.readline()
        header_row = header_row.replace("\r", "")
        header_row = header_row.replace("\n", "")
        header_row = header_row.split(delimiter)

        for column in header_row:
            criteria[column] = []

        for line in spreadsheet_file.readlines():
            for (column, split_line) in zip(header_row, line.split(delimiter)):
                if (split_line[-1:] == "\n"):
                    split_line = split_line.replace("\n", "")
                if (split_line[-1:] == "\r"):
                    split_line = split_line.replace("\r", "")
                criteria[column].append(split_line)
            if (de_duplicate == True):
                criteria[column] = list(set(criteria[column]))

    return (header_row, criteria)

def FormatDict(dictionary, phones_associated, website_images, depth_samedomain_links_list, depth_external_links_list, output_filename, column_list, open_type = "a", output_format = "csv"):

    """ FormatDict(dictionary, phones_associated, website_images, depth_samedomain_links_list, depth_external_links_list, output_filename, column_list, open_type = "a", output_format = "csv"): Prepares output () to be written in SS_WriteOutput
    """

    csv_headers_written = False
    html_headers_written = False

    if (output_format == "csv") and (csv_headers_written == False):

            with open(output_filename, open_type) as write_output:

                write_output.write(",") # Creates the blank field just above the site name

                for values in column_list:
                    if (values[-1:] == "\n"):
                        values = values.replace("\n", "")
                    if (values[-1:] == "\r"):
                        values = values.replace("\r", "")
                    if 'WHOIS' in values:
                        continue
                    write_output.write("{},".format(values))

                write_output.write('Phone numbers associated with this website,')
                write_output.write('# of same-domain links found on this website,')
                write_output.write('# of external links found on this website')
                    
                write_output.write("\n")

            csv_headers_written = True

    if (output_format == "html") and (html_headers_written == False):

        with open(output_filename, open_type) as write_output:
            # TODO: Format the output like links so they could open them directly.  <a href="file://" ...
            write_output.write("""<html><table style="border-style: solid; border-width:2px; background-color: #dddddd;"><tr><td colspan=2><b>Configuration details for this run</b></td></tr>
<tr><td>Depth:</td><td>{}</td></tr>
<tr><td colspan=2><i>If you've made changes to these files since runtime, future run results may vary.</td></tr>
<tr><td>Criteria file:</td><td>{}</td></tr>
<tr><td>Websites file:</td><td>{}</td></tr>
<tr><td>Rightsholders file:</td><td>{}</td></tr></table>""".format(SVT_Window.panel[2].spin_depth.GetValue(), SVT_Window.panel[0].criteria_filename.GetValue(), SVT_Window.panel[1].websites_filename.GetValue(), SVT_Window.panel[3].domaindispute_rightsholders.GetValue()))

        html_headers_written = True

    if 'Phone numbers associated with this website' not in column_list:
        column_list.append('Phone numbers associated with this website')
        
    if output_format == "csv":
        column_list.append('# of same-domain links found on this website')
        column_list.append('# of external links found on this website')

    if output_format == "html":
        column_list.remove('# of same-domain links found on this website')
        column_list.remove('# of external links found on this website')
        column_list.append('Images found on this website')
        column_list.append('List of same-domain links found on this website')
        column_list.append('List of external links found on this website')
    
    for (website, (((colscore_pairs),(full_details)), whois_data, domaindispute_data)) in dictionary.iteritems():

        output = []
   
        output.append(website)

        for column in column_list:
            try:
                output.append(dictionary[website][0][0][column]) 
            except KeyError:
                if 'WHOIS data' in column:
                    if output_format == "html":
                        output.append(whois_data)
                elif 'Domain Dispute Check' in column: 
                    output.append(''.join(domaindispute_data))
                elif 'Phone numbers associated with this website' in column:
                    output.append('<br>'.join(list(set(phones_associated[website])))) # or do you change this in SS_WriteOutput? # I forget what this comment means - do more testing to determine whether there's a bug here
                elif 'Images found on this website' in column:
                    if output_format == "html":
                        output.append(website_images[website])
                elif ('# of same-domain links found on this website' in column and output_format == "csv"):
                        output.append(len(list(set(flatten(depth_samedomain_links_list[website].values())))))
                elif ('List of same-domain links found on this website' in column and output_format == "html"):
                        output.append(depth_samedomain_links_list[website])
                elif ('# of external links found on this website' in column and output_format == "csv"):
                        output.append(len(list(set(flatten(depth_external_links_list[website].values())))))
                elif ('List of external links found on this website' in column and output_format == "html"):
                        output.append(depth_external_links_list[website])
                else:
                    output.append(0)
    
        SS_WriteOutput(column_list, output, full_details, output_format, output_filename)
        
    return

def SS_WriteOutput(column_list, output, full_details, output_format, output_filename, open_type = "a"):

    """ SS_WriteOutput(column_list, output, full_details, output_format, output_filename, open_type): Writes the details of the page fetches / criteria items found to specified files.

            output_format == 'csv': Quick summary, good for an overview
            output_format == 'html': Full details, gives you everything that was found and where
    """

    with open(output_filename, open_type) as write_output:

        if (output_format == "csv"):
            for value in output:
                if 'Whois' not in str(value):
                    write_output.write("{},".format(value)) # this will add a trailing comma but I can live with that
            write_output.write("\n")
        elif (output_format == "html"):
            try:
                write_output.write("""<br/><table border=1 style="text-align: center; vertical-align:middle;" width=1200><tr style="background-color: #beeeef;"><td colspan=2><b>{}</b></td><td><b>{}</b></td></tr>""".format(output[0], sum(output[1:len(output)-6]))) # Total scorea
            except TypeError, e:
                pass
            for (column, value) in zip(column_list, output[1:]): # [1:] because column_list is actually shifted over one to column to the right when written (for the blank field just above the site name)
                if value != "":
                    if ('WHOIS data' in column) or ('Domain Dispute Check' in column) or ('Phone numbers associated with this website' in column):
                        write_output.write("""<tr><td>{}:</td><td colspan=2>{}</td>""".format(column, value))
                    elif ('Images found on this website' in column):
                        write_output.write("""<tr><td>{}:</td><td colspan=2>{}</td>""".format(column, '<br>'.join(value)))
                    elif ('List of same-domain links found on this website' in column) or ('List of external links found on this website' in column):
                        try:
                            write_output.write("""<tr><td>{}:</td><td colspan=2>{}</td>""".format(column, '<br>'.join(list(set(flatten(value.values()))))))
                        except TypeError, e:
                            pass
                        except UnicodeEncodeError:
                            pass
                    else:
                        write_output.write("""<tr><td>{}:</td><td width=50>{}</td>""".format(column, value))
                    try:
                        
                        criteria_found_details = full_details[column]
                        write_output.write("<td>")
                        for (fulldetails_value, fulldetails_page) in criteria_found_details: 
                            write_output.write("""Found <b>{}</b> on <a href="{}" target="_blank">{}</a><br/>\n""".format(fulldetails_value, fulldetails_page, fulldetails_page))
                    except KeyError:
                        write_output.write("""</tr>""")
                    write_output.write("""</td></tr>""")
            write_output.write("""</table></html>""")                                     
            
    return    

def ScanPages(websites, criteria, innocuous_list, criteria_score, desired_depth):

    """ ScanPages(websites, criteria, innocuous_list, criteria_score, desired_depth): Scans a list of websites for selected criteria, ignoring innocuous items, updates the criteria score accordingly.  Visits pages in the website to desired_depth.

            Will also update the UI runtime progress window on .panel[4]

            returns: website_scoring, phones_associated, website_images, depth_samedomain_links_list, depth_external_links_list
    """

    website_scoring = {}
    fetched_already = []
    
    website_images = {}
    phones_associated = {}
    depth_samedomain_links_list = {}
    depth_external_links_list = {}

    if SVT_Window.panel[3].whois_check.GetValue() == True:
        whois_connection = whoisclient.NICClient()

    if SVT_Window.panel[3].domaindispute_rightsholders.GetValue() != "":
        with open(SVT_Window.panel[3].domaindispute_rightsholders.GetValue()) as domaindispute_rightsholders_file:
            domaindispute_rightsholders = domaindispute_rightsholders_file.read()
            domaindispute_rightsholders = domaindispute_rightsholders.split("\n")

    websites_crawled = 0
    current_depth = 0
    pages_this_depth = 0
    
    for x in xrange(3):
        SVT_Window.panel[4].progress_bar[x].SetValue(0)

    SVT_Window.panel[4].pl_websites_crawled = websites_crawled
    SVT_Window.panel[4].pl_current_depth = current_depth
    SVT_Window.panel[4].pl_pages_this_depth = pages_this_depth

    SVT_Window.panel[4].pl_websites_to_crawl = len(websites)
    SVT_Window.panel[4].progress_bar[0].SetRange(len(websites))
    SVT_Window.panel[4].pl_maximum_depth = desired_depth
    SVT_Window.panel[4].progress_bar[1].SetRange(desired_depth+1)
    UpdateRunProgress()

    for website in websites:

        whois_data = {} 
        domaindispute_data = {} 
        criteria_score = {}.fromkeys(criteria,0)
        full_details = {}

        depth_samedomain_links_list[website] = {}
        depth_external_links_list[website] = {}
        website_images[website] = []
        phones_associated[website] = []

        if (SVT_Window.panel[3].whois_check.GetValue() == True) or (SVT_Window.panel[3].domaindispute_rightsholders.GetValue() != ""):
            if re.match('(https?://)?(w{3}\.)?([\d\w\-\.]+)?/?', website): 
                m = re.match('(https?://)?(w{3}\.)?([\d\w\-\.]+)?/?', website)
                protocol = m.group(1)
                www = m.group(2)
                domain = m.group(3)
        
        if SVT_Window.panel[3].whois_check.GetValue() == True:
            if (SVT_Window.panel[2].spin_delay.GetValue == 0) and (SVT_Window.panel[2].spin_delay.GetValue == 0):
                pass # TODO: change to sleep/idle(2s)
                # KNOWN ISSUE: See below in GetPage() for full details.
                #               This is where the fix needs to be implemented as well so that you don't get banned for slamming the WHOIS servers.
            whois_data[website] = whois_connection.whois_lookup(None, domain, 1)
            SVT_Window.panel[4].Append_Log("[WHOIS] info obtained for {}".format(domain))
        else:
            whois_data[website] = None

        if SVT_Window.panel[3].domaindispute_rightsholders.GetValue() != "":
            if re.match('(.+)?\.', domain):
                m = re.match('(.+)?\.', domain) # For domains containing subdomains such as abc.def.com, this will return abc.def
                domain_nosuffix = m.group(1)
            
            for domaindispute_rightsholder in domaindispute_rightsholders:
                if domaindispute_rightsholder in domain:
                    try:
                        domaindispute_data[website].append(domaindispute_rightsholder) 
                    except KeyError:
                        domaindispute_data[website] = []
                        domaindispute_data[website].append(domaindispute_rightsholder)
                    SVT_Window.panel[4].Append_Log("[WIPO] {} maybe be violating {}'s copyrights by using this domain - potential for WIPO UDND action.".format(website, domaindispute_rightsholder))
                else:
                    domaindispute_data[website] = []
        else:
            domaindispute_data[website] = []

        SVT_Window.panel[4].pl_current_website = website
        UpdateRunProgress()
    
        for current_depth in xrange(desired_depth + 1):
            depth_samedomain_links_list[website][current_depth + 1] = []
            depth_external_links_list[website][current_depth + 1] = []
            
            if (current_depth == 0):
                depth_samedomain_links_list[website][current_depth] = []
                depth_samedomain_links_list[website][current_depth].append(website)

            SVT_Window.panel[4].pl_current_depth = current_depth
            SVT_Window.panel[4].progress_bar[1].SetValue(current_depth+1)
            SVT_Window.panel[4].progress_bar[2].SetValue(0)
            UpdateRunProgress()

            pages_this_depth = 0

            for link in depth_samedomain_links_list[website][current_depth]:
                SVT_Window.panel[4].progress_label[2].SetLabel("{} of {} (I'm [ASLEEP] right now so I might be unresponsive.)".format(SVT_Window.panel[4].pl_pages_this_depth, SVT_Window.panel[4].pl_total_pages_this_depth))
                SVT_Window.panel[4].Update()

                (website_source, fetched_already) = GetPage(link, current_depth, fetched_already)

                if (fetched_already == [-1]): # Code to end run early due to failed proxy
                    return (-1, phones_associated, website_images, depth_samedomain_links_list, depth_external_links_list)

                pages_this_depth += 1
                SVT_Window.panel[4].pl_pages_this_depth = pages_this_depth
                SVT_Window.panel[4].progress_bar[2].SetValue(pages_this_depth+1)
                SVT_Window.panel[4].pl_total_pages_this_depth = len(depth_samedomain_links_list[website][current_depth])
                SVT_Window.panel[4].progress_bar[2].SetRange(len(depth_samedomain_links_list[website][current_depth]))
                SVT_Window.panel[4].progress_bar[2].Update()
                UpdateRunProgress()

                for phone in re.finditer('(\d{3}[)\s\.\-]{1,2}\d{3}[\s\.\-]\d{4})', website_source):
                    phones_associated[website].append(phone.group(1))                    

                website_scoring.update({website: [(ScorePage(website_source, link, criteria, innocuous_list, criteria_score, full_details, current_depth)), whois_data[website], domaindispute_data[website]]}) 
                website_images[website].extend(Collect_HTML_Items(website_source, "img", "src")) 
                (samedomain_links_list, external_links_list) = Separate_Links(website, Collect_HTML_Items(website_source, "a", "href"))

                for index, image in enumerate(website_images[website]):
                    if image[0:2] == "//":
                        website_images[website][index] = "http:" + website_images[website][index]
                    elif image[0] == "/":
                        image_path = link[:link.rfind("/")]
                        if image_path[0:5] == "http:":
                            image_path = link

                        website_images[website][index] = image_path + website_images[website][index]

                depth_samedomain_links_list[website][current_depth + 1].extend(samedomain_links_list)
                depth_external_links_list[website][current_depth + 1].extend(external_links_list)

        websites_crawled += 1
        SVT_Window.panel[4].pl_websites_crawled = websites_crawled
        SVT_Window.panel[4].progress_bar[0].SetValue(websites_crawled)
        UpdateRunProgress()

    SVT_Window.panel[4].progress_bar[2].SetRange(1)
    SVT_Window.panel[4].progress_bar[2].SetValue(1)
                    
    return (website_scoring, phones_associated, website_images, depth_samedomain_links_list, depth_external_links_list)

def UpdateRunProgress():

    """ UpdateRunProgress(): Helper function to update the UI runtime progress window on .panel[4]
    """

    SVT_Window.panel[4].progress_label[0].SetLabel("{} of {} \t(Now on: {})".format(SVT_Window.panel[4].pl_websites_crawled, SVT_Window.panel[4].pl_websites_to_crawl, SVT_Window.panel[4].pl_current_website))
    SVT_Window.panel[4].progress_label[1].SetLabel("{} of {}".format(SVT_Window.panel[4].pl_current_depth, SVT_Window.panel[4].pl_maximum_depth))
    SVT_Window.panel[4].progress_label[2].SetLabel("{} of {}".format(SVT_Window.panel[4].pl_pages_this_depth, SVT_Window.panel[4].pl_total_pages_this_depth))

    SVT_Window.panel[4].Update()

    return

def Collect_HTML_Items(website_source, tag, attr):

    """ Collect_HTML_Items(website_source, tag, attr): Typically used to grab all links in source; is written broadly enough to grab any tag/attribute combo specified.
    """    

    items_list = []

    for item in BeautifulSoup(website_source, parse_only = SoupStrainer(tag)):
        if item.has_key(attr):
            items_list.append(item[attr])

    items_list = list(set(items_list))
    
    return items_list

def Separate_Links(current_website, links_list):

    """ Separate_Links(current_website, links_list): Separates links into external links and same-domain links.

            returns: samedomain_links_list, external_links_list
    """

    samedomain_links_list = []
    external_links_list = []

    if re.match('(https?://)?(w{3}\.)?(.+)?/?', current_website): 
        m = re.match('(https?://)?(w{3}\.)?(.+)?/?', current_website)
        protocol = m.group(1)
        www = m.group(2)
        current_domain = m.group(3)

    for link in links_list:
        if (link[:1] == '#' or 'mailto:' in link or link[-4:] == '.pdf'):
            continue
        if (('http://' in link or 'https://' in link or 'www.' in link) and current_domain not in link):
            external_links_list.append(link)
        elif (('http://' in link or 'https://' in link) and current_domain in link):
            samedomain_links_list.append(link)
        else:
            if (protocol == None):
                protocol = ""
            if (www == None):
                www = ""
            if (link != "" and link[0:11] != 'javascript:'):
                if (link[0] == "/") and (link[0:4] != "/../"):
                    samedomain_links_list.append("{}{}{}{}".format(protocol, www, current_domain, link))
                elif (link[0:4]  == "/../"):
                    samedomain_links_list.append("{}{}{}{}".format(protocol, www, current_domain, link[4:]))
                elif (link[0:3] == "../"):
                    samedomain_links_list.append("{}{}{}{}".format(protocol, www, current_domain, link[3:]))
                else:
                    samedomain_links_list.append("{}{}{}/{}".format(protocol, www, current_domain, link))
            
    return (samedomain_links_list, external_links_list)

def ScorePage(website_source, current_page, criteria, innocuous_list, criteria_score, full_details, current_depth):

    """ ScorePage(website_source, current_page, criteria, innocuous_list, criteria_score, full_details, current_depth): Check website_source for selected criteria (ignoring innocuous items) and update that website's criteria_score accordingly.

            Scores of -1 for a website indicate that the page fetch failed (a status other than 200 returned) on the homepage.

            returns: criteria_score, full_details
    """

    for innocuous_value in innocuous_list:
        website_source = website_source.replace(innocuous_value, "")
    
    for (column, values) in criteria.iteritems():
        for value in values:
            if (((str(value).lower()) in website_source.lower()) and (value != "")):
                SVT_Window.panel[4].Append_Log("\tFound {} ({})".format(value, column))
                try:
                    full_details[column].append((value, current_page))
                except KeyError:
                    full_details[column] = []
                    full_details[column].append((value, current_page))
                criteria_score[column] += 1
            elif (website_source == "" and current_depth == 0): 
                criteria_score[column] = -1 
    return (criteria_score, full_details)

def GetPage(website, current_depth, fetched_already = []):

    """ GetPage(website, current_depth, fetched_already = []): As long as the page has not been fetched (or failed) previously, GetPage will attempt to fetch a page and return the source of the page.

            fetched_already contains a list of all of the pages that have already been fetched (or failed) so that time isn't wasted fetching pages more than once.
            if a proxy has been set in .panel[3], GetPage will attempt to use it; if the fetch fails, GetPage will prompt the user to end the run prematurely or proceed without the proxy.

            On the first depth, the referral string is passed in; on subsequent depths, no referral string is passed in

            returns: website_source, fetched_already
    """

    website_source = ""

    if website not in fetched_already:
        if (SVT_Window.panel[2].spin_delay.GetValue() > 0):
            
            # !IMPORTANT!
            # KNOWN ISSUE: time.sleep() also causes the GUI to be unresponsive.  Runtime will proceed, but it's best not to fiddle with the GUI during the sleep periods because Windows (need to confirm on other platforms)
            #                   thinks the program is Not Responding.  If left alone / not force quit, the program will finish and return to normal with no adverse effects.  But since this is a program designed for the end-user,
            #                   this is a Very Bad Thing.  Even with the caveats.
            # BAND-AID FIX:  realistically, you get nearly identical / good enough results by running with zero depth, in which case you could run with zero sleep/delay time and avoid this entirely.
            #                   BUT this might not be completely feasible; you don't want to get noticed by the WHOIS servers if checking WHOIS on a large batch. (See also ScanPages() above)
            # I know I need to do something with queueing or threading but I'm not sure how to implement this.
            
            time.sleep(SVT_Window.panel[2].spin_delay.GetValue()) # oh, little code, you cause so much trouble
            
        if (SVT_Window.panel[3].proxy_ip.GetValue() != "" and SVT_Window.panel[3].proxy_port.GetValue() != ""):
            try:
                proxy = urllib2.ProxyHandler({'http': "{}:{}".format(SVT_Window.panel[3].proxy_ip.GetValue(), SVT_Window.panel[3].proxy_port.GetValue())})
                opener = urllib2.build_opener(proxy)
                if current_depth == 0:
                    opener.addheaders = [('User-agent', SVT_Window.panel[3].user_agent.GetValue()),('Referrer', SVT_Window.panel[3].referral_string.GetValue())]
                else:
                    opener.addheaders = [('User-agent', SVT_Window.panel[3].user_agent.GetValue())]
                request = opener.open(website)
            except Exception, e:
                opener.close()
                SVT_Window.panel[4].Append_Log("[ERR] PROXY failed! IP: {}, Port: {} Technical Details: {}".format(SVT_Window.panel[3].proxy_ip.GetValue(), SVT_Window.panel[3].proxy_port.GetValue(), e))
                result = wx.MessageBox("I wasn't able to load the proxy you specified!\n\nIP: {}\nPort: {}\nTechnical details: {}\n\nAre you sure you want to continue with this run? Your traffic will NOT be hidden behind a proxy!".format(SVT_Window.panel[3].proxy_ip.GetValue(), SVT_Window.panel[3].proxy_port.GetValue(), e), "Proxy Failed", wx.YES_NO|wx.YES_DEFAULT|wx.ICON_ERROR)
                if (result != 2):
                    wx.MessageBox("In that case, I'm going to stop the run and take you to the Advanced Settings page.  Check to make sure your proxy settings are correct, or if you prefer to scan without a proxy, make sure the settings are blank.", "Proxy Failed; Stopping Run", wx.OK|wx.ICON_INFORMATION)
                    SVT_Window.onSwitchPanels(3)
                    return ("", [-1]) # I'm using this return code to stop the run
                else:
                    SVT_Window.panel[4].Append_Log("[INFO] Continuing the run without using proxy.")
                    opener = urllib2.build_opener()
                    opener.addheaders = [('User-agent', SVT_Window.panel[3].user_agent.GetValue()),('Referrer', SVT_Window.panel[3].referral_string.GetValue())]
        else:
            opener = urllib2.build_opener()
            if current_depth == 0:
                opener.addheaders = [('User-agent', SVT_Window.panel[3].user_agent.GetValue()),('Referrer', SVT_Window.panel[3].referral_string.GetValue())]
            else:
                opener.addheaders = [('User-agent', SVT_Window.panel[3].user_agent.GetValue())]
                
        ## You will arrive here when:
        ##            there is no proxy
        ##            when the proxy works
        ##            when the proxy failed but you chose to continue running
        
        try:
            response = opener.open(website)
            fetched_already.append(website)
        except urllib2.URLError, e:
            fetched_already.append(website)
            if hasattr(e, "reason"):
                SVT_Window.panel[4].Append_Log("[ERR] Fetch failed on {}, {}".format(website, e.reason))
            if hasattr(e, "code"):
                SVT_Window.panel[4].Append_Log("[ERR] Fetch failed on {}, Returned status code of {}".format(website, e.code))
        except UnicodeError, e:
            fetched_already.append(website)
        else:
            website_source = response.read()
            website_source = website_source.replace("\n", " ")
            SVT_Window.panel[4].Append_Log("Now fetching {}".format(website))

    return (website_source, fetched_already)

def flatten(nested):

    """ flatten(nested): Generator to flatten nested lists.
    """

    try:
        try:
            nested + ''
        except TypeError:
            pass
        else:
            raise TypeError
        for sublist in nested:
            for item in flatten(sublist):
                yield item
    except TypeError:
        yield nested

if __name__ == '__main__':

    app = wx.App()
    SVT_Window = SVT_Win(None, title="Scam Scanner version 0.1a", size=(750,650))
    app.MainLoop()
