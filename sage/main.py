# Lookup the age of a server banner
# Author: Philip Barwikowski (@philipbarwi)

from burp import IBurpExtender  # Required for all extensions
from burp import IMessageEditorTab  # Used to create custom tabs within the Burp HTTP message editors
from burp import \
    IMessageEditorTabFactory  # Provides rendering or editing of HTTP messages, within within the created tab
from exception_fix import FixBurpExceptions  # Used to make the error messages easier to debug
import sys  # Used to write exceptions for exceptions_fix.py debugging

class BurpExtender(IBurpExtender, IMessageEditorTabFactory):
    ''' Implements IBurpExtender for hook into burp and inherit base classes.
     Implement IMessageEditorTabFactory to access createNewInstance.
    '''

    def registerExtenderCallbacks(self, callbacks):
        # required for debugger: https://github.com/securityMB/burp-exceptions
        sys.stdout = callbacks.getStdout()

        # keep a reference to our callbacks object
        self._callbacks = callbacks

        # obtain an extension helpers object
        # This method is used to obtain an IExtensionHelpers object, which can be used by the extension to perform numerous useful tasks
        self._helpers = callbacks.getHelpers()

        # set our extension name
        callbacks.setExtensionName("Sage")

        # register ourselves as a message editor tab factory
        callbacks.registerMessageEditorTabFactory(self)

        return

    def createNewInstance(self, controller, editable):
        ''' Allows us to create a tab in the http tabs. Returns
        an instance of a class that implements the iMessageEditorTab class
        '''
        return DisplayValues(self, controller, editable)


FixBurpExceptions()


class DisplayValues(IMessageEditorTab):
    ''' Creates a message tab, and controls the logic of which portion
    of the HTTP message is processed.
    '''

    def __init__(self, extender, controller, editable):
        ''' Extender is a instance of IBurpExtender class.
        Controller is a instance of the IMessageController class.
        Editable is boolean value which determines if the text editor is editable.
        '''
        self._txtInput = extender._callbacks.createTextEditor()
        self._extender = extender


    def getUiComponent(self):
        ''' Must be invoked before the editor displays the new HTTP message,
        so that the custom tab can indicate whether it should be enabled for
        that message.
        '''
        return self._txtInput.getComponent()

    def getTabCaption(self):
        ''' Returns the name of the custom tab
        '''
        return "Sage"

    def isEnabled(self, content, isRequest):
        ''' Determines whether a tab shows up on an HTTP message
        '''
        if isRequest:
            # not used, since we will look into the server banner of the response
            return False
        else:
            responseInfo = self._extender._helpers.analyzeResponse(content)
            headers = responseInfo.getHeaders()

            server_header = [header for header in headers if header.find("Server:") != -1]
            if server_header:
                self._server = server_header[0].split()[1:]
                self._server = ' '.join(self._server)

            return True

    def setMessage(self, content, isRequest):
        ''' Shows the message in the tab if not none
        '''
        text = ""
        if self._backend:
            text += "\nBackend: {}".format(self._backend)
        if self._server:
            text += "\nServer: {}".format(self._server)
        self._text = text
        self._txtInput.setText(text)
        return

    def appendMessage(self, message):
        text = self._text + message
        self._text = text
        self._txtInput.setText(text)
        return

FixBurpExceptions()
