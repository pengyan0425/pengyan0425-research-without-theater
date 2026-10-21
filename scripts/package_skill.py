"""Build a reproducible, self-contained skill ZIP from the release sources."""
from hashlib import sha256
from pathlib import Path
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]


def main():
    skill = ROOT / "skills" / "research-without-theater"
    for required in ("SKILL.md", "LICENSE", "NOTICE", "agents/openai.yaml"):
        if not (skill / required).is_file():
            raise SystemExit(f"Missing installable resource: {required}")
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    output = ROOT / "dist" / f"research-without-theater-v{version}.zip"
    output.parent.mkdir(exist_ok=True)
    with ZipFile(output, "w", compression=ZIP_DEFLATED) as archive:
        for source in sorted(skill.rglob("*"), key=lambda path: path.relative_to(skill).as_posix()):
            if source.is_file():
                info = ZipInfo((Path(skill.name) / source.relative_to(skill)).as_posix(), (1980, 1, 1, 0, 0, 0))
                info.compress_type = ZIP_DEFLATED
                info.external_attr = 0o644 << 16
                archive.writestr(info, source.read_bytes())
    checksum = sha256(output.read_bytes()).hexdigest()
    (output.parent / "SHA256SUMS").write_text(f"{checksum}  {output.name}\n", encoding="utf-8")
    print(f"{output.relative_to(ROOT)}  sha256={checksum}")


if __name__ == "__main__":
    main()
