import OpenAI from "openai";
import { BaseLLM } from "../../core/src/base-llm";
import { ChatMessage } from "../../core/src/types";

export class OpenAILLM extends BaseLLM {
  private client: OpenAI;
  constructor(apiKey: string, private model = "gpt-4o-mini") {
    super();
    this.client = new OpenAI({ apiKey });
  }
  async chat(messages: ChatMessage[]): Promise<string> {
    const res = await this.client.chat.completions.create({
      model: this.model,
      messages: messages as OpenAI.Chat.ChatCompletionMessageParam[]
    });
    return res.choices[0].message.content ?? "";
  }
}
