# ChaosArmor Python Jenkins demo

Small Flask web app, served by Waitress on port 5010. No database required.
Scope: checkout -> container build -> dependency install -> four unit tests ->
image push to Nexus, using the existing DevX Jenkins shared pipeline.
The build creates an image; it does not host a running website.

## Run locally (optional before Jenkins)

Python 3.12 is the intended version. From this folder on Windows CMD:

```bat
py -3.12 -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python app.py
```

Linux / WSL:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python app.py
```

Open http://localhost:5010, http://localhost:5010/health and
http://localhost:5010/api/info. Stop with Ctrl+C.
For a corporate laptop, use your approved pip index and CA configuration.
Local execution is not a prerequisite for Jenkins to build the repository.

## Prepare the DevX Jenkins build

1. Extract the ZIP and put this folder's contents at the Python repository root.
   The root must contain app.py, requirements.txt, Dockerfile and ci-config.yaml.
2. Obtain the real internal CA certificate from your platform team. Add it at
   the repository root as `nexus302.systems.uk.hsbc.crt`, following your team's
   certificate distribution policy. It is deliberately not fabricated or bundled.
3. Replace these values in ci-config.yaml:

| Field | Required value |
|---|---|
| registry_nexus | Your team's writable Nexus **Docker** registry/path, following the DevX example's path convention |
| docker_args token value | Jenkins **Secret text** credential ID containing the Nexus token |
| docker_args username value | Jenkins **Secret text** credential ID containing the Nexus username |
| jenkins_credential_id | Credential ID in the Docker config JSON format required by DevX for image pull/push |

4. Confirm the internal Python base image, PyPI proxy URL, HTTPS proxy and CA
   match your environment. The supplied endpoints are transcribed from your
   screenshots and were not reachable/validated here. Use dependency versions
   available in your approved mirror; direct dependencies are pinned, but this
   sample is not a fully locked transitive dependency set.
5. Configure/onboard the repository with the same DevX job mechanism used for
   the frontend, pointing at the desired branch and root ci-config.yaml.
   Keep application deployment disabled in the job/platform settings.
6. Commit and push through your normal repository process, then trigger the
   Jenkins job (or let the configured webhook trigger it).
7. Check Console Output for dependency installation, four passing tests, image
   build and Nexus push. Look for the actual image reference in the build log.

Do not assume `ChaosArmorNexusSecret` from the frontend is suitable here: an npm
username/password credential is not automatically a Docker config JSON credential
or either of the two Secret text credentials used by this example.

## Configuration boundaries

The root ci-config.yaml follows the `build.container.build_type: kaniko` schema
visible in your supplied DevX screenshots. It intentionally omits the additional
GCR destination and includes no Kubernetes manifests or deployment commands.
The screenshots do not show whether your installed shared-library version makes
`registry_deploy` mandatory or what deployment defaults it applies. Confirm
Nexus-only support and deployment-disabled job settings before the first build;
no undocumented `deploy.enabled` key has been invented here.

Kaniko may run on the platform's existing Kubernetes-backed Jenkins agents.
You do not need to provision an application Kubernetes environment for this
sample. If you require no container build either, obtain the DevX Python
non-container build schema; these screenshots only document the Kaniko route.

A standalone Jenkinsfile is not included: ci-config.yaml is consumed by your
organization's existing shared pipeline. Plain Jenkins cannot interpret this
file by itself. The internal library bootstrap/onboarding definition was not
provided and has not been guessed.

## Credentials

Only credential IDs belong in YAML. The Dockerfile follows the screenshots'
build-argument credential contract but removes temporary pip configuration in
the same RUN instruction and never disables certificate verification.
Build arguments can still be exposed through builder metadata/logs/cache; use
this flow only under your platform's approved credential handling. For stronger
isolation ask the platform team for its supported secret injection mechanism;
do not assume BuildKit secret mounts work in Kaniko. Never commit tokens or
passwords. This ZIP contains neither credentials nor an internal CA certificate.

## Run the built image (optional, no Kubernetes)

On an authorized Docker host, authenticate to your registry using the approved
mechanism and run the exact image reference printed by Jenkins:

```bash
docker run --rm -p 127.0.0.1:5010:5010 YOUR_BUILT_IMAGE_REFERENCE
```

Then open http://localhost:5010. This is a manual demo run; persistent hosting
and deployment automation are outside this build-only sample.

## Verification

Run `python -m unittest discover -s tests -v` locally. The Dockerfile runs the
same tests during each image build. Actual internal Jenkins execution, image
build and Nexus authentication must be validated in your corporate environment.
"# chaosarmor-dryrun" 
