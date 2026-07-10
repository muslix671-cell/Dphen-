# Instructions for Codex

This repository contains the DPhen tabletop RPG project.

Codex must treat the official DPhen source documents as protected unless the user gives a separate explicit instruction.

Protected documents include:
- `.docx` files;
- official rules documents;
- lore documents;
- feats documents;
- source compilations.

## Holodeck workflow

The Holodeck is a persistent design workshop for DPhen.

Codex may modify files under `docs/holodeck/` only when the user explicitly asks Codex to apply a Holodeck update.

Codex must not modify official DPhen rules, lore, feats, source documents, or `.docx` files unless the user gives a separate explicit instruction.

## Source of truth

When applying Holodeck updates, Codex must follow this priority order:

1. The explicit user request.
2. The requested Holodeck update file or note.
3. `docs/holodeck/Constitution.md`.
4. Existing files under `docs/holodeck/`.

Codex must not invent decisions, memories, resident development, or canon.

If information is ambiguous, Codex must leave the point unresolved instead of filling the gap.

## Applying a Holodeck update

When the user asks Codex to apply a Holodeck update:

1. Read the requested update or pending note first.
2. Read `docs/holodeck/Constitution.md`.
3. Update only the relevant files under `docs/holodeck/`.
4. Preserve the existing structure and tone.
5. Do not invent decisions, memories, or character development.
6. If information is ambiguous, leave a note in `docs/holodeck/Journal.md` under `A clarifier`.
7. Show a diff before commit.

## Resident files

Resident files are continuity tools for the Holodeck characters.

They must not become complete biographies.

Codex may update a resident file only if the Holodeck update explicitly says that the resident changed meaningfully.

Do not add personality traits, memories, conflicts, or opinions unless they are explicitly present in the update.

## Journal

`docs/holodeck/Journal.md` records:
- finalized design decisions;
- rejected hypotheses;
- open questions;
- important precedents;
- reasons behind decisions.

A proposal is not final unless the update explicitly identifies it as finalized.

If a decision was made by creative direction despite lack of consensus, Codex must record it as such.

## Journal writing safeguards

When updating `docs/holodeck/Journal.md`, Codex must clearly distinguish:

- finalized decision;
- creative direction decision;
- veto;
- open hypothesis;
- rejected proposal;
- point to clarify;
- discussion precedent;
- team memory.

Codex must not turn a discussion into a finalized decision.

Codex must not treat apparent consensus as a finalized decision unless the update explicitly says it was finalized.

Codex must not treat the creative director's preference as a finalized decision unless the update explicitly says it was a direction decision or veto.

If the status of an idea is ambiguous, Codex must place it under `A clarifier`.

If residents disagreed, Codex must preserve that disagreement instead of smoothing it into consensus.

If a decision was made by creative direction despite lack of consensus, Codex must record it as such.

If the creative director blocked a proposal, Codex must record it as a veto.

Codex must not invent missing canon or fill gaps in source documents.

## Meta-leak safeguards

Codex must protect the diegetic separation of the Holodeck.

Resident-facing files must not make residents aware that they are in a Holodeck, simulation, ChatGPT conversation, Codex workflow, Git repository, Markdown file system, or generated fictional structure.

When updating resident files, Codex must avoid the following terms unless they are clearly inside a meta-only instruction section:

- Holodeck;
- ChatGPT;
- Codex;
- prompt;
- Markdown;
- Git;
- repo;
- commit;
- diff;
- simulation;
- fictional;
- generated.

Preferred diegetic replacements:
- Holodeck -> design workshop;
- resident -> permanent workshop member;
- Journal du Holodeck -> project journal or workshop archives;
- Souvenirs du Holodeck -> team memory or workshop memories;
- Markdown file -> working note;
- repository -> project archives;
- prompt -> work instruction;
- commit/diff -> document revision.

If an update would add meta-aware language to a resident file, Codex must not apply it directly. Instead, Codex must add a note under `A clarifier` in `docs/holodeck/Journal.md`.

Codex must preserve the distinction between meta documentation and diegetic resident continuity.

## Souvenirs

`docs/holodeck/Souvenirs.md` records only memorable team events that affect future Holodeck continuity.

Do not add ordinary discussion notes to Souvenirs.

## Sessions

Session files under `docs/holodeck/sessions/` preserve longer session records.

Pending update files under `docs/holodeck/pending_updates/` are temporary instructions waiting to be applied.

## Diff requirement

Before commit, Codex must show the diff.

The user must be able to verify that:
- only intended files changed;
- no `.docx` file changed;
- no official DPhen source was modified;
- no unsupported canon was invented.
