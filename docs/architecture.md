# pipeline-runner architecture

This document describes how **pipeline-runner** is structured. The system is split into four main layers that communicate through well-defined interfaces.

## Core layer

The **core** layer owns the execution model: pipelines, steps, scheduling, and the state machine that tracks each run. It does not know about HTTP or disk layout; it exposes hooks and events so upper layers can observe progress.

## API layer

The **API** layer exposes pipeline operations over HTTP (REST). It maps requests to core commands, serializes responses, and enforces request validation. Long-running work is handed off to workers rather than blocking request threads.

## Workers layer

The **workers** layer runs jobs asynchronously: pulling work from a queue, executing steps in isolated processes or containers, and reporting status back to core. Scaling is horizontal by adding worker processes.

## Storage layer

The **storage** layer abstracts artifacts and metadata: local filesystem, object storage (e.g. S3-compatible), and small caches. Core and workers read/write through this layer so backends can be swapped without changing execution logic.
