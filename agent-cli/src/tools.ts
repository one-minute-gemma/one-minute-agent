import { ToolInterface } from "../../packages/core/src/types";

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

export const tools: ToolInterface[] = [
    {
        name: "get_health_metrics",
        description: "Get the health metrics of the user",
        parameters: {},
        run: get_health_metrics
    },
    {
        name: "get_user_location",
        description: "Get the location of the user",
        parameters: {},
        run: get_user_location
    },
    
    {
        name: "get_audio_input",
        description: "Get the audio input of the user",
        parameters: {},
        run: get_audio_input
    },

    {
        name: "get_video_input",
        description: "Get the video input of the user",
        parameters: {},
        run: get_video_input
    },

    {
        name: "get_user_details",
        description: "Get the details of the user",
        parameters: {},
        run: get_user_details
    }
    
    
]