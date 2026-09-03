import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "product-manager"
EXPECTED_SKILLS = {"product-manager", "product-roadmap", "product-requirements"}


class PackageTest(unittest.TestCase):
    def test_plugin_manifest_points_to_skills_directory(self):
        manifest = json.loads((ROOT / ".codex-plugin" / "plugin.json").read_text())
        self.assertEqual(manifest["name"], "product-manager")
        self.assertEqual(manifest["skills"], "./skills/")

    def test_package_exposes_all_product_capabilities(self):
        discovered = set()
        for path in (ROOT / "skills").glob("*/SKILL.md"):
            name_line = path.read_text().splitlines()[1]
            discovered.add(name_line.removeprefix("name: "))
        self.assertEqual(discovered, EXPECTED_SKILLS)

    def test_expected_public_files_exist(self):
        expected = [
            SKILL_DIR / "agents" / "openai.yaml",
            SKILL_DIR / "references" / "product-sources.md",
            ROOT / "skills/product-roadmap/agents/openai.yaml",
            ROOT / "skills/product-roadmap/references/roadmap-method.md",
            ROOT / "skills/product-requirements/agents/openai.yaml",
            ROOT / "skills/product-requirements/references/requirements-model.md",
            ROOT / "skills/product-requirements/assets/requirements-traceability.template.json",
            ROOT / "skills/product-requirements/scripts/check_requirements_traceability.py",
            ROOT / "README.md",
            ROOT / "README.zh-CN.md",
        ]
        for path in expected:
            self.assertTrue(path.is_file(), str(path))

    def test_package_does_not_contain_private_workspace_paths(self):
        forbidden = [
            "".join(("/Users/", "zita/")),
            "".join(("AI Workspace", " v0.1")),
            "".join(("World_model", "_research")),
        ]
        for path in ROOT.rglob("*"):
            if (
                path.is_file()
                and ".git" not in path.parts
                and "__pycache__" not in path.parts
            ):
                text = path.read_text(errors="ignore")
                for marker in forbidden:
                    self.assertNotIn(marker, text, f"{marker!r} found in {path}")


if __name__ == "__main__":
    unittest.main()
