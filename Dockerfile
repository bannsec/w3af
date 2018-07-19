FROM ubuntu:18.04

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get dist-upgrade -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y git python python-pip npm sudo libxml2-dev libxslt1-dev graphviz python-gtk2 wget && \
    cd /opt && git clone --depth 1 https://github.com/andresriancho/w3af.git && \
    cd w3af && \
    ./w3af_console && \
    /tmp/w3af_dependency_install.sh && \
    wget http://ftp.cn.debian.org/debian/pool/main/p/python-support/python-support_1.0.15_all.deb && \
    dpkg -i python-support_1.0.15_all.deb || apt-get install -fy && \
    apt --fix-broken install && \
    wget http://ftp.cn.debian.org/debian/pool/main/p/pywebkitgtk/python-webkit_1.1.8-3_amd64.deb && \
    dpkg -i python-webkit_1.1.8-3_amd64.deb || apt-get install -fy && \
    apt --fix-broken install && \
    wget http://ftp.cn.debian.org/debian/pool/main/p/pywebkitgtk/python-webkit-dev_1.1.8-3_all.deb && \
    dpkg -i python-webkit-dev_1.1.8-3_all.deb || apt-get install -fy && \
    apt --fix-broken install && \
    apt-get install -y python-gtksourceview2 && \
    /opt/w3af/w3af_console || \
    /tmp/w3af_dependency_install.sh && \
    useradd -d /home/user -m user && \
    chown -R user:user /opt/w3af
    
USER user

WORKDIR /opt/w3af/
