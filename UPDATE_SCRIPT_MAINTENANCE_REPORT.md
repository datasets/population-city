## Update Script Maintenance Report

Date: 2026-03-04

- Root cause: automation used broad triggers and had no explicit workflow write permissions.
- Fixes made: narrowed workflow to schedule + manual dispatch, upgraded action versions, added `permissions: contents: write`, and preserved commit paths for generated files.
- Validation: reviewed workflow run sequence and staged-file scope (`data`, `datapackage.json`, `README.md`).
- Known blockers: none identified in this remediation pass.
