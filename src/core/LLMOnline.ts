import OpenAI from "openai";
import { LLMHandler } from "../interfaces/LLMInterface";

export class LLMOnline implements LLMHandler {
    private llm: any;
  
    constructor(apiKey: string, vendor: string) {
        this.llmSetup(apiKey, vendor);
    }
  
    private llmSetup(apiKey: string, vendor: string) {
      if (vendor === "openai") {
      this.llm = new OpenAI({
          apiKey: apiKey,
      }); 
      return 0;   
    }
    throw new Error("Invalid vendor");
    }

    async sendToLLM(messages: any[]): Promise<string> {
        const response = await this.llm.chat.completions.create({
          model: "gpt-4o-mini",
          messages: messages,
        });
      
        const content = response.choices[0].message.content || "";
        return content;
    }

    async structuredFollowup(functionResult: any): Promise<string> {
        return `
          Observation: ${JSON.stringify(functionResult)}
          
          Continue reasoning. Follow this exact format:
          Thought: <your reasoning>
          Action: <function_name>|None
          Action Input: <JSON or null>
          `;
    }
  }