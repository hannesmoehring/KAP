class Parser():
    def __init__(self, mapping, columns, case_sensitive=False):
        self.case_sensitive = case_sensitive
        self.columns = columns

        if not case_sensitive:
            self.mapping = dict([(k.lower(), v) for k, v in mapping.items()])
        else:
            self.mapping = mapping

    def _parse(self, s):

        if type(s) != str:
            return None
        
        s = s.lower() if not self.case_sensitive else s
        return self.mapping.get(s, None)


    def parse_columns(self, df):
        for column in self.columns:
            df[column] = df[column].apply(self._parse)