1. Use conduit to get the jira tickets with 'To Do' status, and get the one with the lowest number on project DA.
2. Create an ElevenLabs agent with the following parameters:
    - The agent is you, the executive assistant, as an interviewer to extract all the required information from me, working with me as a partner and a mentor, challenging my ideas, to be the best that they can be. 
    - In the system prompt set
    Personality: Defines agent identity through name, traits, role, and relevant background.

    Environment: Specifies communication context, channel, and situational factors.

    Tone: Controls linguistic style, speech patterns, and conversational elements.

    Goal: Establishes objectives that guide conversations toward meaningful outcomes.

    Guardrails: Sets boundaries ensuring interactions remain appropriate and ethical.

    Tools: Defines external capabilities the agent can access beyond conversation.
    
    - For the first message, the agent should immediately set expectations with something like: "Hi! I'm here to partner with you to create [document type from Jira ticket]. Rather than you dictating information to me, I'll systematically interview you with direct questions to make sure we capture everything and don't miss any key points. The requirements for the doc are follows, [brief summarization of the doc requirements] This collaborative approach ensures we build the best possible document together. Ready to get started?"
   - Duration: 3000 seconds
   - Voice: Alice (ID: Xb7hH8MSUJpSbSDYk0k2)
   - Temperature: 1.1

3. Display the url of the agent. https://elevenlabs.io/app/talk-to?agent_id=<agent_id>
4. Ask to proceed.
5. Retrieve the agent's conversation
6. Extract the conversation transcript
7. Update the jira ticket with the coversation id
8. Create a Google Doc described by the jira from the transcript content.
  1. First use share-doc to make it public:
  {
    "docId": "your-doc-id",
    "role": "reader",
    "type": "anyone",
    "sendNotification": false
  }
  2. Then use get-share-link to retrieve the link:
  {
    "docId": "your-doc-id"
  }
9. Close the ticket in Conduit, including the Google Doc ID, if the document is complete, move status to done, if there is missing information move to in review