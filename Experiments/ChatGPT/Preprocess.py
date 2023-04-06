from persist import cache_results


class PreProc:
    def __init__(self, ds_name, data_file, verbose=False):
        self.data_file = data_file
        self.chars = []
        self.text = ""
        cache_name = f"cache/pp_data_{ds_name}"
        self.chars, self.text = cache_results(cache_name, self._load_data, self.data_file)

        if verbose:
            print("character set:", "".join(self.chars))
            print("text length:", len(self.text))

    @staticmethod
    def _load_data(data_file):
        with open(data_file, 'r', encoding="utf-8") as f:
            text = f.read()

        chars = sorted(list(set(text)))
        text = text
        return chars, text
