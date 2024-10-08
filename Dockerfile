# If you need Python 3 and the GitHub CLI, then use:
FROM cicirello/pyaction:4

# If all you need is Python 3, use:
# FROM cicirello/pyaction-lite:3

# If Python 3 + git is sufficient, then use:
# FROM cicirello/pyaction:3

# To pull from the GitHub Container Registry instead, use one of these:
# FROM ghcr.io/cicirello/pyaction-lite:3
# FROM ghcr.io/cicirello/pyaction:4
# FROM ghcr.io/cicirello/pyaction:3



COPY entrypoint.py /entrypoint.py
COPY requirements.txt /requirements.txt

# echo all files in the current directory
RUN ls -la

# give permission to execute the entrypoint
RUN chmod +x /entrypoint.py

# install the required packages
RUN pip install -r /requirements.txt

ENTRYPOINT ["/entrypoint.py"]