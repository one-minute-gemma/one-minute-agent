export interface ChatMessage {
    role: "system" | "user" | "assistant" | "tool";
    content: string;
  }
  
  export type ToolCallResult = unknown;
  
  export interface ToolInterface<I = unknown, O = unknown> {
    name: string;
    description: string;
    parameters: I;
    run(input: I): Promise<O>;
  }
  
  export interface LLMHandler {
    chat(messages: ChatMessage[]): Promise<string>;
  }
  
  export interface AgentInterface {
    llm: LLMHandler;
    tools: Map<string, ToolInterface>;
    systemPrompt: string;
    messages: ChatMessage[];
  
    sendAndStore(role: ChatMessage["role"], content: string): Promise<string>;
    executeTool(name: string, input: unknown): Promise<unknown>;
    getUserInput(): Promise<string>;
    presentAnswer(answer: string): Promise<void>;
    presentThought(thought: string): Promise<void>;
    run(): Promise<void>;
  }
  