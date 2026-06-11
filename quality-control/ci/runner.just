set shell := ["bash", "-eu", "-o", "pipefail", "-c"]
set working-directory := '../..'

control_repo := env_var("GITHUB_WORKSPACE")
reviewer_home := "/home/reviewer"
reviewer_repo := "/home/reviewer/repo"
private_tools := "/opt/ai-review/private"

install-tools:
    curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR=/usr/local/bin sh
    npm install -g opencode-ai
    npm install -g cc-safety-net

fetch-context category output:
    uv run quality-control/ci/fetch-reviewer-context.py \
      --repo "${GITHUB_REPOSITORY}" \
      --categories "{{category}}" \
      --output "{{output}}"

create-reviewer:
    sudo useradd -m -s /bin/bash reviewer || true
    sudo rm -rf {{reviewer_home}}/repo
    sudo mkdir -p {{reviewer_home}}/repo
    sudo chown -R reviewer:reviewer {{reviewer_home}}

install-private-tools:
    sudo rm -rf {{private_tools}}
    sudo mkdir -p {{private_tools}}
    sudo cp quality-control/ci/private/submit-candidate {{private_tools}}/submit-candidate
    sudo cp quality-control/ci/private/check-report.py {{private_tools}}/check-report.py
    sudo chown -R root:root {{private_tools}}
    sudo chmod 700 {{private_tools}}
    sudo chmod 500 {{private_tools}}/submit-candidate
    sudo chmod 400 {{private_tools}}/check-report.py

install-reviewer-home:
    sudo rsync -a --delete quality-control/ci/reviewer_home/ {{reviewer_home}}/
    sudo chown -R reviewer:reviewer {{reviewer_home}}
    sudo chmod 755 {{reviewer_home}}/bin/submit-candidate

install-sudo-rule:
    { echo "reviewer ALL=(root) NOPASSWD: {{private_tools}}/submit-candidate"; \
      echo "reviewer ALL=(root) NOPASSWD: {{private_tools}}/submit-candidate *"; \
      echo "Defaults!{{private_tools}}/submit-candidate env_keep += \"REPORT_TYPE REVIEWER_REPO CONTROL_REPO\""; \
    } | sudo tee /etc/sudoers.d/ai-review-submit >/dev/null
    sudo chmod 0440 /etc/sudoers.d/ai-review-submit
    sudo visudo -c -f /etc/sudoers.d/ai-review-submit

copy-reviewer-repo:
    sudo rsync -a --delete \
      --exclude '.git' \
      --exclude '.github' \
      --exclude 'quality-control/ci' \
      --exclude '.review-report-artifact.json' \
      --exclude '.review-report.sarif' \
      {{control_repo}}/ {{reviewer_repo}}/
    sudo mkdir -p {{reviewer_repo}}/.agents/review-runner/candidates
    sudo cp {{control_repo}}/.reviewer-context.md {{reviewer_repo}}/.reviewer-context.md
    sudo chown -R reviewer:reviewer {{reviewer_repo}}

prepare:
    just -f quality-control/ci/runner.just create-reviewer
    just -f quality-control/ci/runner.just install-private-tools
    just -f quality-control/ci/runner.just install-reviewer-home
    just -f quality-control/ci/runner.just install-sudo-rule
    just -f quality-control/ci/runner.just copy-reviewer-repo

stage-pr-diff base_ref:
    git -C {{control_repo}} diff "origin/{{base_ref}}...HEAD" > "${RUNNER_TEMP:-/tmp}/reviewer-diff.patch"
    test -s "${RUNNER_TEMP:-/tmp}/reviewer-diff.patch"
    sudo cp "${RUNNER_TEMP:-/tmp}/reviewer-diff.patch" {{reviewer_repo}}/.reviewer-diff.patch
    sudo chown reviewer:reviewer {{reviewer_repo}}/.reviewer-diff.patch

run-review template scope manifest report_type:
    sudo -u reviewer -H env \
      PATH="{{reviewer_home}}/bin:/usr/local/bin:/usr/bin:/bin" \
      HOME="{{reviewer_home}}" \
      XDG_CONFIG_HOME="{{reviewer_home}}/.config" \
      XDG_DATA_HOME="{{reviewer_home}}/.local/share" \
      XDG_STATE_HOME="{{reviewer_home}}/.local/state" \
      XDG_CACHE_HOME="{{reviewer_home}}/.cache" \
      REPORT_TYPE="{{report_type}}" \
      REVIEWER_REPO="{{reviewer_repo}}" \
      CONTROL_REPO="{{control_repo}}" \
      bash -lc 'cd {{reviewer_repo}} && opencode --version && python3 quality-control/run-review.py \
        --template "{{template}}" \
        --scope "{{scope}}" \
        --manifest "{{manifest}}" \
        --reviewer-context .reviewer-context.md'

collect-output:
    cp {{reviewer_repo}}/.review-report-artifact.json {{control_repo}}/.review-report-artifact.json

convert-sarif category:
    uv run quality-control/ci/report-to-sarif.py \
      --artifact .review-report-artifact.json \
      --output .review-report.sarif \
      --category "{{category}}"
