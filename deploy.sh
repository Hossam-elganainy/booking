set -e
ssh root@45.10.161.56 'cd /root/islamic_chatbot && git pull --recurse-submodules'
ssh root@45.10.161.56 'cd /root/islamic_chatbot && docker-compose up -d --build'
ssh root@45.10.161.56 'cp /root/islamic_chatbot/infrastructure/nginx.conf /etc/nginx/sites-enabled/islamic_chatbot.conf'
ssh root@104.248.96.25 'cp ~/islamic_chatbot/infrastructure/fron_nginx.conf /etc/nginx/sites-enabled/islamic_chatbot_front.conf'
ssh root@45.10.161.56 'sudo nginx -s reload'


# py manage.py makemessages -l ar
# py manage.py compilemessages