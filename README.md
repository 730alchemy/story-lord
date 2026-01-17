# story-lord

## Characters

3 sources

- built into the framework
- create by a user
- provided by a 3rd party

Each character is a separate agent that generates their own dialogue. All character agents must implement a core set of functions: speak,
think, choose, answer. The idea behind "answer" is that another agent, such as the narrator or architect, can ask the character questions
as part of that agent's work. We must distinguish between character agent types and character agent instances. For example, we might have
2 agent types, each using a different personality model: CharacterAgentMBTI and CharacterAgentBigFive. There can be multiple instances of
these agent types. Sally and Taj might be of type CharacterAgentMBTI while Roger and Lizzy are of the other type. However, all agent types
will always implement the core set of functions. Each character agent type will have it's own set of properties. For example,
"extroversion" might be a property of CharacterAgentMBTI but not of the other character types. Each instance of an agent type will have
their own unique values for all properties and they will have their own instructions. Characters must maintain memory and state across
scenes.
