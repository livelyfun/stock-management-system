from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Chunk:
    content: str
    embed_text: str
    source: str
    document_title: str
    heading_path: str
    section: str
    chunk_index: int
    total_chunks: int
    line_start: int
    line_end: int


@dataclass
class _Section:
    heading_path: list[str]
    level: int
    lines: list[tuple[int, str]]
    line_start: int
    line_end: int


def _is_separator(line: str) -> bool:
    stripped = line.strip()
    return stripped in {"---", "***", "___"}


def _parse_sections(
    content: str,
) -> tuple[str, list[_Section]]:
    """Parse Markdown into title plus sections with full heading paths."""
    document_title = ""
    stack: list[tuple[int, str]] = []
    sections: list[_Section] = []
    buffer: list[tuple[int, str]] = []
    buffer_start = 1

    def current_path() -> list[str]:
        return [text for (_level, text) in stack]

    def flush_buffer(end_line: int) -> None:
        nonlocal buffer, buffer_start

        body = [
            (line_no, text)
            for line_no, text in buffer
            if text.strip() and not _is_separator(text)
        ]

        if body:
            sections.append(
                _Section(
                    heading_path=current_path(),
                    level=stack[-1][0] if stack else 0,
                    lines=body,
                    line_start=buffer_start,
                    line_end=end_line,
                )
            )

        buffer = []

    for index, raw_line in enumerate(
        content.splitlines(),
        start=1,
    ):
        stripped = raw_line.strip()

        if stripped.startswith("#"):
            flush_buffer(index - 1)

            level = len(raw_line) - len(raw_line.lstrip("#"))
            heading_text = raw_line.lstrip("#").strip()

            while stack and stack[-1][0] >= level:
                stack.pop()

            stack.append((level, heading_text))

            if level == 1 and not document_title:
                document_title = heading_text

            buffer_start = index
        else:
            buffer.append((index, raw_line))

    flush_buffer(len(content.splitlines()))

    return document_title, sections


def _group_sections(
    sections: list[_Section],
    chunk_size: int,
    standalone_threshold: int,
) -> list[list[_Section]]:
    """
    Pack consecutive sections that share a parent into reading-order groups.

    Sections that are large on their own stay standalone so their
    topic is not diluted by merging with neighbours.
    """
    groups: list[list[_Section]] = []
    current: list[_Section] = []
    current_size = 0

    for section in sections:
        section_size = sum(len(text) for _line, text in section.lines)
        parent = section.heading_path[:-1]

        if section_size >= standalone_threshold:
            if current:
                groups.append(current)
                current = []
                current_size = 0

            groups.append([section])
            continue

        if current:
            current_parent = current[0].heading_path[:-1]

            if (
                parent != current_parent
                or (current_size + section_size) > chunk_size
            ):
                groups.append(current)
                current = []
                current_size = 0

        current.append(section)
        current_size += section_size

    if current:
        groups.append(current)

    return groups


def _group_heading_path(
    group: list[_Section],
    document_title: str,
) -> str:
    if len(group) == 1:
        return " > ".join(group[0].heading_path)

    common = group[0].heading_path[:-1]

    return " > ".join(common) or document_title


def _build_items(
    group: list[_Section],
) -> list[tuple[int, str]]:
    """Flatten a section group into (line_no, text) items for citation."""
    items: list[tuple[int, str]] = []

    for section in group:
        # Keep the leaf heading label so merged subsections stay
        # identifiable in both display content and the embed text.
        if len(section.heading_path) > 1:
            items.append(
                (
                    section.line_start,
                    section.heading_path[-1],
                )
            )

        for line_no, text in section.lines:
            items.append((line_no, text))

    return items


def _slice_items(
    items: list[tuple[int, str]],
    chunk_size: int,
    overlap: int,
    min_chunk_size: int,
) -> list[tuple[list[tuple[int, str]], int, int]]:
    """Split items into chunks by character size without cutting lines."""
    if not items:
        return []

    text = "\n".join(line_item for _line_no, line_item in items)

    # Offsets map a character position back to a source line number.
    offsets = [0]
    for _line_no, line_item in items:
        offsets.append(offsets[-1] + len(line_item) + 1)

    def line_number(char_pos: int) -> int:
        index = 0
        while index < len(offsets) - 1 and offsets[index + 1] <= char_pos:
            index += 1
        return items[index][0]

    result: list[tuple[list[tuple[int, str]], int, int]] = []

    start = 0
    total = len(text)

    while start < total:
        end = min(start + chunk_size, total)

        if end < total:
            newline = text.find("\n", end)
            if newline != -1:
                end = newline

        slice_text = text[start:end].strip()

        if len(slice_text) >= min_chunk_size:
            chunk_items = _line_items_from_slice(items, text, start, end)
            result.append(
                (
                    chunk_items,
                    line_number(start),
                    line_number(max(end - 1, start)),
                )
            )

        if end >= total:
            break

        previous_start = start
        start = max(end - overlap, 0)

        if start <= previous_start:
            start = previous_start + 1

        if start >= total:
            break

    return result


def _line_items_from_slice(
    items: list[tuple[int, str]],
    text: str,
    start: int,
    end: int,
) -> list[tuple[int, str]]:
    """Return the original items that overlap the given character range."""
    slice_text = text[start:end]

    cursor = 0
    result: list[tuple[int, str]] = []

    for line_no, line in items:
        line_end = cursor + len(line)
        overlaps = line_end > start and cursor < end
        if overlaps:
            result.append((line_no, line))
        cursor = line_end + 1

    return result


def chunk_markdown(
    content: str,
    source: str,
    chunk_size: int = 1200,
    overlap: int = 200,
    min_chunk_size: int = 40,
) -> list[Chunk]:
    document_title, sections = _parse_sections(content)

    if not sections:
        return []

    chunks: list[Chunk] = []

    standalone_threshold = max(int(chunk_size * 0.4), min_chunk_size)

    for group in _group_sections(
        sections,
        chunk_size,
        standalone_threshold,
    ):
        heading_path = _group_heading_path(group, document_title)
        items = _build_items(group)

        for item_slice, line_start, line_end in _slice_items(
            items,
            chunk_size,
            overlap,
            min_chunk_size,
        ):
            body = "\n".join(text for _line_no, text in item_slice).strip()

            if not body:
                continue

            embed_text = f"{heading_path}\n\n{body}"

            chunks.append(
                Chunk(
                    content=body,
                    embed_text=embed_text,
                    source=source,
                    document_title=document_title,
                    heading_path=heading_path,
                    section=heading_path.split(" > ")[-1],
                    chunk_index=0,
                    total_chunks=0,
                    line_start=line_start,
                    line_end=line_end,
                )
            )

    total = len(chunks)

    for index, chunk in enumerate(chunks):
        chunk.chunk_index = index
        chunk.total_chunks = total

    return chunks