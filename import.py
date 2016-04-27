"""SoonTM to import commands/points/quotes and such from other bots"""

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtWebKit import *
from lxml import html

class Imports():

    def __init__(self, uri):
        self.app = QApplication(sys.argv)
        QWebPage.__init__(self)
        self.loadFinished.connect(self._loadFinished)
        self.mainFrame().load(QUrl(uri))
        self.app.exec_()

    def __exit__(self):
        pass

    def _loadFinished(self, result):
        self.frame = self.mainFrame()
        self.app.quit()

    def import_nightbot(self):
        url = 'http://pycoders.com/archive/'
        r = Render(url)
        result = r.frame.toHtml()
        #This step is important.Converting QString to Ascii for lxml to process
        archive_links = html.fromstring(str(result.toAscii()))
        print(archive_links)

    def import_moobot(self):
        pass

    def import_deepbot(self):
        pass

    def import_benbot(self):
        pass

    def import_anhkbot(self):
        pass

    def import_scottybot(self):
        pass

    def import_revlobot(self):
        pass
