ip a | fgrep inet | awk '{print $2}' | grep -v ':' | cut -f 1 -d '/' |  grep -v 127.0.0.1 | grep -v 192.168. | xargs -I {} echo -e "internal: {} port = 10086\nexternal: {}" > /etc/sockd.conf

cat sockd.tmpl >> /etc/sockd.conf
