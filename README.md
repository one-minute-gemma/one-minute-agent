 # One Minute Agent ⌚️: the help you need when seconds count

An intelligent emergency response system built on the `nagents` framework. This project includes both a core agent framework (`nagents`) and a what we call "One Minute Platform" (`one-minute-agent`). The platform holds two different agents: one for emergency victim assistance and support and one for 911-operator communication. Each different agent is built to be run locally using ollama.

Furthermore, there are two directories (`streamlit`) and (`react-app`). Both of these applications hold different iterations of the project's frontend.

## Motivation

The motivation behind this project comes from the fact that we have personally experienced situations where people around us have been in need of immediate assistance, but, at the time, they were unable to get it. From seizures, to heart attacks and even epileptic episodes, we have seen firsthand how difficult it can be to get help in a timely manner: especially for some demographics of people like the elderly, the disabled, people living alone, and even persons that practice extreme sports. Often these people may find themselves alone, with no one around to help. And we think that they deserve better.

Apart from that, we also consider that this solution can be deployed into very different contexts, which can allow people to receive help wherever they are, whenever they need it. For example, we plan to continue working on One Minute to allow integrations into smart homes, smart cars, smart watches, mobile phones, etc.

We also believe that this is a perfect application for offline, privacy-first AI. Medical records are sensitive information, and we believe that it should be kept private. Furthermore, we know that emergencies may happen at any time, anywhere. This is why we decided to build a system that can be used offline, through tooling that enables user location from last-known locations, as well as through technologies like phone calls and SMS (integrations with these are in the works).

## Project Overview

The One Minute Platform is a system that allows users to get help when seconds count. It is built on the `nagents` framework, and it includes two different agents: one for emergency victim assistance and support and one for 911-operator dispatching. Each different agent is built to be run locally using ollama.

### Nagents

`nagents` is a framework that came as a surprise with the creation of this project. When we were looking into what technology we could use, we got the impression that other agentic frameworks are either too complex, or not focused on small models like `gemma3n`. We also wanted to build a system that was easy to understand and modify, and `nagents` seemed to be the perfect fit.

This is why we decided to create a custom framework that would allow us, and hopefully others very soon, to build agent frameworks that are easy to understand and modify when running on small models. Moreover, we also found very difficult to integrate tool calling into models like `gemma3n`, even with existing solutions. We also considered the alternative of finetuning the models using tools like unsloth, but we were still unable to do so due to computational and data constraints. That's why `nagents` allows you to give your model agentic capabilities through a ReAct thinking process, as well as by using structured tool calling. 

