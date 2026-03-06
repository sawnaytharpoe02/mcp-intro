# Glossary (အသုံးအနှုန်းများ)

- **MCP (Model Context Protocol)**: AI model ကို tools/resources/prompts နဲ့ စံပုံစံအတိုင်းချိတ်ဆက်ပေးတဲ့ protocol
- **Server**: tools/resources/prompts ကို expose လုပ်တဲ့ process/service
- **Client**: server ကို transport နဲ့ချိတ်ပြီး tool call/resource read/prompt get လုပ်တဲ့ app-side code
- **Tool**: action/function တစ်ခုကို name + input schema နဲ့ expose လုပ်ထားတာ
- **Resource**: URI နဲ့ address လုပ်လို့ရတဲ့ data (read-only သို့ read-mostly pattern များ)
- **Prompt**: command-like template messages (LLM ကိုပို့မယ့် message set ကို server-defined အဖြစ်စံသတ်မှတ်ထားခြင်း)
- **Transport**: Client ↔ Server ဆက်သွယ်ရေး channel (stdio, http, sse, websocket ...)
- **STDIO transport**: server ကို subprocess အဖြစ် run လုပ်ပြီး stdin/stdout နဲ့ protocol messages ပို့ဆက်သွယ်ခြင်း
- **Tool calling (Function calling)**: LLM က tool ကိုခေါ်ဖို့ structured call output ထုတ်ပြီး app က deterministic execute လုပ်ပေးတဲ့ pattern

