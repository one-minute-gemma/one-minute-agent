# nagents

nagents is a package that provides a framework for building agents using typescript, and, more specifically, to allow react native developers to run agentic workflows using locally hosted models.

[...WORK IN PROGRESS...]

# How to run project

1. Install all the necesary dependencies:

```bash
npm install
```

2. Set your OPENAI_API_KEY in a .env file in the root directory.

3. Then, run our agent example:

```bash
npx ts-node agent-cli/src/index.ts
```

The example will run a simple dummy agent that is equiped with tools and strong prompting to allow it to help a person during an emergency by communicating with a 911 operator.

# Future work

- [ ] Add support for offline provider for llama.rnn and other ways of running models locally
- [ ] Add more online providers
- [ ] Add other examples
