import re
import os
import sys
import json
import subprocess
from github import Github


# Run curl to get the file info
def shell_output(cmd: str):
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    return output

# Comparing CLI arguments
if sys.argv[1].startswith("http"):                      
    lines = shell_output(fr"curl -s {sys.argv[1]}").decode().split("\n")
else:
    with open(sys.argv[1], 'r') as f:
        lines = f.read().split("\n")

cleanLst = []

# clean the source file lines so that it can skip bad data
for line in lines:
	if len(line.split(" ")) == 2 and line.split(" ")[0].startswith("https://github.com"):
		cleanLst.append(line.split(" ")[0])

# using an access token via environment variable for higher request throughput
g = Github(os.getenv('GITHUB_API_TOKEN'))

# RegEx Pattern to get repo name from github link
regxPattern = re.compile(r"(?:git@|https:\/\/)github.com[:\/](.*).git")

finalDict = {}                                          # final dictionary output

# Iterating Github Repo Links
for link in cleanLst:                                   
    repoDict = {}
    repo = g.get_repo(regxPattern.findall(link)[0])
    contents = repo.get_contents("")
    # Browsing Github Repo
    while contents:                                     
        file_content = contents.pop(0)
        if file_content.type == "dir":
            contents.extend(repo.get_contents(file_content.path))
        # Searching for file named Dockerfile
        if file_content.name == "Dockerfile":           
            imgLst = []
            so = shell_output(fr"curl -s https://raw.githubusercontent.com/{regxPattern.findall(link)[0]}/master/{file_content.path}")
            rawLines = so.decode().split('\n')

            for oneLine in rawLines:                    # Iterating raw Dockerfile lines
                if oneLine.startswith("FROM"):          # Searching for docker images
                    imgLst.append(oneLine.split(' ')[1])

            repoDict[file_content.path] = imgLst

    finalDict[link] = repoDict


print(json.dumps({"data":finalDict}, indent=2))


    