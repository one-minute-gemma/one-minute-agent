
import dotenv from "dotenv";
import fs from "fs";
import { Agent } from "./core/Agent";
import ToolInterface from "./interfaces/ToolInterface";
import { LLMOnline } from "./core/LLMOnline";
dotenv.config();

async function main() {
   const apiKey = process.env.OPENAI_API_KEY ?? "";

   const tools: ToolInterface[] = getTools();
   const llm: LLMOnline = new LLMOnline(apiKey, "openai");

   const agent = new Agent(llm, tools, fs.readFileSync("src/prompt.md", "utf8"), "Operator");
   await agent.run();
}

// Below are details that would be dependent of the app you are building

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
  
function getTools(): ToolInterface[] {
  return [
    {
        name: "get_user_location",
        description: "Get the user's location",
        parameters: {},
        function: get_user_location
    },
    {
      name: "get_user_details",
      description: "Get the user's details",
      parameters: {},
      function: get_user_details
    },
    {
      name: "get_health_metrics",
      description: "Get the user's health metrics",
      parameters: {},
      function: get_health_metrics
    },
    {
      name: "get_audio_input",
      description: "Get the user's audio input",
      parameters: {},
      function: get_audio_input
    },
    {
      name: "get_video_input",
      description: "Get the user's video input",
      parameters: {},
      function: get_video_input
    }
   ]
}

main();
