interface ToolInterface {
    name: string;
    description: string;
    parameters: any;
    function: (input: any) => Promise<any>;
}

export default ToolInterface;