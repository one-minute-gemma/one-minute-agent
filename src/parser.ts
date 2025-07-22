interface ParsedLLMResponse {
    thought: string;
    action: string | null;
    actionInput: any;
}

export default function parseLLMResponse(response: string) {
    const thoughtMatch = response.match(/Thought:\s*(.*)/i);
    const actionMatch = response.match(/Action:\s*(.*)/i);
    const actionInputMatch = response.match(/Action Input:\s*([\s\S]*)/i);

    const thought = thoughtMatch ? thoughtMatch[1].trim() : '';
    const action = actionMatch ? actionMatch[1].trim() : null;

    let actionInput: any = null;

    if (actionInputMatch) {
        const inputString = actionInputMatch[1].trim();
        try {
            actionInput = inputString !== 'null' ? JSON.parse(inputString) : null;
        } catch {
            actionInput = null;
        }
    }

    return {
        thought,
        action: action === 'None' ? null : action,
        actionInput,
    };
}