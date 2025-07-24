import { BaseLLM } from "../../core/src/base-llm";
import { ChatMessage } from "../../core/src/types";
// import { load } from "react-native-llama.cpp";

class load {
    constructor() {}
    complete(msgs: ChatMessage[]) {
        return "Not implemented";
    }
}

export class LocalLLM extends BaseLLM {

  private engine = new load(/* … */);
  async chat(msgs: ChatMessage[]) {
    return this.engine.complete(msgs);
  }
}