from beartype.typing import TypedDict, Literal, List

History = List[
    TypedDict("HistoryItem", {"role": Literal["user", "assistant"], "content": str})
]
