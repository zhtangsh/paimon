FROM 192.168.1.50:29006/tools/python:3.9.18-bookworm

ENV MIRROR=https://pypi.tuna.tsinghua.edu.cn/simple
ENV PYTHONPATH=/dropbox/:/dropbox/paimon
ENV FILENAME_PREFIX=http://192.168.1.50:9000/cbond-strategy/trade_order/trade_order_ref_v6_
ENV RQDATAC2_CONF=rqdata://license:c4-2NvsJ9XY1801-IsFiPYY1WRz6yKXo_27MHkJ6vX8qHJPrz01ATZbOtfl-oQk3isUbm7VdbmRPPzMKOi2eL1NrtOIS60y3m6FSwdkW781UnstlCZwLUavSi2CK1gedKl0lI3jZFRwSqGa7XUNYJUh001NMvNdyBCzzYejvkXg=b82XowVTc6mtnfgxn_RNPad925S0lqSwJCeJzuDCFiplCF0lyrnisri8MKeNHfth9fNC7LF1qnKWjKxUbP683NOmmdZmqDRSemDXJ4ysRBxAb1tAZwWkCpuol0VWYUBR5ccBvL-ImbXhujUp89u8gpXQeQ3So7ctfQxRGXBVf7g=@rqdatad-pro.ricequant.com:16011
ENV TZ=Asia/Shanghai
ENV DATA_FEED=rqdata

WORKDIR /dropbox
ADD paimon/docker/requirement.txt requirement.txt
RUN pip install -i $MIRROR -r requirement.txt

ADD paimon paimon

ENTRYPOINT ["/usr/local/bin/python"]