This library can be found in the `nagents/` directory, and we plan to separate it into its own repository in the future. Furthermore, there are other implementations of the framework in other languages like typescript which can be found in [this repository](https://github.com/ramcav/nagents/tree/main/src). This library is a work in progress, and we are constantly adding new features and improving the framework: we hope to release it to the open source community in the future.

### Project Architecture

We wanted to build a system that was coherent for helping both the 911 operators and the emergency victims. We think that in a lot of cases, 911 operators are not able to help the victims as quickly as they would like to, and this may not be their fault or the victims'. These situations are high risk and trigger a lot of stress, thus, reducing that communication burden was logical to us.

This is why our system has clear separation of concerns: we have the `nagents` framework which is the backbone of both agents, and then two individual agents that can be instantiated and run locally. These agents have access to tools that allow them to interact with the world (more on this later). Finally, we have a streamlit app acting as the bridge between the agents and the users.

It is important to highlight that we wanted to build a frontend in react as well as our second iteration, and that is currently in progress.

Below you can find a diagram of the project architecture:

![Project Architecture](./misc/system_architecture.png)

### Agents

#### Victim assistance agent

This agent is the one that is responsible for helping the emergency victim. It is built to be run locally, and it is the one that is responsible for. This agent's sole responsibility is to help the victim in any way possible (act as a first responder) by providing medical advice as well as emotional support.

It has access to a set of tools that allow it to interact with the world. These tools are:

- `get_emergency_location`: This tool allows the agent to get the emergency location of the victim.
- `get_first_aid_advice`: This tool allows the agent to get first aid advice for the victim based on a traditional matching of input to a set of predefined first aid instructions.
- `get_rag_medical_advice`: This tool allows the agent to get medical advice for the victim by using a RAG system.

The victim assistance agent has a prompt that can be found in `one-minute-agent/agents/victim_assistant/prompts/prompt.md`. This prompt is used to guide the agent's behavior and to provide it with the necessary context to help the victim. We underwent a lot of iterations to get to this prompt, and we are constantly improving it.

#### 911 operator agent

This agent is responsible for communciation with 911 operators. It's job is to get information from the victim and relay it to the operator. It also has access to a set of tools that allow it to interact with the world to get more information about the situation even if the victim is unable to provide it. These tools are:

- `get_health_metrics`: This tool allows the agent to get the health metrics of the victim.
- `get_user_location`: This tool allows the agent to get the location of the victim.
- `get_audio_input`: This tool allows the agent to get audio input from the victim.
- `get_video_input`: This tool allows the agent to get video input from the victim.
- `get_user_details`: This tool allows the agent to get the details of the victim.
- `call_emergency_contact`: This tool allows the agent to call the emergency contact of the victim.
- `activate_alarm`: This tool allows the agent to activate the alarm.
- `log_incident`: This tool allows the agent to log the incident.

Note: Some of these tools are implemented as dummies in the current state of the project. We are working on implementing them in the future. 

The 911 operator agent has a prompt that can be found in `one-minute-agent/agents/operator/prompts/prompt.md`. This prompt is used to guide the agent's behavior and to provide it with the necessary context to help the victim. We underwent a lot of iterations to get to this prompt, and we are constantly improving it.

### Streamlit App

The streamlit app is the one that is responsible for the communication between the agents and the users. This acts as a Proof Of Concept for the project, as we want to transition this app to be used in other contexts apart from browsers in the future.

### React App

This is also a work in progress, and we are currently working on it. It would be a better iteration on the already existinf PoC.

## Challenges and Learnings

This project was a very challenging one, and we learned a lot from it. We had to pivot several times in the implementation side as we started with the idea of building a fully functional react native app. This proved to be very difficult, especially considering the time constraints we had. Despite this, we were able to at least understand how to use technologies like `llama.rnn` (library that wraps the `llama.cpp` library for react native) to run models locally. Though, we decided to pivot because we knew that building a library like `nagents`for react native would take us even more time (this is being worked on, though 👀), and we wanted to focus on the core of the project and release a valuable PoC.

This is when we pivotted to using Python. We first turned to `Google Adk`, but we quickly realized that it was not the right tool for the job. For some reason, we did not manage to get reasonable results with it: agent workflows were very buggy, possibly because `gemma3n` does not natively support tool calling. We read others had similar issues in the library's GitHub issues, and we decided to pivot to `nagents`.

Setting up `nagents` also was a challenge that goes out of the scope of this project, however, we were able to abstract the main parts that are needed to build an agentic system.

In terms of agent behavior, despite our agents managing themselves well, they still suffer from hallucinations. We have ran informal benchmarks against the regular model without any prompt enginering and we see that a lot of its features shine through, despite us ordering the model to act in a certain way. They especially tend to overexagerate small details like 'I am bleeding' and jump to conclusions instead of asking further questions or using tooling sometimes. This made us look into finetuning, which also proved to be difficult as we did not manage to download the GGUF from Kaggle because of computational constraints.

Another issue we went through was the fact that the `gemma3n` version offered through `ollama` did not support multimodality. This was a big hurdle as we had assumed from the beginning that we would be able to use the model to get audio and video input from the victim. However, we do not consider this a sever technical debt as this can be solved just by plugging the right model once it is made available.

Despite all of this, we are very proud of the results we have achieved. We have a working system that can be used to help people in need, and we are constantly improving it. We think that our open source contribution with `nagents` + `one-minute-agent`+ `gemma3n` can be a great start for us and otherpeople to build upon, and, more importantly, to start saving peoples lives.

## Tech debt and Future Work

We have a lot of things we have to improve in the future. Below you can find them listed down based on different categories:

- **Nagents**:
    - Add support for providers like `llama.cpp`.
    - Abstract the functionality even more so the user can spin up an agent with a single function call.

- **Agents**:
    - Improve communication between agents through logging system (read -> write -> repeat cycle through file).
    - Attach proper functionality to tools, as some of them still have dummy implementations.
    - Use abstract functionality over hardcoded implementations
    - Improve prompts so models hallucinate less (they tend to overexagerate and not engage in human-like, short conversations)
    - Finetune the models for function calling and the specific tasks they are supposed to do.

- **React App**:
    - Move our Streamlit PoC to a React App.

## On the technical side

### Directory Structure

- **`nagents/`** - Core agent framework with base classes, tool registry, and provider system
- **`one-minute-agent/`** - Agent implementations
- **`streamlit/`** - Streamlit PoC
- **`react-app/`** - React App PoC
- **`misc/`** - Legacy experimental code and samples
- **`medical_kb/`** - Knowledge base for the medical tooling

### Prerequisites

- Python 3.13+
- [Ollama](https://ollama.ai/) installed and running locally

### Quick Start

#### 1. Setup Environment

```bash
# Create and activate virtual environment
uv venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv sync
```

#### 2. Install Ollama Model

```bash
ollama pull gemma3n:e2b
```

#### 3. Run the Emergency Agent

```bash
# Run the emergency response agent
python -m one-minute-agent

# OR run the framework example
python -m nagents
```

### Development

Each component has its own README with detailed information:
- See `nagents/README.md` for framework documentation
- See `one-minute-agent/README.md` for emergency agent specifics

## HF Spaces Config

---
title: One Minute Agent
emoji: 🚨
colorFrom: red
colorTo: yellow
sdk: docker
app_port: 8501
pinned: false
---
