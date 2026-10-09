# Source control

Repository selected by the user on 2026-10-07: https://github.com/alexandergazzard-beep/Praetorian

The workspace root is the Git repository. The initial branch is `main`. Repository naming does not change the game's working title, Lost Vanguard.

Initial upload verified on 2026-10-07: project commit `c531b5892713f603d1a2b4ee72c850cb0ba6e9ac` matched GitHub main after a successful push. All 35 LFS objects uploaded (approximately 3.2 MB), and local LFS integrity passed. The branch tracks origin/main. A follow-up documentation commit records upload verification. No fresh clone or recovery test has been performed.

## What is included

Project records and story drafts, source scripts, Unreal project/configuration and saved Content assets, reference art, verification reports and screenshots, and shareable PDFs. Saved Unreal assets are versioned through Git LFS without changing their binary contents.

Git ignores Unreal Binaries, Intermediate, DerivedDataCache and Saved folders; local caches; temporary render files; virtual environments; credentials; and local assistant settings. Generated build summaries within Unreal/Saved are not backed up by Git. Durable verification reports in reports remain tracked. GitHub is one versioned project copy, not a backup of every local generated file or installed application.

## Routine updates

Save changed assets in Unreal first. From the project folder, use `git status`, `git add .`, `git commit -m "Describe the change"`, and `git push`. Review files before committing. The initial Git setup uses the existing configured author identity.

Git LFS stores game binaries separately from ordinary Git objects. Other machines need Git LFS installed and `git lfs pull` after cloning. LFS is configured locally and in .gitattributes; successful upload and ref comparison are required before recording the repository as pushed.

Git/Git LFS installed versions: Git 2.53.0.windows.1, Git LFS 3.7.1. LFS handling was checked against [GitHub's official documentation](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-git-large-file-storage).

Avoid force-pushes. Do not move or edit .uasset/.umap assets through filesystem operations; keep authoring in Unreal. Git versions the files saved by the editor.


## Combined environment upload readiness - 2026-10-08
Asset sources committed 736e32d; integration committed 8eda88e, followed by this documentation update. Active 5.8 project now tracked with terrain/vegetation and accepted movement. 1,358 files, 8.05 GiB working bytes; image sources now LFS alongside game/model binaries. Final LFS integrity passes; scan of 442 text files found no credential/signed-link patterns. All 41 gameplay checks pass. See COMBINED_ENVIRONMENT_REPORT.md.

Remote main remains 642db88 at latest inspection. Automatic approval review rejected large-asset upload because it requires explicit destination/payload authorization. Local work awaits that confirmation. Successful LFS upload and remote ref comparison are required before claiming a new push.


## GitHub storage rules checked - 2026-10-08
User explicitly approved the ~8GB combined project upload to Praetorian main after the automatic-review block. Push is running; completion/ref verification pending at this checkpoint.

Unique reachable Git LFS objects: 823, 8,563,798,539 bytes (7.98GiB). Working files:8.05GiB. Local ordinary Git loose objects about235MiB (includes history/unreferenced local objects; not a GitHub account usage reading).

Official GitHub [LFS billing](https://docs.github.com/en/billing/concepts/product-billing/git-lfs) states Free/Pro accounts include10GiB storage and10GiB download bandwidth per billing cycle, shared by the repository owner's account. Uploads do not count against download bandwidth; every changed binary version adds its entire file size to retained storage. Account plan, other repositories' usage and billing budget are unverified; no billing settings changed. [Repository limits](https://docs.github.com/en/repositories/creating-and-managing-repositories/repository-limits) recommends ordinary Git history under10GB and enforces100MB regular-file objects/2GB Git pushes. [LFS file limits](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-git-large-file-storage) are2GB/file for Free/Pro,4GB Team,5GB Enterprise Cloud; current largest file is about255MB. LFS assets are stored separately from the Git pack.


## Combined upload verified - 2026-10-08
User explicitly approved exact destination/payload. `git push origin main` completed successfully:786 new LFS objects,8.6GB reported uploaded, main642db88 to9ff877a. Live remote main exactly matched9ff877a57b7dc516d4edc7e1d014f20046fb346c; local `git lfs fsck` passed. Earlier pending/rejected entries are historical. This final documentation update is committed and pushed separately with another remote comparison. No fresh clone/full asset download performed, avoiding consumption of the account's download allowance. No billing settings changed.
