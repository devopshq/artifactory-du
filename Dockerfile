FROM python:3-alpine

RUN python -mpip install artifactory-du && rm -rf ~/.cache
ENTRYPOINT [ "artifactory-du" ]
CMD [ "--help" ]
