# Putting this on GitHub and building the apps

Written for someone who has not used GitHub before. Everything in a grey box is
typed into Terminal. `%` or `$` at the start of a line is the prompt — don't
type that part.

Where a box holds several lines, you can paste the whole thing at once; Terminal
runs each line in turn. And most of these commands print **nothing at all** when
they succeed — on the command line, silence is good news. Where a command does
produce output worth checking, it says so below.

## 1. One-time setup on your Mac

First check that git is installed. Run:

```
git --version
```

If it prints something like `git version 2.39.5`, you already have it — carry
on to the next block.

If instead a window pops up saying *"The 'git' command requires the command
line developer tools"*, macOS is offering to install them. Click **Install**,
accept the licence, and wait a few minutes. Nothing is printed in Terminal
while it downloads. When it finishes, run `git --version` again and it will
work. (This is Apple's own installer, not a third-party download.)

Tell git who you are. The email should be the one you use for GitHub.

You can paste all three lines at once — Terminal runs each as it reaches the
end of a line. **None of them prints anything.** That silence means they
worked; `git config` only speaks up when something is wrong.

```
git config --global user.name "Daniel Mechoulan"
git config --global user.email "you@example.com"
git config --global init.defaultBranch main
```

To see that it took, ask git to read the settings back:

```
git config --global --list
```

which should show your name, your email and `init.defaultbranch=main`.

## 2. Make the repository on github.com

1. Sign in at <https://github.com> (create the account first if needed).
2. Click **+** at the top right → **New repository**.
3. Repository name: `chidon-hapax-finder` — it must match the name already in
   `__init__.py`, or the link in the About box will be wrong.
4. Description: *Finds words and phrases that appear only once in a Tanach
   syllabus.*
5. **Public**. The GPL obliges you to make source available to anyone you give
   a binary to, and public is the simple way to satisfy that.
6. Do **not** tick "Add a README", "Add .gitignore" or "Choose a license" —
   you already have all three, and ticking them creates a conflict you would
   then have to untangle.
7. **Create repository.**

Leave that page open. It shows the URL you need next.

## 3. Push your files

In Terminal, from the folder containing `run.py`:

```
cd /path/to/chidon_hapax_finder
git init
git add .
git status
```

`git status` lists what will be saved. Check that `build/` and `dist/` are
**not** in the list — `.gitignore` excludes them, and they are hundreds of
megabytes of rebuildable output.

```
git commit -m "Chidon HaTanach Hapax Finder 1.0"
git remote add origin https://github.com/TheCodingMedStudent/chidon-hapax-finder.git
git branch -M main
git push -u origin main
```

The push asks for your GitHub username and password. **Your account password
will not work** — GitHub stopped accepting it years ago. You need a Personal
Access Token instead: github.com → your avatar → Settings → Developer settings
→ Personal access tokens → Tokens (classic) → Generate new token, tick
**repo**, generate, then copy it and paste it as the password. Copy it
somewhere safe; it is shown once.

Refresh the GitHub page and your files should be there.

## 4. Watch it build

Pushing triggers the workflow. Click the **Actions** tab. Three jobs run in
parallel — Windows, macOS Apple Silicon, macOS Intel — taking roughly five to
fifteen minutes.

Each one builds the app, then runs `--selftest` **inside the packaged app** to
prove the Tanach text really made it into the bundle. If a job goes red, click
it and read the failed step; the error is almost always in the last few lines.

When they finish, the built apps are at the bottom of the run page under
**Artifacts**. These are for checking. They expire after 90 days.

## 5. Publish a release

When you are happy, tag it:

```
git tag v1.0
git push origin v1.0
```

That runs the same three builds and then creates a **draft** release with all
three files attached. Go to the **Releases** tab, review it, write a sentence
about what it is, and press **Publish release**. Draft-by-default means nothing
becomes public by accident.

Your friends then download from the Releases page:

| Their computer | File |
| --- | --- |
| Windows | `Hapax Finder (Windows).zip` |
| Mac, 2020 or later | `Hapax Finder (Apple Silicon).dmg` |
| Mac, 2019 or earlier | `Hapax Finder (Intel).dmg` |

Unsure which Mac they have:  → About This Mac. "Apple M1" or later means
Apple Silicon; "Intel" means Intel.

## 6. Changing something later

```
git add .
git commit -m "what changed"
git push
```

For a new release, bump `__version__` in `chidon_hapax/__init__.py` and the
version numbers in `chidon_hapax.spec` and `version_info.txt`, then tag it
`v1.1` and push the tag as above.

## If a push is rejected

`! [rejected] ... fetch first` means the GitHub copy has something yours does
not — usually a file added through the website. Fix it with:

```
git pull --rebase origin main
git push
```
