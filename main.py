import logging
import colorama
import sys

# Logging INIT

FORMAT = "[{levelname:^7}] {name}.{threadName}.{module}.{funcName}.{lineno}: {message}"
FORMAT = "{asctime} [{threadName}] |{levelname}| in {filename}/{module}/{funcName} Line {lineno}: {message}"
FORMATS = {
    logging.DEBUG: colorama.Fore.BLUE + FORMAT + colorama.Fore.RESET,
    logging.INFO:  colorama.Fore.GREEN + FORMAT + colorama.Fore.RESET,
    logging.WARNING: colorama.Fore.YELLOW + FORMAT + colorama.Fore.RESET,
    logging.ERROR: colorama.Fore.LIGHTRED_EX + FORMAT + colorama.Fore.RESET,
    logging.CRITICAL: colorama.Fore.RED + FORMAT + colorama.Fore.RESET,
}

class Format(logging.Formatter):
    def format(self, record):
        log_fmt = FORMATS[record.levelno]
        #a = record.levelname+(" "*(9-len(record.levelname)))
        #log_fmt = log_fmt.replace("{levelname}", a)
        if record.funcName == "<module>":
            # record.funcName = "global"
            log_fmt = log_fmt.replace("/{funcName}", "")
        formatter = logging.Formatter(log_fmt, style="{")
        return formatter.format(record)
    
handler = logging.StreamHandler()
handler.setFormatter(Format())

if "-debug" in sys.argv:
    debug_level = sys.argv[sys.argv.index("-debug") + 1]
    if debug_level in ["0","1","2","3","4"]:
        logging.basicConfig(
            level = int(debug_level),
            handlers=[handler]
        )
        levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        print(f"Debug Level {levels[int(debug_level)]}")
    else:
        print("Invalid Debug Level {debug_level}. Defaulting to INFO")
        logging.basicConfig(
            level = logging.INFO,
            handlers=[handler]
        )
else:
        print("Degub Level: INFO")
        logging.basicConfig(
            level = logging.INFO,
            handlers=[handler]
        )


if "-colors" in sys.argv:
    logging.debug("Test running with arg -colors")
    logging.info("Test running with arg -colors")
    logging.warning("Test running with arg -colors")
    logging.error("Test running with arg -colors")
    logging.critical("Test running with arg -colors")
    exit()
elif "-server" in sys.argv:
    import Server
elif "-listen" in sys.argv:
    import Utils.passconn
else:
    logging.critical("\n-colors, -server, or -listen not provided.\nWHAT DO I DO!\nI guess i will exit.\nUse -server to run server next time.")