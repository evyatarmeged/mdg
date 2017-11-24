import json


PRINT = 'print '  # Space intentional
EQ = '='
SEMI_COLON = ';'
COMMA = ','
EOL = '\n'


class AWKDataGenerator:
    def __init__(self):
        with open('data_generation/awk.json', 'r') as file:
            self.awk_config = json.loads(file.read())
            self.commands = self.awk_config['commands']
            self.constants = self.awk_config['constants']

    def __str__(self):
        return "AWK files generator"

    def _get_awk_cmd(self, data_type, header):
        """
        Return AWK command for files type, else header if not is self.commands
        :param post_data: POST request files
        :param header: CSV column header
        """
        return self.commands.get(data_type, header)

    def _python_loop_statement(self, num_rows):
        """Return python loop statement formatted with number of rows"""
        return self.constants['python_loop'].format(num_rows)

    def _awk_command_body(self, post_data, headers):
        """
        Return the awk files generating command for each header.
        :param post_data: POST request files
        :param headers: CSV column headers
        """
        return (SEMI_COLON + EOL).join(header + EQ + self._get_awk_cmd(post_data.get(header), header)
                                       for header in headers) + SEMI_COLON

    @staticmethod
    def _print_statement(headers):
        """Return AWK print statement for headers"""
        return PRINT + COMMA.join(headers)

    def _close_statement(self, filename, ofmt=None):
        """
        Return string of AWK close_statement, decimal digit amount, and append to file
        :param filename: Filename
        :param ofs: User specified close_statement. Defaults to comma
        :param ofmt: User specified decimal digit amount. Defaults to None.
        """
        close_statement = self.constants['delimiter'].format(COMMA)  # AWK close_statement
        if ofmt:
            # If there's a float files type, concat number of decimal digits
            close_statement += self.constants['decimal_count'].format(ofmt)
        return close_statement + self.constants['append_file'].format(filename)

    def create_awk_statement(self, post_data, headers, num_rows, filename):
        """Create full awk command"""
        return EOL.join((self._python_loop_statement(num_rows),
                         self.constants['awk_cmd_string'] % (self._awk_command_body(post_data, headers) +
                         self._print_statement(headers)))) + self._close_statement(filename)
