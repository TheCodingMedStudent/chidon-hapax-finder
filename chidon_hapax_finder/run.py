#!/usr/bin/env python3
"""Launcher: python run.py

    --selftest   load everything and exit, printing a summary. Used by the
                 build workflow to prove a packaged app actually works
                 before it is published.
"""
import sys


def selftest() -> int:
    from chidon_hapax import __version__, paths
    from chidon_hapax.corpus import corpus_path, load_corpus
    print(f"Hapax Finder {__version__}")
    print(f"  frozen      : {paths.frozen()}")
    print(f"  corpus path : {corpus_path()}")
    corpus = load_corpus()
    print(f"  corpus      : {len(corpus.books)} books, "
          f"{len(corpus.verses):,} verses")
    from chidon_hapax.syllabus import collect_verses, parse_syllabus_full
    from chidon_hapax.engine import Options, analyze
    parsed = parse_syllabus_full("יונה", corpus, lenient=True)
    res = analyze(corpus, collect_verses(parsed.ranges, corpus),
                  Options(max_n=1, include_n=(1,)))
    print(f"  analysis    : Jonah -> {res.per_n[1]} hapaxes "
          f"in {res.elapsed:.1f}s")
    assert res.per_n[1] == 49, f"expected 49, got {res.per_n[1]}"
    import os
    for name in ("style.qss", "icons/app.ico", "icons/icon_256.png"):
        p = paths.resource(*name.split("/"))
        assert os.path.exists(p), f"missing resource: {p}"
        print(f"  resource ok : {name}")
    print("SELFTEST PASSED")
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    from chidon_hapax.app import main
    main()
