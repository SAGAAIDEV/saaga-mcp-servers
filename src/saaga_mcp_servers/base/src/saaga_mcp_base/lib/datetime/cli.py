import fire
import asyncio
from saaga_mcp_base.lib.datetime.tools.datetime import get_date


def get_date_wrapper(days_offset: int = 0):
    return asyncio.run(get_date(days_offset=days_offset))


def main():
    fire.Fire(get_date_wrapper)


if __name__ == "__main__":
    main()
