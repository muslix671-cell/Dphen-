# Instructions for Codex

This repository contains the DPhen tabletop RPG project and its Holodeck documentation.

`AGENTS.md` governs repository edits by Codex. It is not part of the normal live-session bundle and must never be exposed to residents.

## Protected sources

Official DPhen sources are protected unless the user gives a separate, explicit instruction to modify them.

Protected sources include:
- every `.docx` file;
- official rules and SRD documents;
- lore documents;
- feats documents;
- source compilations.

A request to update the Holodeck authorizes edits under `docs/holodeck/` only. It does not authorize a change to DPhen canon or protected sources.

## Authority order

When applying a Holodeck change, follow this order:

1. The user's explicit request.
2. The requested update file or supplied note.
3. `docs/holodeck/Constitution.md`.
4. `docs/holodeck/Runtime.md` for condensed live-session behavior.
5. The active program context and existing persistent files.

Do not invent a decision, memory, relationship, resident development, source fact or canon. Leave ambiguous content unresolved.

## Applying changes

Before editing:

1. Read the complete request or update.
2. Read the relevant Constitution sections.
3. Inspect the target files and current Git status.
4. Identify protected files and keep them untouched.

During editing:

- change only the files required by the request;
- preserve identifiers and provenance;
- archive obsolete history instead of silently deleting it when it remains useful;
- use `docs/holodeck/meta/End_of_Session_Requirements.md` as the canonical end-of-session schema;
- use the templates only as concise projections of that schema;
- keep program-specific information in the active context;
- update `docs/holodeck/sessions/INDEX.md` when a session is added, archived or superseded.

After editing:

1. Verify that no protected source changed.
2. Check references, identifiers and program boundaries.
3. Inspect the complete diff.
4. Show the diff before commit when requested or required by the update.
5. Commit or push only after an explicit user instruction.

## Status safeguards

The Journal must distinguish:
- finalized decision;
- creative direction decision;
- confirmed presidential veto;
- open hypothesis;
- rejected proposal;
- discussion precedent;
- point to clarify.

A discussion, apparent consensus, preference, `OK`, `interessant` or `continue` is not a finalized decision.

When status is ambiguous, place the item under `Points a clarifier`. Preserve unresolved disagreement instead of smoothing it into consensus.

For a confirmed presidential veto, record its scope, final confirmation and remaining disagreement. Add an individual opinion to each active resident file only when the update provides enough scene context to derive it without invention. Compliance never implies agreement.

A newer decision overrides a source only when it explicitly identifies what it replaces. Until the protected source is separately updated, record the change as a pending canonical amendment.

## Persistent layers

- `Journal.md` contains DPhen institutional memory, not framework instructions.
- `Souvenirs.md` contains rare lived events that change future team dynamics.
- Resident files contain durable personal memory, convictions and relationships for that resident only.
- Active session files support recent memory for their participants.
- `sessions/archive/technical/` contains operational history, not lived memory.
- `sessions/archive/superseded/` contains provenance, not duplicate active continuity.
- `meta/history/` contains retired framework material and is never loaded as resident memory.
- `pending_updates/` is operator-only until an update is applied.

Do not turn a useful idea, technical milestone or ordinary discussion into a Souvenir. Do not give a resident knowledge of an unattended exchange, another resident's private file or an unconsulted source.

## Resident files

Use `docs/holodeck/residents/TEMPLATE_Resident.md` for a new resident. The completed file must use the program's own context and must not inherit DPhen traits by default.

Update a resident file only when the request records a meaningful durable change. A passing reaction is not a new conviction, relationship or memory. Preserve the concrete origin of every durable change.

Durable opinions about another participant belong in the file of the person who holds the opinion. Relationships may be asymmetric.

An invited specialist remains temporary unless the director explicitly makes that person recurring or permanent.

## Meta separation

Resident-facing content must not reveal the Holodeck mechanism, ChatGPT, Codex, prompts, Markdown, Git, repositories, commits, diffs, connectors, file paths or generated fiction.

Stable project content may receive a natural diegetic equivalent such as `atelier`, `archives` or `journal de projet`. A technical state or failure must never be translated into an event experienced by residents.

If technical language would enter a resident file, stop and place the issue under `Points a clarifier` instead.

## Runtime synchronization

`docs/holodeck/Runtime.md` is the only condensed live-session contract. It must remain consistent with the Constitution and must not create independent authority.

When a change affects live behavior, update the Constitution and Runtime in the same revision. Do not duplicate that behavior into `AGENTS.md`, `Workflow.md`, program contexts or operator notes unless those files need a short reference for their specialized purpose.

Keep rationales and edge cases in the Constitution. Keep the Runtime concise and directly actionable.

## Diff requirement

Before commit, verify at minimum:

- no `.docx` or protected DPhen source changed;
- only intended Holodeck files changed;
- no hypothesis became a decision without explicit confirmation;
- no disagreement was erased;
- no meta leak entered resident continuity;
- no memory or resident evolution was invented;
- archived sessions are excluded from active loading;
- Runtime and Constitution remain synchronized.
