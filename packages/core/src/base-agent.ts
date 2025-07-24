import { parseAnswer, parseLLMResponse } from "../utils/parser";
import { AgentInterface, ChatMessage, ToolInterface, LLMHandler, ToolCallResult } from "./types";

export abstract class BaseAgent implements AgentInterface {
  readonly messages: ChatMessage[] = [];
  tools: Map<string, ToolInterface>;

  constructor(
    public llm: LLMHandler,
    tools: ToolInterface[],
    public systemPrompt: string
  ) {
    this.tools = new Map(tools.map(t => [t.name, t]));
    this.messages.push({ role: "system", content: systemPrompt });
  }

  async sendAndStore(role: ChatMessage["role"], content: string) {
    this.messages.push({ role, content });
    const reply = await this.llm.chat(this.messages);
    this.messages.push({ role: "assistant", content: reply });
    return reply;
  }

  async structuredFollowUp(r: ToolCallResult): Promise<string> {
    return [
        `
        Observation: ${JSON.stringify(r)}

        Continue reasoning. Follow this exact format:
        {
            "thought": <your reasoning>,
            "action": <function_name>|None,
            "actionInput": <JSON or null>
        }
        `
    ].join("\n");
  }

  async finalAnswer() {
    this.messages.push({ role: "assistant", content: finalAnswerPrompt });
    const reply = await this.llm.chat(this.messages);
    return reply;
  }

  async executeTool(name: string, input: unknown) {
    const tool = this.tools.get(name);
    if (!tool) throw new Error(`No such tool: ${name}`);
    return tool.run(input);
  }

  abstract getUserInput(): Promise<string>;
  abstract presentAnswer(answer: string): Promise<void>;
  abstract presentThought(thought: string): Promise<void>;
  
  async run() {
    while (true) {
      const user = await this.getUserInput();
      let reply = await this.sendAndStore("user", user);
  
      while (true) {
        const { thought, action, actionInput } = parseLLMResponse(reply);
        await this.presentThought(thought);
  
        if (!action || action === "None") {
          const answer = await this.finalAnswer();
          await this.presentAnswer(parseAnswer(answer));
          break;
        }
  
        const result = await this.executeTool(action, actionInput);
        reply = await this.sendAndStore("system", await this.structuredFollowUp(result));
      }
    }
  }
}


const finalAnswerPrompt = `
    You now have to answer the question posed to you by the user.

    Remember to answer using the following format:
    {
        "answer": <your answer here>,
    }
`;