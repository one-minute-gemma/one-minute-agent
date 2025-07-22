import OpenAi from "openai";
import readline from "readline";
import dotenv from "dotenv";
import fs from "fs";
import parseLLMResponse from "./parser";

dotenv.config();

const openai = new OpenAi({
  apiKey: process.env.OPENAI_API_KEY,
});

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

const messages: any[] = [];

const SYSTEM_PROMPT = fs.readFileSync("src/prompt.md", "utf-8");
messages.push({ role: "system", content: SYSTEM_PROMPT });

async function get_health_metrics(_: any) {
  console.log("✅ Getting health metrics");
  return {
    heart_rate: 100,
    blood_pressure: 120,
    blood_oxygen: 95,
  };
}

async function get_user_location(_: any) {
  console.log("📍 Getting user location");
  return {
    latitude: 40.7128,
    longitude: -74.0060,
  };
}

async function get_audio_input(_: any) {
  console.log("🎙️ Getting audio input");
  const situations = [
    "Ah! I think I'm having a heart attack",
    "Cough, cough, cough",
    "Ahh!!! My chest is killing me",
    "I feel some pressure in my chest",
    "Please help me, I'm dying",
  ];
  return { audio: situations[Math.floor(Math.random() * situations.length)] };
}

async function get_video_input(_: any) {
  console.log("📹 Getting video input");
  const situations = [
    "The person is lying on the ground, not moving",
    "The person is unconscious, not moving",
    "The person is unresponsive, not moving",
    "The person is not breathing, not moving",
  ];
  return { video: situations[Math.floor(Math.random() * situations.length)] };
}

async function get_user_details(_: any) {
  console.log("👤 Getting user details");
  return {
    name: "John Doe",
    age: 30,
    gender: "male",
    blood_type: "A+",
    medical_history: "None",
    current_medications: "None",
    allergies: "None",
    medical_conditions: "None",
  };
}

const function_map: { [key: string]: Function } = {
  get_health_metrics,
  get_user_location,
  get_audio_input,
  get_video_input,
  get_user_details,
};

async function send_to_llm(prompt: string): Promise<string> {
  messages.push({ role: "user", content: prompt });
  const response = await openai.chat.completions.create({
    model: "gpt-4o-mini",
    messages,
  });

  const content = response.choices[0].message.content || "";
  messages.push({ role: "assistant", content });
  return content;
}

async function structured_followup(functionResult: any): Promise<string> {
  return `
Observation: ${JSON.stringify(functionResult)}

Continue reasoning. Follow this exact format:
Thought: <your reasoning>
Action: <function_name>|None
Action Input: <JSON or null>
`;
}

async function main() {
    while (true) {
      const input: string = await new Promise((resolve) => {
        rl.question("\n👮 Operator: ", resolve);
      });
  
      let llmResponse = await send_to_llm(input);
  
      while (true) {
        if (!llmResponse) {
          console.error("❌ LLM returned no response");
          break;
        }
  
        const { thought, action, actionInput } = parseLLMResponse(llmResponse);
  
        console.log(`\n🤔 Thought: ${thought}`);
  
        if (!action || action.toLowerCase() === "none") {
          const naturalLanguagePrompt = `
          Now answer the operator's question directly and clearly in natural language.
          
          Operator's question: "${input}"
          `;
          
          llmResponse = await send_to_llm(naturalLanguagePrompt);
          
          console.log(`\n🚨 Operator Answer:\n${llmResponse}`);
          break;
        }
  
        console.log(`⚙️ Action: ${action}`);
        console.log(`📨 Action Input: ${JSON.stringify(actionInput)}`);
  
        const functionToCall = function_map[action];
        if (!functionToCall) {
          console.error(`❌ No such function: ${action}`);
          break;
        }
  
        const functionResult = await functionToCall(actionInput);
  
        llmResponse = await send_to_llm(await structured_followup(functionResult));
      }
    }
  }
  

main();
