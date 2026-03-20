from pathlib import Path
from typing import ClassVar

from pydantic import BaseModel, ConfigDict, Field


class CheckRunAnnotation(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(strict=True)
    path: str
    start_line: int
    annotation_level: str
    message: str
    title: str | None = None
    blob_href: str | None = None


class CheckRun(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(strict=True)
    id: int
    name: str
    status: str
    conclusion: str | None = None
    details_url: str | None = None
    annotations: list[CheckRunAnnotation] = Field(default_factory=list)


class PRRef(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(strict=True)
    repo: str
    number: int
    url: str | None = None
    title: str | None = None
    state: str | None = None


class Comment(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(strict=True)
    id: int
    body: str
    author: str
    is_resolved: bool
    created_at: str | None = None
    type: str = "comment"


class UnresolvedIssue(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(strict=True)
    author: str
    body: str


class SummarizeInput(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(strict=True)
    pr_url: str
    output_file: Path | None = None


class IssuesInput(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(strict=True)
    pr_url: str
    output_file: Path | None = None


class ListInput(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(strict=True)
    repo: str | None = None
    output_file: Path | None = None


class ResolveInput(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(strict=True)
    comment_id: str
    justification: str
    repo: str | None = None
