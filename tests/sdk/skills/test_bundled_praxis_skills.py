"""Owned defaults must load without cloning any external repository."""

from openhands.sdk.skills import skill as skill_module, utils as utils_module


def test_default_skills_are_bundled_without_git(monkeypatch, tmp_path):
    def unexpected_clone(*args, **kwargs):
        raise AssertionError("Bundled defaults must not contact a repository")

    monkeypatch.setattr(utils_module, "try_cached_clone_or_update", unexpected_clone)
    monkeypatch.setattr(skill_module, "get_skills_cache_dir", lambda: tmp_path)
    skill_module._invalidate_public_skills_cache()
    skills = skill_module.load_public_skills()
    assert len(skills) == 12
    assert "bundled:praxis" == skill_module.PUBLIC_SKILLS_REPO
    assert (tmp_path / "praxis-bundles").is_dir()
    assert skill_module.load_public_skills() == skills
