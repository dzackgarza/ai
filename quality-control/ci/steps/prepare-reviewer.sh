#!/usr/bin/env bash
set -euo pipefail

CONTROL_REPO="${GITHUB_WORKSPACE:?GITHUB_WORKSPACE is required}"
REVIEWER_HOME="/home/reviewer"
REVIEWER_REPO="/home/reviewer/repo"
PRIVATE_TOOLS="/opt/ai-review/private"
PUBLIC_TOOLS="/opt/ai-review/bin"

sudo useradd -m -s /bin/bash reviewer || true

sudo rm -rf "$REVIEWER_REPO" "$PRIVATE_TOOLS" "$PUBLIC_TOOLS"
sudo mkdir -p "$REVIEWER_REPO" "$PRIVATE_TOOLS" "$PUBLIC_TOOLS"

# Private implementation tools. Reviewer must not read these.
sudo cp quality-control/ci/locked/submit-candidate "$PRIVATE_TOOLS/submit-candidate"
sudo cp quality-control/ci/locked/check-report.py "$PRIVATE_TOOLS/check-report.py"
sudo cp quality-control/ci/report-to-sarif.py "$PRIVATE_TOOLS/report-to-sarif.py"

sudo chown -R root:root "$PRIVATE_TOOLS"
sudo chmod 700 "$PRIVATE_TOOLS"
sudo chmod 500 "$PRIVATE_TOOLS/submit-candidate"
sudo chmod 400 "$PRIVATE_TOOLS/check-report.py"
sudo chmod 400 "$PRIVATE_TOOLS/report-to-sarif.py"

# Public command visible to reviewer. It contains no validation logic.
sudo tee "$PUBLIC_TOOLS/submit-candidate" >/dev/null <<'SH'
#!/usr/bin/env sh
set -eu
exec sudo -n --preserve-env=REPORT_TYPE,REVIEWER_REPO,CONTROL_REPO /opt/ai-review/private/submit-candidate "$@"
SH
sudo chown root:root "$PUBLIC_TOOLS/submit-candidate"
sudo chmod 755 "$PUBLIC_TOOLS/submit-candidate"

# Sudo rule: reviewer may run exactly the private submit command, nothing else.
{
  echo "reviewer ALL=(root) NOPASSWD: $PRIVATE_TOOLS/submit-candidate"
  echo "reviewer ALL=(root) NOPASSWD: $PRIVATE_TOOLS/submit-candidate *"
  echo "Defaults!$PRIVATE_TOOLS/submit-candidate env_keep += \"REPORT_TYPE REVIEWER_REPO CONTROL_REPO\""
} | sudo tee /etc/sudoers.d/ai-review-submit >/dev/null
sudo chmod 0440 /etc/sudoers.d/ai-review-submit
sudo visudo -c -f /etc/sudoers.d/ai-review-submit

# Sanitized reviewer checkout.
rsync -rlptD --delete \
  --no-owner --no-group \
  --exclude '.git' \
  --exclude '.github/workflows' \
  --exclude 'quality-control/ci' \
  --exclude '.review-report-artifact.json' \
  --exclude '.review-report-comment.md' \
  --exclude '.review-report.sarif' \
  "$CONTROL_REPO/" "$REVIEWER_REPO/"

mkdir -p "$REVIEWER_REPO/.agents/review-runner/candidates"
cp "$CONTROL_REPO/.reviewer-context.md" "$REVIEWER_REPO/.reviewer-context.md"

sudo chown -R reviewer:reviewer "$REVIEWER_REPO"
sudo mkdir -p "$REVIEWER_HOME/bin"
sudo ln -sf "$PUBLIC_TOOLS/submit-candidate" "$REVIEWER_HOME/bin/submit-candidate"
sudo chown -R reviewer:reviewer "$REVIEWER_HOME/bin"
