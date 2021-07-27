import contextlib

CONFIG_DEFAULTS = {
    'categorical_threshold': 0.2,
    'numeric_categorical_threshold': None,
    'email_inference_regex': r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
}


class Config:
    def __init__(self, default_values):
        self._defaults = default_values
        self._data = default_values.copy()

    def set_option(self, key, value):
        if key not in self._data.keys():
            raise KeyError(f"Invalid option specified: {key}")
        self._data[key] = value

    def get_option(self, key):
        if key not in self._data.keys():
            raise KeyError(f"Invalid option specified: {key}")
        return self._data[key]

    def reset_option(self, key):
        if key not in self._data.keys():
            raise KeyError(f"Invalid option specified: {key}")
        self._data[key] = self._defaults[key]

    @contextlib.contextmanager
    def with_options(self, **options):
        old_options = {k: self.get_option(k) for k in options}

        for k, v in options.items():
            self.set_option(k, v)
        try:
            yield
        finally:
            for k, v in old_options.items():
                self.set_option(k, v)

    def __repr__(self):
        output_string = "Woodwork Global Config Settings\n"
        output_string += "-" * (len(output_string) - 1)
        for key, value in self._data.items():
            output_string += f"\n{key}: {value}"
        return output_string


config = Config(CONFIG_DEFAULTS)
