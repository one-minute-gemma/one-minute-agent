import { ChatMessage, LLMHandler, ToolCallResult } from "./types";

export abstract class BaseLLM implements LLMHandler {
  abstract chat(msgs: ChatMessage[]): Promise<string>;
}