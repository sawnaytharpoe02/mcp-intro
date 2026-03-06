# 01 - MCP မိတ်ဆက် (Model Context Protocol)

## MCP ဆိုတာဘာလဲ

**MCP (Model Context Protocol)** က AI model (LLM) တစ်ခုကို “အပြင်က tools/resources/prompt templates” တွေနဲ့ စံသတ်မှတ်ထားတဲ့ပုံစံနဲ့ ချိတ်ဆက်ပေးတဲ့ protocol တစ်ခုပါ။

ဒီ project ထဲမှာ MCP ကို ဒီလိုအသုံးချထားပါတယ်—

- MCP **Server** က “tools/resources/prompts” ကို expose လုပ်တယ်
- MCP **Client** က server ကို transport တစ်ခု (ဒီ project မှာ `stdio`) နဲ့ချိတ်ပြီး
  - tool list လုပ်မယ်
  - tool call လုပ်မယ်
  - resource read / prompt get လုပ်မယ် (project မှာ TODO ရှိ)
- CLI chat က user input ကိုယူပြီး LLM ကိုခေါ်၊ LLM က tool call တောင်းဆိုရင် MCP tools ကို run ပေးပြီး result ကို LLM ဆီပြန်ပို့တယ်

## MCP မှာ အဓိက concept ၄ခု

### 1) Tools

Tool ဆိုတာ “Function တစ်ခုကို API လို expose” လုပ်ထားတာပါ။ LLM/Client က tool name + input schema အတိုင်း arguments ပေးပြီး ခေါ်နိုင်ပါတယ်။

ဒီ project ထဲက server tools ဥပမာ—

- `read_doc_contents(doc_id: str) -> str`
- `edit_document(doc_id: str, old_string: str, new_string: str) -> None`

### 2) Resources

Resource ဆိုတာ “URI နဲ့ address လုပ်လို့ရတဲ့ data” ပါ။ ဥပမာ `docs://documents` လို URI တစ်ခုကို read လုပ်ပြီး doc list ကိုရနိုင်တယ်။

ဒီ project ထဲမှာ CLI က resource pattern ကို သုံးဖို့ရေးထားပြီးသားပါ—

- `docs://documents` → doc IDs list
- `docs://documents/<doc_id>` → doc content

ဒါပေမယ့် **server ဘက် resource implementation က TODO** ဖြစ်နေသေးပါတယ်။ (Page 06 မှာ ဖြည့်တည်ဆောက်ပုံရှိ)

### 3) Prompts

Prompt ဆိုတာ “command လို ပြောလို့ရတဲ့ template messages” ပါ။ ဥပမာ `/summarize deposition.md` လို command က server-defined prompt template ကိုယူပြီး LLM ကိုပို့သုံးနိုင်တယ်။

ဒီ project မှာ CLI က `/command` ကို prompt အဖြစ်ယူဖို့ flow ရှိပြီးသားပေမယ့် **client/server prompt API က TODO** ဖြစ်နေသေးပါတယ်။

### 4) Transports

Transport ဆိုတာ “Client ↔ Server ဆက်သွယ်ရေး channel” ပါ။ MCP မှာ အသုံးများတာတွေ—

- `stdio` (ဒီ project သုံးထားတဲ့ transport): server ကို subprocess အဖြစ် run လုပ်ပြီး stdin/stdout နဲ့ JSON-RPC လို message ပို့ကြတယ်
- HTTP/SSE/WebSocket စတာတွေ (project မပါ)

## ဒီ project နဲ့ အမြန် mental model တစ်ခုပြုလုပ်မယ်

- **Server (`mcp_server.py`)**: FastMCP နဲ့ tools register လုပ်ထားတယ် → `mcp.run(transport="stdio")`
- **Client (`mcp_client.py`)**: server process ကို spawn လုပ်ပြီး `ClientSession` တစ်ခုဖွင့်တယ် → `initialize()` လုပ်တယ် → tools list/call လုပ်နိုင်တယ်
- **CLI (`main.py` + `core/*`)**: user input → LLM chat → tool calls → MCP clients က tool 실행 → tool results ကို LLM ဆီပြန်ပို့ → final answer print

## Mermaid diagram (High-level mental model)

```mermaid
flowchart LR
  U[User] -->|type query| CLI[CLI App\n(main.py + core/*)]
  CLI -->|chat + tool schema| LLM[LLM Provider\n(OpenRouter/OpenAI compatible)]
  LLM -->|tool calls| CLI
  CLI -->|list_tools / call_tool| C[MCPClient\n(mcp_client.py)]
  C -->|stdio| S[MCP Server\n(mcp_server.py)]
  S -->|tool result| C -->|result| CLI -->|final answer| U
```

နောက်စာမျက်နှာမှာ ဒီ project architecture ကို diagram/flow အနေနဲ့ရှင်းမယ်။

