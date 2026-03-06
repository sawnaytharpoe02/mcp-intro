# 07 - Run/Testing/Debugging

ဒီ page က “ဒီ project ကို run လုပ်နည်း” နဲ့ “MCP server/client integration ကို ဘယ်လိုစစ်မလဲ” ကို တိုတောင်းပြီးလက်တွေ့ကျတဲ့ checklist ပုံစံနဲ့ပေးထားပါတယ်။

## 1) Environment variables (.env)

`main.py` က အောက်က env variables ၂ခုမရှိရင် assert နဲ့ရပ်သွားပါလိမ့်မယ်—

- `LLM_MODEL`
- `LLM_API_KEY`

Optional:

- `USE_UV=1` ထားရင် MCP server ကို `uv run mcp_server.py` နဲ့ spawn လုပ်မယ်
- မထားရင် `python mcp_server.py` နဲ့ spawn လုပ်မယ်

## 2) Run commands

### uv သုံးတဲ့နည်း

```bash
uv run main.py
```

### python သုံးတဲ့နည်း

```bash
python main.py
```

## 3) “MCP server alone” ကို စစ်ချင်ရင်

ဒီ project မှာ server က STDIO transport နဲ့ run လုပ်ထားတဲ့အတွက် “human interactive” လို run စစ်တာက အဆင်မပြေပါဘူး (STDIO က protocol messages သွားလာရတာမို့)။

အဲဒါကြောင့် “server အလုပ်လုပ်/မလုပ်” ကိုစစ်ဖို့ **client test** လေးကိုသုံးတာအကောင်းဆုံးပါ။

## 4) Client tool list test (`mcp_client.py` ထဲက main)

`mcp_client.py` အောက်ဆုံးမှာ test `main()` ပါပြီးသားပါ—

- server ကို spawn
- `list_tools()` call
- result print

Run:

```bash
python mcp_client.py
```

Output မှာ tool names (`read_doc_contents`, `edit_document`) တွေပါလာရင် MCP client ↔ server STDIO connection အလုပ်လုပ်နေပြီလို့ယူဆနိုင်ပါတယ်။

## 5) CLI ထဲမှာ tool calling loop စစ်ရန်

CLI ကို run ပြီးနောက် user input ပေးပါ—

- tool call မလိုတဲ့ simple question
- doc mention / command flow (resources/prompts ကို Page 06 အတိုင်း implement ပြီးမှ)

