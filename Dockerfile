FROM alpine:latest
RUN apk add --update python py-pip ffmpeg && rm -rf /var/cache/apk/*
RUN mkdir -p /mnt/rec /mnt/stream /usr/share/streammgr
COPY rec.py cfg.py streammgr.py /usr/share/streammgr/
ENTRYPOINT ["/usr/bin/python"]
CMD ["/usr/share/streammgr/streammgr.py"]
