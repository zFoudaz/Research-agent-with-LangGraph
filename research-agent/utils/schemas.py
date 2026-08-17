from pydantic import BaseModel, Field

class reviewerSchema(BaseModel):
    need_improve:bool = Field(description="a boolean value whether the research needs improvement or not")
    notes: str | None = Field(description="notes for the student to improve his research")