from dataclasses import dataclass, asdict, fields
from typing import Dict, List

class SuperDC():
    def to_dict(self) -> Dict:
        return asdict(self)
    @classmethod
    def from_dict(cls, dict_):
        class_fields = {f.name for f in fields(cls)}
        return cls(**{k: v for k, v in dict_.items() if k in class_fields}) 

@dataclass
class Tag(SuperDC):
    name: str = ""
    _id:str = ""

@dataclass
class Quote(SuperDC):
    author: str = ""
    content: str = ""
    tags: List[str] = ""
    _id:str = "" # a unique id for this quote
    
@dataclass
class Author(SuperDC):
    name: str = ""
    bio:str = ""
    description:str = ""
    link: str = ""
    slug:str = ""
    _id:str = ""

def main():
    q1 = Quote(author="Abraham Lincoln", content="Four score and seven years ago...", tags=["war"])
    print(q1)

    a1 = Author(name="Abraham Lincoln", bio="Test", description="Blah")
    print(a1)

    t1 = Tag("war")
    print(t1)

if __name__ == "__main__":
    main()