import readline from "readline";
import { BaseAgent } from "../../packages/core/src/base-agent";
import { parseLLMResponse } from "../../packages/core/utils/parser";
import { tools } from "./tools";
import { OpenAILLM } from "../../packages/providers/online/provider-openai";
import dotenv from "dotenv";
import fs from "fs";

export class CLIAgent extends BaseAgent {
    private rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  
    async getUserInput() {
      return new Promise<string>(res => this.rl.question("\n👤 Operator: ", res));
    }
  
    async presentThought(thought: string) {
      console.log(`\n🤔 ${thought}`);
    }
  
    async presentAnswer(answer: string) {
      console.log(`\n☑️ ${answer}`);
    }
  
    close() { this.rl.close(); }
}

if (require.main === module) {
  dotenv.config();
  const llm = new OpenAILLM(process.env.OPENAI_API_KEY ?? "");
  const systemPrompt = fs.readFileSync("agent-cli/src/prompt.md", "utf8");
  const agent = new CLIAgent(llm, tools, systemPrompt);
  agent.run();
}