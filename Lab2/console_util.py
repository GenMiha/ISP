import converter
import configparser
import argparse
import logging

logging.basicConfig(
    level=logging.WARNING, filename="warning.log", format="%(levelname)s: %(message)s"
)

def main():
    try:
        parser = argparse.ArgumentParser(
            description="Serializer", fromfile_prefix_chars="@"
        )

        parser.add_argument(
            "-c", "--config", dest="config_file", help="Path for the configuration file"
        )

        parser.add_argument(
            "input_path", metavar="input_path", type=str, help="Path to the converted file"
        )

        parser.add_argument(
            "-il",
            "--in_lang",
            metavar="input_language",
            choices=["json", "yaml", "pickle", "toml"],
            default="json",
            type=str,
            help="Override language for input file",
        )

        parser.add_argument(
            "-ol",
            "--out_lang",
            metavar="output_language",
            choices=["json", "yaml", "pickle", "toml"],
            default="json",
            type=str,
            help="Override language for output file",
        )

        parser.add_argument(
            "output_path",
            metavar="output_path",
            type=str,
            help="Path to the file to be converted",
        )

        args = parser.parse_args()
        converter.file_converter(**vars(args))
    except Exception as ex:
        logging.warning(f"Warning: {ex}")



