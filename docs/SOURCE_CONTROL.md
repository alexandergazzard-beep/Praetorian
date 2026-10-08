# Source control

Repository selected by the user on 2026-10-07: https://github.com/alexandergazzard-beep/Praetorian

The workspace root is the Git repository. The initial branch is `main`. Repository naming does not change the game's working title, Lost Vanguard.

## What is included

Project records and story drafts, source scripts, Unreal project/configuration and saved Content assets, reference art, verification reports and screenshots, and shareable PDFs. Saved Unreal assets are versioned through Git LFS without changing their binary contents.

Git ignores Unreal Binaries, Intermediate, DerivedDataCache and Saved folders; local caches; temporary render files; virtual environments; credentials; and local assistant settings. Generated build summaries within Unreal/Saved are not backed up by Git. Durable verification reports in reports remain tracked. GitHub is one versioned project copy, not a backup of every local generated file or installed application.

## Routine updates

Save changed assets in Unreal first. From the project folder, use `git status`, `git add .`, `git commit -m "Describe the change"`, and `git push`. Review files before committing. The initial Git setup uses the existing configured author identity.

Git LFS stores game binaries separately from ordinary Git objects. Other machines need Git LFS installed and `git lfs pull` after cloning. LFS is configured locally and in .gitattributes; successful upload and ref comparison are required before recording the repository as pushed.

Git/Git LFS installed versions: Git 2.53.0.windows.1, Git LFS 3.7.1. LFS handling was checked against [GitHub's official documentation](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-git-large-file-storage).

Avoid force-pushes. Do not move or edit .uasset/.umap assets through filesystem operations; keep authoring in Unreal. Git versions the files saved by the editor.
