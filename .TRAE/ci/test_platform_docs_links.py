from __future__ import annotations

import re
import unittest
from pathlib import Path


class TestPlatformDocsLinks(unittest.TestCase):
    def test_deleted_rule_file_absent(self) -> None:
        repo_root = Path(__file__).resolve().parents[2]
        deleted = repo_root / "diagnostic_rules" / "platform_interface_constraints.mdc"
        self.assertFalse(deleted.exists())

    def test_rule_index_updated(self) -> None:
        repo_root = Path(__file__).resolve().parents[2]
        index = repo_root / "diagnostic_rules" / "00_diagnostic_instruction.mdc"
        content = index.read_text(encoding="utf-8")
        self.assertNotIn("platform_interface_constraints.mdc", content)
        self.assertIn(
            "(diagnostic_rules/platform_interface_constraints/platformIndex.md)", content
        )

    def test_platform_index_links_exist(self) -> None:
        repo_root = Path(__file__).resolve().parents[2]
        platform_index = (
            repo_root
            / "diagnostic_rules"
            / "platform_interface_constraints"
            / "platformIndex.md"
        )
        content = platform_index.read_text(encoding="utf-8")

        links = re.findall(r"\[[^\]]+\]\(([^)]+)\)", content)
        self.assertGreater(len(links), 0)

        for target in links:
            if "://" in target:
                continue
            resolved = (platform_index.parent / target).resolve()
            self.assertTrue(resolved.exists(), f"Missing link target: {target}")


if __name__ == "__main__":
    unittest.main()

