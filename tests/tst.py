from typing import Generator, Iterable, Callable, Any
from dataclasses import dataclass
from enum import StrEnum, auto
from functools import reduce
import this


class LogLevel(StrEnum):
    INFO = auto()
    WARNING = auto()
    ERROR = auto()

@dataclass(slots=True, frozen=True)
class LogRecord:
    level: LogLevel
    message: str

def read_logs() -> Generator[str, None, None]:
    lines = [
        'info User logged in',
        'warning Slow database query',
        'error Payment failed'
    ]
    for line in lines:
        print(f'Producing: {line}')
        yield line

def parse_logs(lines: Iterable[str]) -> Generator[LogRecord, None, None]:
    for line in lines:
        level_text, message = line.split(' ', maxsplit=1)
        level = LogLevel(level_text)
        yield LogRecord(level, message)

def handle_records(records: Iterable[LogRecord]) -> None:
    for record in records:
        print(f'handling: {record}')

type PipelineStage = Callable[[Iterable[Any]], Iterable[Any]]

def compose(*stages: PipelineStage) -> PipelineStage:
    def apply(data: Iterable[Any]) -> Iterable[Any]:
        return reduce(lambda acc, stage: stage(acc), stages, data)
    return apply


def main():
    pipeline = compose(
        parse_logs,
        handle_records,

    )
    records = pipeline(read_logs())
    handle_records(records)

if __name__ == '__main__':
    main()
