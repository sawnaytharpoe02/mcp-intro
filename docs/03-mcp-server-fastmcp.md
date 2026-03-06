# 03 - MCP Server (FastMCP) ကိုနားလည်ခြင်း

ဒီ project ထဲက MCP server က `mcp_server.py` ပါ။ FastMCP wrapper ကိုသုံးပြီး tools ကို decorator နဲ့ register လုပ်ထားပါတယ်။

## `FastMCP` ဆိုတာ

`mcp.server.fastmcp.FastMCP` က MCP server တစ်ခုကို “tool/resource/prompt” register လုပ်ဖို့ လွယ်ကူအောင် API ပေးတဲ့ helper ပါ။

ဒီ project မှာ server ကို ဒီလိုတည်ဆောက်ထားပါတယ်—

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("DocumentMCP", log_level="ERROR")
```

- `"DocumentMCP"` က server name
- `log_level="ERROR"` က log ကိုလျှော့ချထားတာ

## ဒီ server က manage လုပ်တဲ့ data

`docs` ဆိုတဲ့ dict တစ်ခုထဲမှာ “document id → document contents” ကို in-memory အနေနဲ့ ထားထားပါတယ်။

```python
docs = {
  "deposition.md": "...",
  "report.pdf": "...",
  # ...
}
```

အရေးကြီးတာက—

- ဒီ project မှာ **file I/O မလုပ်သေး**ပါ (အခုက sample data)
- ဒါကိုတိုးချဲ့ပြီး disk/database ထဲက data ကိုဖတ်/ရေး လုပ်နိုင်ပါတယ်

## Tool register လုပ်ပုံ (Decorator pattern)

FastMCP မှာ tool တစ်ခု register လုပ်ဖို့ `@mcp.tool(...)` ကိုသုံးပါတယ်။

### Tool 1: `read_doc_contents`

```python
@mcp.tool(
    name="read_doc_contents",
    description="Reads the contents of a document and return it as a string",
)
def read_document(doc_id: str = Field(description="The ID of the document to read")):
    if doc_id not in docs:
        raise ValueError(f"Document with ID {doc_id} not found in the list")
    return docs[doc_id]
```

**ဘာတွေကိုလေ့လာရမလဲ**

- **Tool name**: `read_doc_contents` (client/LLM က ဒီ name နဲ့ခေါ်မယ်)
- **Input schema**: `doc_id: str` + pydantic `Field(description=...)`
- **Error handling**: doc မတွေ့ရင် `ValueError` throw လုပ်ပြီး client မှာ error result ဖြစ်လာမယ်

### Tool 2: `edit_document`

```python
@mcp.tool(
    name="edit_document",
    description="Edit a document by replacing a string in the document contents with another string",
)
def edit_document(doc_id: str, old_string: str, new_string: str):
    if doc_id not in docs:
        raise ValueError(f"Document with ID {doc_id} not found in the list")
    docs[doc_id] = docs[doc_id].replace(old_string, new_string)
```

**သင်ခန်းစာ**

- Tool အနေနဲ့ “stateful update” လုပ်နိုင်ပါတယ် (ဒီမှာ in-memory dict ကို update)
- ထိန်းချုပ်ချင်ရင် old_string မတွေ့တဲ့အခါ error throw လုပ်ခြင်း/ diff return လုပ်ခြင်း စတာတွေတိုးချဲ့နိုင်ပါတယ်

## Server ကို run လုပ်ပုံ (STDIO transport)

`mcp_server.py` အဆုံးမှာ—

```python
if __name__ == "__main__":
    mcp.run(transport="stdio")
```

**STDIO transport** ဆိုတာ server ကို subprocess အဖြစ် run လုပ်ပြီး stdin/stdout ကနေ request/response message တွေလွှဲပြောင်းတဲ့နည်းပါ။

ဒီ project ရဲ့ `mcp_client.py` က လည်း ဒီ transport နဲ့ကိုက်ညီအောင် `stdio_client(...)` ကိုသုံးထားပါတယ်။

## Server-side TODOs (Project မှာမပြီးသေးတာ)

`mcp_server.py` မှာ comment TODO တွေပါထားပါတယ်—

- resources: `docs://documents` / `docs://documents/<id>` ကို provide လုပ်ရန်
- prompts: `/summarize` `/rewrite_markdown` စတဲ့ command prompts define လုပ်ရန်

အဲ့ဒါတွေကို **Page 06** မှာ ဒီ project flow နဲ့ကိုက်အောင် ဘယ်လို implement လုပ်မလဲကို ဆက်ရှင်းပါတယ်။

