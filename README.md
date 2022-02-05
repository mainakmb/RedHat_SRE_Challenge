# RedHat_SRE_Challenge

Script for scanning github repos and grab the image related information from Dockerfile

## Environment Variables

To run the script, you will need to set the shell environment variable

`GITHUB_API_TOKEN`

## Install Dependencies

Linux utility `curl` must be present and `python3` must be present
```
pip3 install -r requirements.txt
```

## Run the script

```
./main.py sources.txt

or

./main.py https://gist.githubusercontent.com/jmelis/c60e61a893248244dc4fa12b946585c4/raw/25d39f67f2405330a6314cad64fac423a171162c/sources.txt
```

## Sample Output

```
{
  "data": {
    "https://github.com/app-sre/qontract-reconcile.git": {
      "dockerfiles/Dockerfile": [
        "quay.io/app-sre/qontract-reconcile-builder:0.2.0",
        "quay.io/app-sre/qontract-reconcile-base:0.7.1"
      ]
    },
    "https://github.com/app-sre/container-images.git": {
      "jiralert/Dockerfile": [
        "registry.access.redhat.com/ubi8/go-toolset:latest",
        "registry.access.redhat.com/ubi8-minimal:8.2"
      ],
      "qontract-reconcile-base/Dockerfile": [
        "registry.access.redhat.com/ubi8/ubi:8.4",
        "registry.access.redhat.com/ubi8/ubi-minimal:8.4"
      ],
      "qontract-reconcile-builder/Dockerfile": [
        "registry.access.redhat.com/ubi8/ubi:8.4",
        "quay.io/app-sre/qontract-reconcile-base:0.6.2"
      ]
    }
  }
}
```

## Docker Usage

Set env variable  `GITHUB_API_TOKEN`

```
docker run -e GITHUB_API_TOKEN=XXXXXXX --name test mainakmb/imageinfo-grabber source.txt/raw_text_link
```

## Run as Kubernetes Job

Edit the `job.yaml` file, set the `GITHUB_API_TOKEN` value and set the `args`

```
  - name: imageinfo-grabber
    image: mainakmb/imageinfo-grabber:1.0
    env:
    - name: GITHUB_API_TOKEN
      value: "<acccess-key>"
    args: 
    - "https://gist.githubusercontent.com/jmelis/c60e61a893248244dc4fa12b946585c4/raw/25d39f67f2405330a6314cad64fac423a171162c/sources.txt"
  restartPolicy: Never
```
