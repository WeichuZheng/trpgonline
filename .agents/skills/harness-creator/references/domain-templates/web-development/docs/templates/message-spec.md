# Message Specification: [Event/Queue Name]

> **Status**: Draft | Review | Approved | Deprecated
> **Version**: 1.0
> **Last Updated**: YYYY-MM-DD

## Overview

[What this message/event represents and why it exists.]

## Topic/Queue Information

| Field | Value |
|-------|-------|
| **Name** | `module.event_type` (e.g., `user.created`) |
| **Type** | Topic / Queue |
| **Broker** | Pulsar / RabbitMQ |
| **Retention** | 7 days / Infinite |
| **Partitioning** | By `user_id` / None |

## Message Format

### Schema

```json
{
  "schema_version": "1.0",
  "event_id": "evt_abc123def456",
  "event_type": "module.event_type",
  "timestamp": "2026-03-30T14:30:00Z",
  "source": "service-name",
  "correlation_id": "req_xyz789",
  "data": {
    "id": "string",
    "field1": "type",
    "field2": "type"
  },
  "metadata": {
    "version": "1.0",
    "trace_id": "trace_abc123"
  }
}
```

### Field Definitions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| schema_version | string | Yes | Message schema version |
| event_id | string | Yes | Unique event identifier |
| event_type | string | Yes | Event type name |
| timestamp | string | Yes | ISO8601 timestamp |
| source | string | Yes | Service that produced the event |
| correlation_id | string | No | Request correlation ID |
| data | object | Yes | Event payload |
| metadata | object | No | Additional metadata |

### Data Payload Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | string | Yes | Entity ID |
| field1 | string | Yes | [Description] |
| field2 | integer | No | [Description] |

## Producer

### Service

**Name**: [Service that produces this message]

**Trigger**: [When this message is produced]
- [Trigger 1: e.g., User completes registration]
- [Trigger 2: e.g., Admin approves request]

### Publishing Logic

```python
async def publish_event(event_data: dict) -> None:
    message = {
        "schema_version": "1.0",
        "event_id": generate_uuid(),
        "event_type": "module.event_type",
        "timestamp": utc_now().isoformat(),
        "source": "service-name",
        "data": event_data
    }
    await producer.send(topic, message)
```

### Rate Expectations

| Metric | Value |
|--------|-------|
| Average rate | 100 messages/minute |
| Peak rate | 1000 messages/minute |
| Burst handling | Queue with backpressure |

## Consumer

### Service(s)

| Service | Purpose |
|---------|---------|
| [Service 1] | [What it does with this event] |
| [Service 2] | [What it does with this event] |

### Processing Logic

```python
class EventHandler:
    async def process(self, message: dict) -> None:
        event_id = message["event_id"]

        # Idempotency check
        if await self.is_processed(event_id):
            return

        try:
            # Process the event
            await self.handle_event(message["data"])

            # Mark as processed
            await self.mark_processed(event_id)

        except ValidationError as e:
            # Business error - send to DLQ
            await self.send_to_dlq(message, str(e))

        except TemporaryError as e:
            # Retry later
            raise
```

### Idempotency

**Strategy**: [How duplicate messages are handled]
- Store processed `event_id` in Redis with TTL
- Check before processing
- Acknowledge but skip if already processed

### Retry Policy

| Attempt | Delay | Action |
|---------|-------|--------|
| 1 | Immediate | Process |
| 2 | 30 seconds | Retry |
| 3 | 5 minutes | Retry |
| 4 | 30 minutes | Retry |
| 5+ | - | Send to DLQ |

## Error Handling

### Dead Letter Queue

| Field | Value |
|-------|-------|
| **Queue Name** | `module.event_type.dlq` |
| **Retention** | 30 days |
| **Alert Threshold** | 10 messages/hour |

### Error Categories

| Error Type | Action | Retry |
|------------|--------|-------|
| Validation Error | DLQ | No |
| Database Error | Retry | Yes |
| External API Error | Retry | Yes |
| Schema Mismatch | DLQ + Alert | No |

## Monitoring

### Metrics

| Metric | Alert Threshold |
|--------|-----------------|
| Messages produced | N/A |
| Messages consumed | N/A |
| Consumer lag | > 1000 messages |
| DLQ size | > 10 messages |
| Processing latency | > 5 seconds |

### Alerts

| Alert | Condition | Severity |
|-------|-----------|----------|
| HighLag | Lag > 1000 | Warning |
| DLQGrowing | DLQ > 10 | Critical |
| ConsumerDown | No consumption for 5 min | Critical |

## Versioning Strategy

### Backward Compatibility

- New optional fields: Allowed without version bump
- New required fields: Requires new schema version
- Removed fields: Requires new schema version

### Migration Path

1. Producer sends both versions during transition
2. Consumers handle both versions
3. After all consumers updated, producer drops old version

## Testing

### Test Messages

```json
// Valid message
{
  "schema_version": "1.0",
  "event_id": "evt_test_001",
  "event_type": "module.event_type",
  "timestamp": "2026-03-30T14:30:00Z",
  "source": "test",
  "data": {
    "id": "test_001",
    "field1": "test_value"
  }
}

// Invalid message (missing required field)
{
  "schema_version": "1.0",
  "event_id": "evt_test_002",
  "event_type": "module.event_type",
  "timestamp": "2026-03-30T14:30:00Z",
  "source": "test",
  "data": {
    "id": "test_002"
    // Missing field1
  }
}
```