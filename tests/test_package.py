import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "product-manager"


class PackageTest(unittest.TestCase):
    def test_plugin_manifest_points_to_skills_directory(self):
        manifest = json.loads((ROOT / ".codex-plugin" / "plugin.json").read_text())
        self.assertEqual(manifest["name"], "product-manager")
        self.assertEqual(manifest["skills"], "./skills/")

    def test_skill_has_matching_name(self):
        skill = (SKILL_DIR / "SKILL.md").read_text()
        self.assertTrue(skill.startswith("---\nname: product-manager\n"))
        self.assertIn("## Select the lightest mode", skill)

    def test_expected_public_files_exist(self):
        expected = [
            SKILL_DIR / "agents" / "openai.yaml",
            SKILL_DIR / "references" / "component-versioning.md",
            SKILL_DIR / "references" / "product-sources.md",
            ROOT / "README.md",
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
