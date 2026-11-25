# Structurizr workspace guide

## Source policy

The active architecture sources are:

- `workspace.dsl` for the C4 model, relationships, views, and deployment model
- `docs/` for architecture documentation
- `adrs/` for architecture decisions

`workspace.dsl` is the only DSL entry point. The README explains the workflow. It is not an architecture source of truth.

`workspace.json` is a generated Structurizr Local runtime file. It contains a materialized copy of the model, imported documentation, decisions, generated identifiers, and local UI state. It is not an architecture source. It is ignored by Git and must not be committed. Structurizr Local regenerates it from `workspace.dsl`, `docs/`, and `adrs/`.

All accepted view definitions and layout rules must remain in `workspace.dsl`. Do not rely on an uncommitted manual layout that exists only in `workspace.json`.

The official project brief, TA clarifications, and machine-readable evaluation contracts can be used to verify the active architecture sources. Do not copy an unverified historical statement into the active architecture.

## Prerequisites

Install and start Docker Desktop before local validation.

## MCP workflow

Use this sequence for model changes:

1. Read `workspace.dsl` as UTF-8 text.
2. Keep the repository file unchanged.
3. If the hosted MCP rejects file-backed directives, remove only `!docs` and `!adrs` from the in-memory copy.
4. Run MCP parse.
5. Run MCP validate.
6. Run MCP inspect.
7. Correct all operational findings.
8. Export each active view only after the model is stable.

The two documentation findings that result from the in-memory directive removal are synthetic. Record them separately. Do not remove the directives from the repository file.

## Local viewing and validation

Structurizr Local can write the ignored `workspace.json` file in the mounted directory. The active sources remain unchanged.

Run these commands from the repository root in PowerShell:

```powershell
docker run --rm -it --name didrah-structurizr -p 8180:8080 -v "${PWD}/docs/Analytics:/usr/local/structurizr" structurizr/structurizr local
```

Open <http://localhost:8180>. Stop the server with `Ctrl+C`.

Port `8180` avoids the Windows port-exclusion range that can include port `8080`. Use another available host port when necessary. The container port remains `8080`.

Run CLI validation against the same source directory:

```powershell
docker run --rm -v "${PWD}/docs/Analytics:/usr/local/structurizr" structurizr/structurizr validate -workspace /usr/local/structurizr/workspace.dsl
```

A successful command returns without a validation error. Commit only accepted changes to `workspace.dsl`, `docs/`, `adrs/`, and other approved source artifacts. Do not commit the generated `workspace.json` file.

## Mermaid generation

Generate Mermaid only from active Structurizr view keys. For each MCP export response:

1. Read the JSON response.
2. Extract only the `definition` field.
3. Write the definition to the matching `.mmd` file.
4. Do not store the raw MCP JSON response.
5. Regenerate the complete active Artifact set after a view or relationship change.

Do not restore an old Mermaid file unless its matching view key is active.

## Documentation URL validation

Documented elements use this URL form:

```dsl
url "{workspace}/documentation/DIDRAH#<anchor>"
```

For each URL:

1. Confirm that the target anchor exists in `docs/`.
2. Confirm that the anchor is unique.
3. Open the link in Structurizr Local.
4. Confirm that the link selects the intended element section.

## Change rules

- Keep `!impliedRelationships false`.
- Keep stable view keys unless the approved plan requires a new view.
- Do not hand-edit generated artifacts as model sources.
- Do not change `workspace.json` to repair a DSL error. Correct the active sources and validate them. Structurizr Local regenerates the ignored runtime file.
- Validate the DSL, documentation links, ADR links, and protected-file hashes before a phase exits.

## Troubleshooting

- If the browser shows an old model, stop and restart the Local container.
- If Docker cannot mount the directory, check Docker Desktop's file sharing settings for the drive containing this repository.
- If the page is unavailable, confirm that the container is running and that the selected host port is published and free.
- If a diagram loses its layout, confirm that its view key did not change.
