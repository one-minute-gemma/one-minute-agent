export interface LLMHandler {
    sendToLLM(messages: any[]): Promise<string>;
    structuredFollowup(functionResult: any): Promise<string>;
}