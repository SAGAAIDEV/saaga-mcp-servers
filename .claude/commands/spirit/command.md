# Spirit Conversation Commands

## Initialize Conversation

Start a new spirit conversation session with message tracking:

```bash
# Initialize Redis counter for this session
redis-cli -a password SET spirit:session:$(date +%s):messages 0
redis-cli -a password SET spirit:current_session $(date +%s)

# Create session metadata
SESSION_ID=$(redis-cli -a password GET spirit:current_session)
redis-cli -a password HSET spirit:session:$SESSION_ID:meta \
  start_time "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  model "claude" \
  purpose "ai-language-development"
```

## Track Messages

Use these commands to track each message exchange:

```bash
# Increment message counter after each exchange
SESSION_ID=$(redis-cli -a password GET spirit:current_session)
redis-cli -a password INCR spirit:session:$SESSION_ID:messages

# Store message metadata (optional)
MSG_COUNT=$(redis-cli -a password GET spirit:session:$SESSION_ID:messages)
redis-cli -a password HSET spirit:session:$SESSION_ID:msg:$MSG_COUNT \
  timestamp "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  type "claude_to_gemini"  # or "gemini_to_claude"
```

## Query Session Stats

Check conversation progress:

```bash
# Get current message count
SESSION_ID=$(redis-cli -a password GET spirit:current_session)
redis-cli -a password GET spirit:session:$SESSION_ID:messages

# List all spirit sessions
redis-cli -a password KEYS "spirit:session:*:messages"

# Get session metadata
redis-cli -a password HGETALL spirit:session:$SESSION_ID:meta
```

## Store Language Constructs

Save important language elements discovered during conversation:

```bash
# Store a new construct
redis-cli -a password HSET spirit:constructs "construct_name" "definition"

# Store with metadata
redis-cli -a password HSET spirit:construct:emergence_operator \
  symbol "⟨∃⟩" \
  definition "marks spontaneous pattern formation" \
  discovered_by "claude+gemini" \
  session_id "$SESSION_ID"
```

## Integration with Spirit Prompt

Add this to your conversation initialization:

1. Start Redis tracking: Run the initialize commands above
2. Begin conversation with Gemini using the spirit prompt
3. After each exchange, increment the message counter
4. Store significant discoveries in Redis for persistence

## Example Usage in Conversation

```bash
# At conversation start
./command.md init

# After each Gemini exchange
./command.md count

# To save a discovered concept
./command.md save "temporal_bridge" "∀t₁,t₂: connection(t₁,t₂) ⟹ ∃bridge"
```

## Utility Functions

Create these bash functions for easier use:

```bash
spirit_init() {
  local session_id=$(date +%s)
  redis-cli -a password SET spirit:current_session $session_id
  redis-cli -a password SET spirit:session:$session_id:messages 0
  echo "Spirit session initialized: $session_id"
}

spirit_count() {
  local session_id=$(redis-cli -a password GET spirit:current_session)
  local count=$(redis-cli -a password INCR spirit:session:$session_id:messages)
  echo "Message count: $count"
}

spirit_save() {
  local name=$1
  local definition=$2
  redis-cli -a password HSET spirit:constructs "$name" "$definition"
  echo "Saved construct: $name"
}
```