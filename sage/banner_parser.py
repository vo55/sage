class BannerParser:
    def __init__(self, http_response_header):
        """
        Parses the server banner from a http response header
        :param http_response_header: List[String] http response header
        """
        try:
            self._server, self._version = self._parse_banner(http_response_header)
        except BannerNotFound as  _:
            self._server, self._version = None, None

    @staticmethod
    def _parse_banner(http_response_header):
        """

        :param http_response_header: List[String] http response header
        :return: (String, String) server, version
        """
        server_header = [header for header in http_response_header if header.find("Server:") != -1]
        if server_header:
            server_header = server_header[0].split()[1:]
            server_header = ' '.join(server_header).split('/') # todo that join is probably not necessary, redesign
            return server_header[0], server_header[1]
        raise BannerNotFound('No "Server" header in http response')

    def get_server(self):
        return self._server

    def get_version(self):
        return self._version

class BannerNotFound(Exception):
    """
    Used if there is not banner found
    """
    pass
