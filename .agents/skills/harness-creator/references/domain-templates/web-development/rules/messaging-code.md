---
paths:
  - "messaging/**"
  - "queues/**"
  - "events/**"
  - "pulsar/**"
  - "rabbitmq/**"
---

# Messaging Code Rules

- Message format must be JSON with schema version field
- Consumers must be idempotent (safe to reprocess the same message)
- Error queue must be configured for failed messages
- Topic/queue naming: `module.event_type` (e.g., `user.created`, `order.completed`)
- Producer must handle connection failures gracefully with retry
- Message schemas must be documented and versioned
- Large messages (>64KB) should use reference pattern (store in DB, send ID)
- Time-sensitive messages must have TTL configured

## Examples

**Correct** (idempotent consumer with error handling):
```python
class UserCreatedConsumer:
    """
    Consumer for user.created events.

    Idempotency: Uses user_id as idempotency key. If user already exists,
    event is acknowledged but not processed.
    """

    async def process(self, message: dict) -> None:
        event_id = message["event_id"]
        user_id = message["data"]["user_id"]

        # Idempotency check
        if await self._is_processed(event_id):
            logger.info(f"Event {event_id} already processed, skipping")
            return

        try:
            # Process the event
            await self._create_user_profile(user_id, message["data"])

            # Mark as processed
            await self._mark_processed(event_id)

        except ValidationError as e:
            # Business error - send to error queue for investigation
            await self._send_to_error_queue(message, str(e))
            raise

        except TemporaryError as e:
            # Infrastructure error - retry later
            raise  # Message will be redelivered
```

**Correct** (message format with versioning):
```python
# CORRECT: Versioned message format
message = {
    "schema_version": "1.0",
    "event_id": "evt_abc123",
    "event_type": "user.created",
    "timestamp": "2026-03-30T14:30:00Z",
    "source": "auth-service",
    "data": {
        "user_id": "usr_123",
        "email": "user@example.com",
        "name": "John Doe"
    }
}

# CORRECT: Topic naming convention
# user.created     - User account created
# user.email_verified - User verified their email
# order.placed     - Customer placed an order
# order.cancelled  - Order was cancelled
```

**Incorrect** (no idempotency, no versioning):
```python
# VIOLATION: no idempotency check
# VIOLATION: no schema version
# VIOLATION: no error handling
async def process_message(message):
    user = message["user"]  # No version field
    await create_profile(user)  # Will create duplicate on retry
    # No error handling
```