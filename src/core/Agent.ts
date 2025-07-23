import readline from "readline";
import openai, { OpenAI } from "openai";
import { parseLLMResponse, parseAnswer } from "../utils/parser";
import ToolInterface from "../interfaces/ToolInterface";
import { LLMHandler } from "../interfaces/LLMInterface";

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });

export class Agent {
    private llm: LLMHandler;
    private tools: Map<string, ToolInterface>;
    private userRole: string;
    private messages: any[] = [];

    constructor(llm: LLMHandler, tools: ToolInterface[], systemPrompt: string, userRole: string) {
        this.llm = llm;
        this.tools = new Map<string, ToolInterface>(tools.map(tool => [tool.name, tool]));
        this.userRole = userRole ?? "user"
        this.messages.push({ role: "system", content: systemPrompt });
    }

    private async structuredFollowup(functionResult: any): Promise<string> {
        return `
          Observation: ${JSON.stringify(functionResult)}
          
          Continue reasoning. Follow this exact format:
          Thought: <your reasoning>
          Action: <function_name>|None
          Action Input: <JSON or null>
          `;
    }

    private async sendAndStoreMessage(role: string, content: string): Promise<string> {
        this.messages.push({ role, content });
        const response = await this.llm.sendToLLM(this.messages);
        this.messages.push({ role: "assistant", content: response });
        return response;
    }

    private async executeTool(action: string, actionInput: any): Promise<any | null> {
        console.log(`\n🔍 Executing tool: ${action}`);
        const tool = this.tools.get(action);
        if (!tool) {
            console.error(`❌ No such tool: ${action}`);
            return null;
        }
        return await tool.function(actionInput);
    }

    private async getUserInput(): Promise<string> {
        return new Promise((resolve) => {
            rl.question(`\n👮 ${this.userRole}: `, resolve);
        });
    }

    public async run() {
        while (true) {
            const input: string = await this.getUserInput();
            
            let llmResponse = await this.sendAndStoreMessage("user", input);

            while (true) {
                if (!llmResponse) {
                    console.error("❌ LLM returned no response");
                    break;
                }

                const { thought, action, actionInput } = parseLLMResponse(llmResponse);

                console.log(`\n🤔 Thought: ${thought}`);

                if (!action || action.toLowerCase() === "none") {
                    const naturalLanguagePrompt = `
                    Now answer the ${this.userRole.toLowerCase()}'s question directly and clearly in natural language.
          
                    ${this.userRole}'s question: "${input}"
                    `;
                    llmResponse = await this.sendAndStoreMessage("user", naturalLanguagePrompt);

                    console.log(`\n🚨 ${this.userRole} Answer:\n${parseAnswer(llmResponse)}`);
                    break;
                }

                console.log(`⚙️ Action: ${action}`);
                console.log(`📨 Action Input: ${JSON.stringify(actionInput)}`);

                const functionResult = await this.executeTool(action, actionInput);
                if (functionResult === null) break;
                llmResponse = await this.sendAndStoreMessage("user", await this.structuredFollowup(functionResult));
            }
        }

       

        }
}