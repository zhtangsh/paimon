FROM python:3.9.18-bookworm

ENV MIRROR=https://pypi.tuna.tsinghua.edu.cn/simple
ENV PYTHONPATH=/dropbox/:/dropbox/paimon
ENV RQDATAC2_CONF=rqdata://license:bRFOV6yI5yB4q6jEDHG6d8-CO7XIfm30vPiz5x6HEHo1Tdv0NmwKkzIVwRAXCD2GTlZ1saBStp5QoseqRaqDgxrQH2iwx9W0cX_oXFBKryxP315CUrwdnmJMANNFI6RkygqqHjtd8tEoquzZkNRLJsAfcIU7J4YfH_LV3Lr-VnM=C-EpgalM0c02FKu1xLi-F-vGmhe6l98EOZq9oNdSf_CqolOd_dYbOSg8wzU2NAX0t2wUvFfyOAyUHY2r30mVOORPFRC7KaUzm0QJQwSDwo5urLhbOw8KuzLJCggjZpHRVrndoleoP3NgTL-jitixt6Tk9JPImuni5vj4Jz6IR7c=@rqdatad-pro.ricequant.com:16011
ENV TZ=Asia/Shanghai

WORKDIR /dropbox
ADD paimon/docker/requirement.txt requirement.txt
RUN pip install -i $MIRROR -r requirement.txt

ADD paimon paimon

ENTRYPOINT ["/usr/local/bin/python"]