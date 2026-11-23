# Structurizr workspace guide

## Source policy

The active architecture sources are:

- `workspace.dsl` for the C4 model, relationships, views, and deployment model
- `docs/` for architecture documentation
- `adrs/` for architecture decisions

`workspace.dsl` is the only DSL entry point. The README explains the workflow. It is not an architecture source of truth.

`workspace.json` is the generated Structurizr Local snapshot. It contains the imported model, documentation, decisions, and layout data. Do not edit it by hand. Regenerate and commit it after an accepted change to `workspace.dsl`, `docs/`, or `adrs/` so that a direct local mount shows the same accepted sources.

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

## Safe local validation

Structurizr Local can write layout data. Run it against a temporary copy so that it cannot change the repository `workspace.json`.

Run these commands from the repository root in PowerShell:

```powershell
$structurizrTemp = Join-Path ([IO.Path]::GetTempPath()) ([IO.Path]::GetRandomFileName())
New-Item -ItemType Directory -Path $structurizrTemp | Out-Null
Copy-Item -Recurse -Path "${PWD}/docs/Analytics/*" -Destination $structurizrTemp
Remove-Item -LiteralPath (Join-Path $structurizrTemp "workspace.json") -ErrorAction SilentlyContinue
docker run --rm -it -p 8080:8080 -v "${structurizrTemp}:/usr/local/structurizr" structurizr/structurizr local
```

Open <http://localhost:8080>. Stop the server with `Ctrl+C`.

Run CLI validation against the same temporary copy:

```powershell
docker run --rm -v "${structurizrTemp}:/usr/local/structurizr" structurizr/structurizr validate -workspace /usr/local/structurizr/workspace.dsl
```

A successful command returns without a validation error. After visual and CLI validation, stop Structurizr Local and copy the generated `workspace.json` from the temporary directory to `docs/Analytics/workspace.json`. Review it and commit it with the accepted source changes or in an immediately following generated-artifact commit.

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
- Do not change `workspace.json` to repair a DSL error. Correct the active sources, validate them, and then regenerate the snapshot.
- Validate the DSL, documentation links, ADR links, and protected-file hashes before a phase exits.

## Troubleshooting

- If the browser shows an old model, stop and restart the temporary Local container.
- If Docker cannot mount the directory, check Docker Desktop's file sharing settings for the drive containing this repository.
- If the page is unavailable, confirm that the container is running and that port 8080 is free.
- If a diagram loses its layout, confirm that its view key did not change.
