# Update & install Docker
  apt-get update && apt-get upgrade -y
  curl -fsSL https://get.docker.com | sh

  # Create a non-root deploy user
  useradd -m -s /bin/bash deploy
  usermod -aG docker deploy

   # Authorize the deploy key
  mkdir -p /home/deploy/.ssh
  echo "PASTE_CONTENTS_OF_scout_deploy.pub_HERE" >>
  /home/deploy/.ssh/authorized_keys
  chmod 700 /home/deploy/.ssh
  chmod 600 /home/deploy/.ssh/authorized_keys
  chown -R deploy:deploy /home/deploy/.ssh

   # Clone the repo
  mkdir -p /opt/scout
  chown deploy:deploy /opt/scout
  su - deploy -c "git clone https://github.com/YOUR_ORG/YOUR_REPO.git
  /opt/scout"


  Then manually copy your .env file to the VPS (this contains your
  secrets and should never go in Git or GitHub Actions):

  scp -i ~/.ssh/scout_deploy .env deploy@93.188.162.38:/opt/scout/.env