# pipeline-runner architecture

**pipeline-runner** is organized into layers and feature modules with clear boundaries.

## Core layer

The **core** layer owns pipelines, steps, scheduling, and the run state machine. It exposes hooks and events so other layers observe progress without coupling to HTTP or storage.

## API layer

The **API** layer serves REST endpoints, maps requests to core operations, validates input, and defers long work to workers so request threads stay responsive.

## Workers layer

**Workers** dequeue jobs, run steps in isolated processes or containers, and report status to core. Add processes to scale horizontally.

## Storage layer

**Storage** abstracts artifacts and metadata (filesystem, object stores, caches) so backends can change without touching execution logic.

## Auth module

**Auth** covers API tokens, service accounts, and scoped permissions. Middleware attaches identity before handlers run.

## Notifications module

**Notifications** delivers webhooks, email, and chat alerts on lifecycle events by subscribing to core events.

## CLI module

The **CLI** offers commands to submit runs, tail logs, and inspect status for local dev and ops without raw HTTP.

## Plugins module

**Plugins** loads custom step types and hooks via entry points and registers them like built-ins.
