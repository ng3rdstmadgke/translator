# install
```bash
cd translator

# venv set up
python3.8 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# docker instal
sudo amazon-linux-extras install docker
sudo systemctl enable docker.service
sudo systemctl start docker.service
# ec2-userをdockerグループに追加してsudoなしでdockerを操作できるようにする
sudo usermod -a -G docker ec2-user
# 一度ログアウトして再ログイン

# sls deploy
npm install
sls deploy
```

