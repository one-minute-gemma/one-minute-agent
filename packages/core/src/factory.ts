import { LLMHandler } from "./types";
import { OpenAILLM } from "../../providers/online/provider-openai";
import { LocalLLM } from "../../providers/offline/provider-llamarnn";

export type LLMVendor = { kind: "openai"; apiKey: string; model?: string }
                     | { kind: "local"; modelPath: string };

export function createLLM(vendor: LLMVendor): LLMHandler {
  switch (vendor.kind) {
    case "openai": return new OpenAILLM(vendor.apiKey, vendor.model);
    case "local":  return new LocalLLM();
  }
}