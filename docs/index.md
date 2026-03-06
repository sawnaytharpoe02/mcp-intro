# MCP (Model Context Protocol) ကို ဒီ Project နဲ့လေ့လာခြင်း (Burmese)

ဒီ `cli_project` က MCP server/client ကို STDIO transport နဲ့ချိတ်ပြီး CLI chat ထဲကနေ MCP tools ကိုခေါ်သုံးနိုင်အောင် တည်ဆောက်ထားတဲ့ learning project ပါ။

## ဒီ docs ရဲ့ ရည်ရွယ်ချက်

- MCP ကို concept အနေနဲ့ နားလည်လာစေခြင်း (Tools / Resources / Prompts / Transports)
- ဒီ project ထဲက `mcp_server.py` (server) / `mcp_client.py` (client) ကိုဖတ်ပြီး confidence ရလာစေခြင်း
- ကိုယ်တိုင် MCP server/client တစ်ခုကို from-scratch လုပ်နိုင်အောင် လမ်းညွှန်ပေးခြင်း

## စာမျက်နှာလိုက် ဖတ်ရန် (Recommended order)

1. [01 - MCP မိတ်ဆက်](./01-mcp-introduction.md)
2. [02 - Project Architecture (ဒီ project ရဲ့ flow)](./02-project-architecture.md)
3. [03 - MCP Server (FastMCP) ကိုနားလည်ခြင်း](./03-mcp-server-fastmcp.md)
4. [04 - MCP Client (STDIO) ကိုနားလည်ခြင်း](./04-mcp-client-stdio.md)
5. [05 - CLI Chat Flow ( @docs , /commands , tool-calls )](./05-cli-chat-flow.md)
6. [06 - Resources/Prompts ကို project ထဲမှာဖြည့်တည်ဆောက်ခြင်း](./06-add-resources-prompts.md)
7. [07 - Run/Testing/Debugging](./07-testing-debugging.md)
8. [08 - Next Steps (ကိုယ်တိုင် MCP server/client တည်ဆောက်ရန်)](./08-next-steps.md)
9. [Glossary](./glossary.md)

## Notes (အရေးကြီး)

- ဒီ project ထဲက `mcp_server.py` က **tools ၂ခု** ကို implement လုပ်ထားပြီး **resources/prompts** တွေက TODO အနေဖြင့် မပြီးသေးပါဘူး။ Docs မှာ အဲ့ဒါကို ဘယ်လိုဖြည့်ရမလဲကို လမ်းညွှန်ထားပါတယ်။
- CLI က LLM provider အဖြစ် OpenRouter/OpenAI compatible API ကိုသုံးထားတာကြောင့် MCP tools ကို LLM function calling နဲ့ချိတ်ထားတဲ့ pattern ကိုလည်း လေ့လာနိုင်ပါတယ်။

