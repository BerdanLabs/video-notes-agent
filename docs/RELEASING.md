# Releasing

This project publishes Python distributions from GitHub releases.

## One-time PyPI setup

1. Create the `video-notes-agent` project on PyPI.
2. Configure PyPI trusted publishing for:
   - Owner: `BerdanLabs`
   - Repository: `video-notes-agent`
   - Workflow: `release.yml`
   - Environment: `pypi`
3. In GitHub, create the `pypi` environment. Add manual approval if the project wants a release gate.

No PyPI password or API token is needed when trusted publishing is configured.

## Release checklist

1. Confirm CI is green on `main`.
2. Update `pyproject.toml` version.
3. Run:

```bash
python -m pip install -e ".[dev]"
python -m pytest
python -m build
python -m twine check dist/*
```

4. Commit the version change.
5. Create and push a tag:

```bash
git tag v0.1.0
git push origin v0.1.0
```

6. Draft a GitHub release from that tag. Publishing the release triggers PyPI publication.

The tag build uploads package artifacts to GitHub Actions. The release publish step uploads those
artifacts to PyPI.
