"""
Check Git Status
Overí či sú všetky zmeny pushnuté na GitHub
"""

import subprocess


def run_git_command(args: list) -> tuple[bool, str]:
    """Spusti git príkaz"""
    try:
        result = subprocess.run(
            ["git"] + args,
            capture_output=True,
            text=True,
            check=True,
            cwd="C:/Development/nex-automat",
        )
        return True, result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return False, e.stderr.strip()


def check_git_status():
    """Skontroluj Git status"""
    print("=" * 80)
    print("GIT STATUS")
    print("=" * 80)
    print()

    success, output = run_git_command(["status", "--short"])

    if not success:
        print("❌ Git status failed!")
        print(output)
        return False

    if output:
        print("⚠️  Uncommitted changes:")
        print(output)
        print()
    else:
        print("✅ Working directory clean (no uncommitted changes)")
        print()

    return True


def check_current_branch():
    """Skontroluj aktuálnu branch"""
    print("=" * 80)
    print("CURRENT BRANCH")
    print("=" * 80)
    print()

    success, output = run_git_command(["branch", "--show-current"])

    if success:
        print(f"Current branch: {output}")
        print()
        return output
    else:
        print("❌ Could not determine current branch")
        return None


def check_remote_url():
    """Skontroluj remote URL"""
    print("=" * 80)
    print("REMOTE REPOSITORY")
    print("=" * 80)
    print()

    success, output = run_git_command(["remote", "-v"])

    if success:
        print(output)
        print()

        # Extract GitHub URL
        for line in output.split("\n"):
            if "github.com" in line and "(push)" in line:
                parts = line.split()
                if len(parts) >= 2:
                    github_url = parts[1]
                    print(f"✅ GitHub repository: {github_url}")
                    print()
                    return True

        print("⚠️  No GitHub remote found")
        print()
        return False
    else:
        print("❌ Could not get remote info")
        return False


def check_last_commits():
    """Zobraz posledné commits"""
    print("=" * 80)
    print("LAST 5 COMMITS (LOCAL)")
    print("=" * 80)
    print()

    success, output = run_git_command(["log", "--oneline", "--decorate", "-5"])

    if success:
        print(output)
        print()
    else:
        print("❌ Could not get commit log")


def check_unpushed_commits():
    """Skontroluj nepushnuté commits"""
    print("=" * 80)
    print("UNPUSHED COMMITS")
    print("=" * 80)
    print()

    # Get current branch
    success, branch = run_git_command(["branch", "--show-current"])
    if not success:
        print("❌ Could not determine current branch")
        return

    # Check unpushed commits
    success, output = run_git_command(["log", f"origin/{branch}..HEAD", "--oneline"])

    if not success:
        print(f"⚠️  Could not compare with origin/{branch}")
        print("   Maybe branch not pushed yet?")
        print()

        # Try to show all local commits
        print("Showing all local commits:")
        success2, output2 = run_git_command(["log", "--oneline", "-5"])
        if success2:
            print(output2)
        print()
        return

    if output:
        print(f"⚠️  Found {len(output.splitlines())} unpushed commit(s):")
        print(output)
        print()
        print("❌ COMMITS NOT PUSHED TO GITHUB!")
        print()
        return False
    else:
        print("✅ All commits are pushed to GitHub")
        print()
        return True


def check_remote_commits():
    """Skontroluj commits na GitHub"""
    print("=" * 80)
    print("REMOTE COMMITS (GITHUB)")
    print("=" * 80)
    print()

    # First, fetch latest info from GitHub
    print("Fetching latest info from GitHub...")
    success, _ = run_git_command(["fetch", "origin"])

    if not success:
        print("❌ Could not fetch from GitHub")
        print("   Check internet connection")
        print()
        return

    print("✅ Fetch successful")
    print()

    # Get current branch
    success, branch = run_git_command(["branch", "--show-current"])
    if not success:
        print("❌ Could not determine current branch")
        return

    # Show last 5 commits on GitHub
    success, output = run_git_command(["log", f"origin/{branch}", "--oneline", "-5"])

    if success:
        print(f"Last 5 commits on GitHub (origin/{branch}):")
        print(output)
        print()
    else:
        print(f"⚠️  Could not get commits from origin/{branch}")
        print()


def compare_local_remote():
    """Porovnaj local a remote"""
    print("=" * 80)
    print("LOCAL vs REMOTE COMPARISON")
    print("=" * 80)
    print()

    # Get current branch
    success, branch = run_git_command(["branch", "--show-current"])
    if not success:
        print("❌ Could not determine current branch")
        return

    # Fetch
    run_git_command(["fetch", "origin"])

    # Get local HEAD commit
    success, local_commit = run_git_command(["rev-parse", "HEAD"])
    if not success:
        print("❌ Could not get local commit")
        return

    # Get remote HEAD commit
    success, remote_commit = run_git_command(["rev-parse", f"origin/{branch}"])
    if not success:
        print(f"⚠️  Could not get remote commit for origin/{branch}")
        print()
        return

    print(f"Local HEAD:  {local_commit[:8]}")
    print(f"Remote HEAD: {remote_commit[:8]}")
    print()

    if local_commit == remote_commit:
        print("✅ LOCAL and REMOTE are IN SYNC")
        print()
        return True
    else:
        print("❌ LOCAL and REMOTE are OUT OF SYNC")
        print()
        print("Local is ahead or behind remote.")
        print("Check UNPUSHED COMMITS section above.")
        print()
        return False


def show_push_command():
    """Zobraz príkaz na push"""
    print("=" * 80)
    print("HOW TO PUSH")
    print("=" * 80)
    print()

    # Get current branch
    success, branch = run_git_command(["branch", "--show-current"])
    if not success:
        branch = "main"

    print("To push your commits to GitHub, run:")
    print()
    print(f"  git push origin {branch}")
    print()
    print("Or in PyCharm: VCS → Git → Push (Ctrl+Shift+K)")
    print()


def main():
    """Main execution"""

    print("=" * 80)
    print("NEX AUTOMAT - GIT STATUS CHECK")
    print("=" * 80)
    print()

    # Run checks
    check_git_status()
    branch = check_current_branch()
    check_remote_url()
    check_last_commits()

    # Critical checks
    unpushed_ok = check_unpushed_commits()
    check_remote_commits()
    sync_ok = compare_local_remote()

    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print()

    if unpushed_ok and sync_ok:
        print("✅ Everything is pushed to GitHub")
        print("✅ Local and remote are in sync")
        print()
        print("🎉 All good!")
    elif unpushed_ok is False:
        print("❌ You have unpushed commits")
        print()
        show_push_command()
    elif sync_ok is False:
        print("❌ Local and remote are out of sync")
        print()
        show_push_command()
    else:
        print("⚠️  Could not determine sync status")
        print("   Check the output above for details")
        print()

    print("=" * 80)


if __name__ == "__main__":
    main()
