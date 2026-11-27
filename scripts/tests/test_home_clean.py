import io
import json
import os
import shutil
import subprocess
import tarfile
import tempfile
import time
import unittest
from pathlib import Path


class SageCleanupTest(unittest.TestCase):
    def test_home_recipe_preserves_recently_used_project_cache(self):
        project = Path(__file__).resolve().parents[2]
        just = shutil.which("just")
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            volume = root / ".local/share/docker/volumes/sage-repos/_data"
            repo = volume / "project"
            subprocess.run(["git", "init", "-q", repo], check=True)
            clones = root / "gitclones"
            clones.mkdir()
            (clones / "project").symlink_to(repo)
            scratch = root / "tmp"
            scratch.mkdir()
            old = time.time() - 2 * 86400
            for name in (".ruff_cache", ".pytest_cache"):
                cache = repo / name
                cache.mkdir()
                tag = cache / "CACHEDIR.TAG"
                tag.write_bytes(b"Signature: 8a477f597d28d172789f06886806bc55\n")
                entry = cache / "entries"
                entry.write_text("existing result")
                os.utime(tag, (old, old))
                os.utime(cache, (old, old))
                if name == ".pytest_cache":
                    os.utime(entry, (old, old))
            env = dict(os.environ, HOME=folder, TMPDIR=str(scratch), REPO=str(project), PATH="/usr/bin:/bin")
            subprocess.run([just, "-f", project / "home-justfile", "clean"], env=env, check=True)
            self.assertTrue((repo / ".ruff_cache/entries").is_file())
            self.assertFalse((repo / ".pytest_cache").exists())

    def test_sage_cleanup(self):
        script = Path(__file__).resolve().parents[1] / "home-clean"
        docker = shutil.which("docker") or Path.home() / "bin/docker"
        client = [docker, "--host", f"unix:///run/user/{os.getuid()}/docker.sock"]
        image = subprocess.check_output(
            [*client, "inspect", "sage-research", "--format", "{{.Image}}"], text=True
        ).strip()
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            home = root / "home"
            archives = home / ".cache/mathlib"
            archives.mkdir(parents=True)
            warm = archives / "0123456789abcdef.ltar"
            warm.write_bytes(b"cached archive")
            downloads = root / "elan/tmp"
            downloads.mkdir(parents=True)
            stream = io.BytesIO()
            with tarfile.open(fileobj=stream, mode="w") as bundle:
                bundle.addfile(tarfile.TarInfo("lean/toolchain"))
            compressed = subprocess.check_output(["zstd", "-qc"], input=stream.getvalue())
            stale = downloads / "b8lgfuw3oq94j8y7_file"
            recent = downloads / "k8lgfuw3oq94j8y7_file"
            opened = downloads / "q8lgfuw3oq94j8y7_file"
            other = downloads / "release-notes"
            for path in (stale, recent, opened, other):
                path.write_bytes(compressed)
            scratch = root / "tmp"
            scratch.mkdir()
            metadata = scratch / "tmp.XXabc123"
            metadata.write_text(json.dumps({"dynlibs": ["/lib/" + "x" * 300], "importArts": {}}))
            old = time.time() - 2 * 86400
            for path in (stale, other, opened, metadata):
                os.utime(path, (old, old))

            repo = root / "repos/project"
            subprocess.run(["git", "init", "-q", repo], check=True)
            git = ["git", "-C", repo]
            subprocess.run([*git, "config", "maintenance.loose-objects.auto", "1"], check=True)
            content = b"unpublished research input"
            oid = subprocess.check_output([*git, "hash-object", "-w", "--stdin"], input=content).strip().decode()
            subprocess.run([*git, "hash-object", "-w", "--stdin"], input=b"second object", stdout=subprocess.DEVNULL, check=True)
            loose = repo / ".git/objects" / oid[:2] / oid[2:]
            self.assertTrue(loose.is_file())
            for tool in ("trash", "trash-empty"):
                body = Path(shutil.which(tool)).read_bytes().split(b"\n", 1)[1]
                entry = root / tool
                entry.write_bytes(b"#!/sage/.venv/bin/python\n" + body)
                entry.chmod(0o755)
            command = [
                *client, "run", "--rm", "--pull=never", "--network=none", "--read-only",
                "-v", f"{root}:/fixture", "-v", f"{root / 'repos'}:/repos",
                "-v", f"{script}:/clean:ro",
                "-v", "/usr/lib/python3/dist-packages/trashcli:/tools/trashcli:ro",
                "-e", "HOME=/fixture/home", "-e", "ELAN_HOME=/fixture/elan",
                "-e", "TMPDIR=/fixture/tmp", "-e", "PYTHONPATH=/tools",
                "-e", "PATH=/fixture:/usr/local/bin:/usr/bin:/bin", "-e", "UV_CACHE_DIR=/fixture/uv",
                "--entrypoint", "/bin/sh", image, "-c",
                'exec /sage/.venv/bin/python /clean --sage 3<"$ELAN_HOME/tmp/$1"', "sh", opened.name,
            ]
            subprocess.run(command, check=True)
            for path in (stale, metadata, loose):
                with self.subTest(removed=path.relative_to(root)):
                    self.assertFalse(path.exists())
            with self.subTest(preserved="Mathlib cache"):
                self.assertTrue(warm.is_file())
                self.assertEqual(warm.read_bytes(), b"cached archive")
            self.assertEqual(subprocess.check_output([*git, "cat-file", "blob", oid]), content)
            self.assertEqual(recent.read_bytes(), compressed)
            self.assertEqual(opened.read_bytes(), compressed)
            self.assertEqual(other.read_bytes(), compressed)


if __name__ == "__main__":
    unittest.main()
