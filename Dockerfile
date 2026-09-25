# Internal base image and PyPI proxy follow the supplied DevX example.
# Confirm these endpoints and base-image availability with your platform team.
FROM nexus3.systems.uk.hsbc:18082/com/hsbc/fcr/gcp/forest/python3:3.12

USER root
WORKDIR /app
COPY nexus302.systems.uk.hsbc.crt /usr/local/share/ca-certificates/nexus302.crt
RUN update-ca-certificates && useradd -m -u 10001 appuser
COPY requirements.txt ./

# Compatibility with the documented Kaniko docker_args mechanism.
# Build arguments are not a secret-isolation mechanism; see README.
ARG NEXUS_PERSONAL_USERNAME
ARG NEXUS_PERSONAL_TOKEN
RUN python3 -c 'import os, urllib.parse; from pathlib import Path; u=urllib.parse.quote(os.environ["NEXUS_PERSONAL_USERNAME"], safe=""); p=urllib.parse.quote(os.environ["NEXUS_PERSONAL_TOKEN"], safe=""); Path("/tmp/demo-pip.conf").write_text("[global]\nindex-url = https://"+u+":"+p+"@nexus302.systems.uk.hsbc:8081/nexus/repository/pypi-proxy_n3p/simple\ncert = /etc/ssl/certs/ca-certificates.crt\n")' \
    && PIP_CONFIG_FILE=/tmp/demo-pip.conf python3 -m pip install --no-cache-dir --break-system-packages -r requirements.txt \
    && rm /tmp/demo-pip.conf

COPY app.py ./
COPY tests/ ./tests/
# A failing test fails the image build. No undocumented DevX test keys required.
RUN python3 -m unittest discover -s tests -v
USER appuser
ENV HOST=0.0.0.0 PORT=5010 PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
EXPOSE 5010
CMD ["python3", "app.py"]
