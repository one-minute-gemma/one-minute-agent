interface ParsedLLMResponse {
    thought: string;
    action: string | null;
    actionInput: any;
}

export function parseLLMResponse(response: string): ParsedLLMResponse {
    try {
        const jsonString = response
            .replace(/```(?:json)?/g, '')
            .trim();
        const obj = JSON.parse(jsonString);
        return {
            thought: obj.thought || '',
            action: obj.action === 'None' ? null : obj.action || null,
            actionInput: obj.actionInput ?? null,
        };
    } catch {
        return {
            thought: '',
            action: null,
            actionInput: null,
        };
    }
}

export function parseAnswer(response: string): string {
    const jsonString = response
        .replace(/```(?:json)?/g, '')
        .trim();
    const obj = JSON.parse(jsonString);
    return obj.answer || '';
}