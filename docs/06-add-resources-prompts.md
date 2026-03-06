# 06 - Resources/Prompts ကို project ထဲမှာဖြည့်တည်ဆောက်ခြင်း

ဒီ project ရဲ့ CLI (`core/cli_chat.py`) က အောက်ပါ API တွေကို အလုပ်လုပ်မယ်လို့မျှော်လင့်ထားပါတယ်—

- **Resources**
  - `docs://documents` → doc IDs list
  - `docs://documents/<doc_id>` → doc content
- **Prompts**
  - `/summarize <doc_id>` (ဥပမာ) → server-defined prompt messages

အခုအချိန်မှာ `mcp_server.py` / `mcp_client.py` မှာ အဲ့ဒီအပိုင်းတွေ TODO ဖြစ်နေသေးပါတယ်။ ဒီ page က “ဒီ project shape မပြောင်းဘဲ” ဖြည့်ရေးနည်းကို guide လုပ်ပါတယ်။

## Part A — Resources ကို Server ဘက်မှာ ထည့်ခြင်း

### Goal

CLI က call လုပ်နေတဲ့ URIs—

- `docs://documents`
- `docs://documents/<doc_id>`

ကို server က resolve လုပ်ပေးနိုင်ရပါမယ်။

### What to implement

FastMCP မှာ resource define လုပ်တဲ့ API က version အလိုက် အနည်းငယ်ကွာနိုင်ပါတယ်။ သင့် environment မှာ `mcp.server.fastmcp` ရဲ့ resource decorator အမည်က မတူနိုင်လို့ **principle ကိုပဲ** သေချာမှတ်ပါ—

- “URI pattern” တစ်ခုကို register လုပ်
- handler က request URI ကိုယူပြီး list/content ကို return ပြန်

#### Recommended resource behaviors

- `docs://documents` ကို read လုပ်ရင် `["deposition.md", "report.pdf", ...]` လို list ပြန်
- `docs://documents/<doc_id>` ကို read လုပ်ရင် `docs[doc_id]` string ပြန်
- doc မတွေ့ရင် error ပြန်

## Part B — Resources ကို Client ဘက်မှာ ဖြည့်ခြင်း

### Goal

`mcp_client.py` ထဲက placeholder method—

- `read_resource(self, uri: str) -> Any`

ကို “session resource API” ကိုခေါ်ပြီး content ကို parse/return လုပ်အောင်ဖြည့်ရပါမယ်။

### Client-side principle

MCP client session မှာ resources ကိုဖတ်တဲ့ method တစ်ခုရှိပြီး (e.g. `session().read_resource(...)` သို့ မျိုးဆက်တူ) result ထဲက content ကိုယူပြီး CLI friendly value ဖြစ်အောင် ပြောင်းပေးရပါမယ်။

ဒီ project ထဲက CLI က ထင်ထားတဲ့ return type—

- `CliChat.list_docs_ids()` က `list[str]` ပြန်လိုတယ်
- `CliChat.get_doc_content(doc_id)` က `str` ပြန်လိုတယ်

ဒါကြောင့် `read_resource()` ထဲမှာ—

- URI `docs://documents` ဖြစ်ရင် list[str] ကို return
- URI `docs://documents/<id>` ဖြစ်ရင် string ကို return

## Part C — Prompts ကို Server ဘက်မှာ ထည့်ခြင်း

### Goal

CLI က `/summarize deposition.md` လို command မျိုးရိုက်ရင်

```python
messages = await self.doc_client.get_prompt(command, {"doc_id": words[1]})
```

ကနေ prompt messages list ကိုရပြီး LLM messages ထဲထည့်နိုင်ရပါမယ်။

### Prompt design recommendation

Prompt က “messages list” ကိုပြန်ပေးတဲ့ template ပါ။ ဥပမာ summarize prompt ဆိုရင်—

- user role message: “ဒီ document ကို တိုတောင်းအောင်အကျဉ်းချုပ်ရေးပါ…”
- (optional) system/assistant role hints

ဒီ project က `convert_prompt_messages_to_llm_messages()` နဲ့ `PromptMessage` ကို `LLMMessage` အဖြစ်ပြောင်းနေတဲ့အတွက် PromptMessage content က text ဖြစ်ရင် အလုပ်လုပ်ပါလိမ့်မယ်။

## Part D — Prompts ကို Client ဘက်မှာ ဖြည့်ခြင်း

Client placeholder methods—

- `list_prompts()`
- `get_prompt(prompt_name, args)`

ကို server session API နဲ့ချိတ်ပြီး prompt definitions/messages ကိုယူပေးရပါမယ်။

## Practical “incremental approach” (မအော်မဟုတ်ပဲ တဖြည်းဖြည်း)

အကြံပြုထားတဲ့ အဆင့်လိုက်လုပ်ပုံ—

- **Step 1**: server မှာ resources ကိုပထမ implement (doc ids + content)
- **Step 2**: client `read_resource()` ကို implement
- **Step 3**: CLI ထဲမှာ `@deposition.md` mention လုပ်ပြီး context ထည့်တာ အလုပ်လုပ်/မလုပ် စစ်
- **Step 4**: server prompts (summarize) တစ်ခု implement
- **Step 5**: client `list_prompts()` / `get_prompt()` implement
- **Step 6**: `/summarize deposition.md` command အလုပ်လုပ်/မလုပ် စစ်

## Troubleshooting hints (ဒီ project နဲ့ဆိုင်တာ)

- `@doc_id` mention လုပ်တာ မအလုပ်လုပ်ရင်—
  - `docs://documents` resource က list ပြန်မပြန်
  - list ထဲက ids နဲ့ mention strings တိုက်ဆိုင်/မတိုက်ဆိုင်
- `/command` completion မပေါ်ရင်—
  - `list_prompts()` မှာ prompt list ပြန်မပြန်
  - CLI initialize လုပ်တဲ့အချိန် `refresh_prompts()` error မရှိ/ရှိ

Page 07 မှာ run/testing/debugging ကို စနစ်တကျ စစ်ဆေးနည်းတွေကိုဆက်ရေးထားပါတယ်။

