# 08 - Next Steps (ကိုယ်တိုင် MCP server/client တည်ဆောက်ရန်)

ဒီ project ကိုသေချာဖတ်ပြီးပြီဆိုရင် ကိုယ်တိုင် MCP server/client ကို အောက်က pattern နဲ့စလုပ်နိုင်ပါတယ်။

## A) MCP server တစ်ခုကို from-scratch လုပ်မယ်ဆိုရင်

- **Data model ကိုရွေး**: in-memory dict / filesystem / database / third-party API
- **Expose လုပ်မယ့် surface ကိုရွေး**:
  - tool (action) — “ဖတ်/ရေး/တွက်/ရှာ” လို operations
  - resources (addressable data) — “URI နဲ့ဖတ်”
  - prompts (templates) — “command တစ်ခုနဲ့ message set”
- **Transport ကိုရွေး**:
  - local development: `stdio`
  - production service: HTTP/SSE/WebSocket (လိုအပ်ချက်ပေါ်မူတည်)

ဒီ project က local-first (`stdio`) pattern ကို ကောင်းကောင်းပြထားပါတယ်။

## B) MCP client တစ်ခုကို from-scratch လုပ်မယ်ဆိုရင်

- connect lifecycle ကို `async with` သို့ `AsyncExitStack` နဲ့ clean-up ထိန်း
- feature set ကို layer ခွဲ
  - low-level session (initialize/list_tools/call_tool/read_resource/get_prompt)
  - app-specific wrapper (doc client, github client, etc.)

## C) ဒီ project ကို “learning lab” အဖြစ်တိုးချဲ့ရန် idea များ

- **Server**
  - `docs` ကို dict မဟုတ်ဘဲ `docs/` folder ထဲက file တွေကနေ load လုပ်
  - `edit_document` ကို “diff + validation” ပြန်တဲ့ tool အဖြစ် upgrade လုပ်
  - resources + prompts ကို အပြည့်အစုံ implement (Page 06)
- **Client**
  - error types ကို categorize (connection error / protocol error / tool error)
  - tracing/logging ထည့်ပြီး debugging လွယ်ကူအောင်လုပ်
- **CLI**
  - `/help` command
  - tool list/inspect commands (e.g. `/tools`, `/resources`)

## D) Best practice (confidence မြန်မြန်တက်စေမယ့်)

- tool တစ်ခုချင်းစီကို “input schema + sample calls + expected outputs” နဲ့ test cases လေးလုပ်
- “resource URIs” ကို consistent naming convention တစ်ခုထား
- prompt names ကို CLI friendly (`summarize`, `rewrite_markdown`) ထား

